# shop views
from django.shortcuts import render, get_object_or_404, redirect
from .models import Print, Theme, ContactSubmission
from django.urls import reverse
from django.core.paginator import Paginator # For pagination
import stripe
from django.conf import settings
# To restrict access to logged-in users
from django.contrib.auth.decorators import login_required  
from .forms import PrintForm, ContactForm
from django.core.mail import send_mail  # For sending emails
import hashlib
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from .forms import CustomSignupForm

stripe.api_key = settings.STRIPE_SECRET_KEY

#Homepage view
def homepage(request):
    login_url = reverse('login')  # URL for the login page
    return render(request, 'shop/homepage.html', {'login_url': login_url})

# Form for uploading prints
# @login_required
# def upload_print(request):
#     if request.method == 'POST':
#         form = PrintForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('illustration_gallery')  
#     else:
#         form = PrintForm()
#     return render(request, 'shop/upload.html', {'form': form})

@login_required
def upload_print(request):
    if request.method == 'POST':
        form = PrintForm(request.POST, request.FILES)
        if form.is_valid():
            print_obj = form.save(commit=False)

            # Automatically set today's date
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

# only logged-in users can access cart and checkout routes
# Require user to be logged in to access this view
@login_required
def add_to_cart(request):
    
    product_id = request.POST.get('product_id')  # Get the product ID
    # Get the quantity default to 1
    quantity = int(request.POST.get('quantity', 1))  
    # Retrieve the current cart from the session, or initialize an empty dict
    cart = request.session.get('cart', {})

    # If the product is already in the cart, increase its quantity
    if product_id in cart:
        cart[product_id] += quantity
    else:
        # Otherwise, add it with the selected quantity
        cart[product_id] = quantity
    # Save the updated cart back into the session
    request.session['cart'] = cart
    # Mark the session as modified to ensure Django saves it
    request.session.modified = True
    # Redirect the user to the cart view page
    return redirect('cart_view')

# Require user to be logged in to view their cart
@login_required
def cart_view(request):
    # Get the cart dictionary from the session
    cart = request.session.get('cart', {})
    # Fetch all Print objects whose IDs are in the cart
    items = Print.objects.filter(id__in=cart.keys())
    # Prepare a list of cart items with quantity and total price
    cart_items = []
    for item in items:
        cart_items.append({
            'product': item,  # The Print object
            'quantity': cart[str(item.id)],  # Quantity from session
            'total': item.price * cart[str(item.id)],  # Total cost
        })

    # Render the cart template with the cart_items context
    return render(request, 'shop/cart.html', {'cart_items': cart_items})

# Require user to be logged-in to proceed to checkout
@login_required
def create_checkout_session(request, product_id):
    product = get_object_or_404(Print, id=product_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {'name': product.title},
                'unit_amount': int(product.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/success/',
        cancel_url='http://127.0.0.1:8000/cancel/',
    )
    return redirect(session.url)

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