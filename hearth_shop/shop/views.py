# shop views
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator # For pagination
from django.conf import settings
# To restrict access to logged-in users
from django.contrib.auth.decorators import login_required  
from django.core.mail import send_mail  # For sending emails
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import datetime
import stripe
import hashlib

# Import all models
from .models import Print, Theme, ContactSubmission, Cart, CartItem, Order
from .forms import PrintForm, ContactForm, CustomSignupForm

stripe.api_key = settings.STRIPE_SECRET_KEY

#Homepage view
def homepage(request):
    login_url = reverse('login')  # URL for the login page
    return render(request, 'shop/homepage.html', {'login_url': login_url})

# Upload print view
@login_required
def upload_print(request):
    if request.method == 'POST':
        form = PrintForm(request.POST, request.FILES)
        if form.is_valid():
            print_obj = form.save(commit=False)

            # Set today's date automatically 
            print_obj.date = datetime.today().date()
            print_obj.save()
            form.save_m2m()

            # Redirect based on type
            if print_obj.type == 'photography':
                return redirect('photography_gallery')
            else:
                return redirect('illustration_gallery')
    else:
        form = PrintForm()
    return render(request, 'shop/upload.html', {'form': form})

# Illustration gallery view
def illustration_gallery(request):
    prints = Print.objects.filter(type='illustration', in_stock=True)
    paginator = Paginator(prints, 20)  # 20 items per page
    page_number = request.GET.get('page')  # get current page number
    page_obj = paginator.get_page(page_number) 
    return render(request, 'shop/illustration_gallery.html', {'page_obj': page_obj})


# Photography gallery view
def photography_gallery(request):
    prints = Print.objects.filter(type='photo', in_stock=True)
    paginator = Paginator(prints, 20)  # 20 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/photography_gallery.html', {'page_obj': page_obj})

# Theme filter view with optional category
def theme_filter(request):
    slug = request.GET.get('theme')
    category = request.GET.get('type')  # 'illustration' or 'photography'
    theme = get_object_or_404(Theme, slug=slug)

    prints = Print.objects.filter(themes=theme)

    if category == 'illustration':
        prints = prints.filter(type='illustration')
        template = 'shop/illustration_gallery.html'
    elif category == 'photography':
        prints = prints.filter(type='photo')
        template = 'shop/photography_gallery.html'
    else:
        template = 'shop/theme_filtered_gallery.html'

    return render(request, template, {
        'prints': prints,
        'theme': theme,
        'category': category
    })

# Require login to access cart and checkout routes
# Add to cart (model-based, not session)
@login_required
def add_to_cart(request):
    print_id = request.POST.get('print_id')  # Get the print ID
    # Get the quantity default to 1
    quantity = int(request.POST.get('quantity', 1))  
    # validate print ID
    if not print_id or not print_id.isdigit(): 
        return redirect('cart_view')
    
    print = get_object_or_404(Product, id=print_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, print=print)
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity
    cart_item.save()


    return redirect('cart_view')

# Require user to be logged in to view their cart
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.select_related('print')

    items = []
    for item in cart_items:
        items.append({
            'print': item.print,
            'quantity': item.quantity,
            'total': item.print.price * item.quantity,
        })
    total = sum(item.print.price * item.quantity for item in cart_items)
    return render(request, 'shop/cart.html', {'cart_items': items,  'cart_total': total})

# Require user to be logged-in to proceed to checkout
@login_required
def create_checkout_session(request):
    cart = get_object_or_404(Cart, user=request.user)
    line_items = []

    for item in cart.cartitem_set.select_related('print'):
        line_items.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {'name': item.print.title},
                'unit_amount': int(item.print.price * 100),
            },
            'quantity': item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        client_reference_id=request.user.id,
        success_url='http://127.0.0.1:8000/success/',
        cancel_url='http://127.0.0.1:8000/cancel/',
    )

    return redirect(session.url)

# Order history view
@login_required
def order_history(request):
    orders = Order.objects.filter(customer_email=request.user.email).prefetch_related("items__product")
    return render(request, "shop/order_history.html", {"orders": orders})

# Contact form
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Honeypot check
            if form.cleaned_data.get('website'):
                return redirect('thank_you')

            # Privacy checkbox server-side validation
            if not form.cleaned_data.get('privacy_agree'):
                form.add_error('privacy_agree', _("You must agree to the Privacy Notice"))
            else:
                # Metadata
                ip = request.META.get('REMOTE_ADDR', '')
                user_agent = request.META.get('HTTP_USER_AGENT', '')
                ip_hash = hashlib.sha256(ip.encode()).hexdigest()

                # Save to database
                ContactSubmission.objects.create(
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    message=form.cleaned_data['message'],
                    ip_hash=ip_hash,
                    user_agent=user_agent,
                    submitted_at=timezone.now(),
                    marketing_consent=form.cleaned_data.get('marketing_consent', False)
                )

                # Send email to admin
                send_mail(
                    subject=_("New Contact Form Submission from %(name)s") % {'name': form.cleaned_data['name']},
                    message=form.cleaned_data['message'],
                    from_email=form.cleaned_data['email'],
                    recipient_list=['1.space.channel.1@gmail.com'],
                )

                # Confirmation email to user
                subject = _("Thank you for contacting Hearth Design")
                message = _(
                    f"Hi {form.cleaned_data['name']},\n\n"
                    "Thank you for reaching out to us. We've received your message and will get back to you shortly.\n\n"
                    "Best regards,\nHearth Design Team"
                )
                send_mail(
                    subject=subject,
                    message=message,
                    from_email='noreply@hearth.design',
                    recipient_list=[form.cleaned_data['email']],
                )

                return redirect('thank_you')
    else:
        form = ContactForm()
    return render(request, 'shop/contact.html', {'form': form})

# Signup
def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_mail(
                subject="Welcome to Hearth Shop!",
                message="Thank you for signing up, {}.".format(user.username),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return redirect('login')
    else:
        form = CustomSignupForm()
    return render(request, 'registration/signup.html', {'form': form})