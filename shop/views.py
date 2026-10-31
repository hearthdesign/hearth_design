# shop views
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.core.paginator import Paginator  # For pagination
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

import hashlib
import stripe

from shop.services.webhooks import handle_stripe_webhook

# Import all models
from .models import (
    Order,
    Print,
    Theme,
    ContactSubmission,
    Cart,
    CartItem,
)

from .forms import PrintForm, ContactForm, CustomSignupForm

stripe.api_key = settings.STRIPE_SECRET_KEY


# Homepage view
def homepage(request):
    # Get filters from query string
    print_type = request.GET.get("type")  # 'illustration' or 'photo'
    theme_slug = request.GET.get("theme")

    # Base queryset: active prints
    prints = Print.objects.filter(
        is_active=True,
        stock__gt=0,
    ).order_by("-date")

    # Filter by category type if provided
    if print_type in ["illustration", "photo"]:
        prints = prints.filter(type=print_type)

    # Filter by theme if provided
    theme = None
    if theme_slug:
        theme = Theme.objects.filter(slug=theme_slug).first()
        if theme:
            prints = prints.filter(themes=theme)

    # Paginate results
    paginator = Paginator(prints, 12)  # 12 prints per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "shop/homepage.html", {
        "page_obj": page_obj,
        "category": print_type,
        "theme": theme,
        "login_url": reverse("login"),
    })


# Upload print view
@login_required
def upload_print(request):
    if request.method == "POST":
        form = PrintForm(request.POST, request.FILES)

        if form.is_valid():
            print_obj = form.save(commit=False)

            # Set today's date automatically
            print_obj.date = timezone.now().date()

            print_obj.save()
            form.save_m2m()

            # Redirect based on type
            if print_obj.type == "photo":
                return redirect("photography_gallery")

            elif print_obj.type == "illustration":
                return redirect("illustration_gallery")

    else:
        form = PrintForm()

    return render(request, "shop/upload.html", {"form": form})

# Illustration gallery view
def illustration_gallery(request):
    prints = Print.objects.filter(
        type="illustration",
        stock__gt=0,
        is_active=True,
    ).order_by("-date")

    paginator = Paginator(prints, 20)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "shop/illustration_gallery.html", {
        "page_obj": page_obj,
        "category": "illustration",
        "theme": None,
    })

# Photography gallery
def photography_gallery(request):
    prints = Print.objects.filter(
        type="photo",
        stock__gt=0,
        is_active=True,
    ).order_by("-date")

    paginator = Paginator(prints, 20)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "shop/photography_gallery.html", {
        "page_obj": page_obj,
        "category": "photo",
        "theme": None,
    })

# Theme filter view with optional print type
def theme_filter(request):
    slug = request.GET.get("theme")

    if not slug:
        return redirect("homepage")

    # 'illustration' or 'photo'
    print_type = request.GET.get("type")

    # If it's missing, redirect to the homepage
    theme = get_object_or_404(Theme, slug=slug)

    # Base queryset
    prints = Print.objects.filter(
        themes=theme,
        stock__gt=0,
        is_active=True,
    )

    # Decide which queryset to use based on print type
    if print_type == "illustration":
        prints = prints.filter(type="illustration")
        template = "shop/illustration_gallery.html"

    elif print_type == "photo":
        prints = prints.filter(type="photo")
        template = "shop/photography_gallery.html"

    else:
        # If no print type is specified, return all active prints
        # belonging to the selected theme (combine both)
        template = "shop/themed_gallery.html"

    prints = prints.order_by("-date")

    # Paginate results
    paginator = Paginator(prints, 20)  # 20 items per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        template,
        {
            "page_obj": page_obj,
            "theme": theme,
            "print_type": print_type,
        },
    )

# Require login to access cart and checkout routes
# Add to cart (model-based, not session)
@login_required
def add_to_cart(request):

    print("=== ADD TO CART ===")
    print(request.POST)

    print_id = request.POST.get("print_id")

    print("print_id:", print_id)

    if not print_id or not print_id.isdigit():
        print("INVALID PRINT ID")
        return redirect("cart_view")

    print_obj = get_object_or_404(Print, id=print_id)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    quantity = max(1, quantity)
    quantity = min(quantity, print_obj.stock)

    print("quantity:", quantity)

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        print=print_obj,
        defaults={"price_at_time": print_obj.price},
    )

    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity = min(
            cart_item.quantity + quantity,
            print_obj.stock,
        )

    cart_item.save()

    print("CART ITEM SAVED")

    return redirect("cart_view")

# Require user to be logged in to view their cart
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.select_related('print')

    items = []
    for item in cart_items:
        items.append({
            'id': item.id,
            'print': item.print,
            'quantity': item.quantity,
            'price_at_time': item.price_at_time,
            'total': item.price_at_time * item.quantity,
        })
    total = sum(item['total'] for item in items)
    return render(request, 'shop/cart.html', {'cart_items': items,  'cart_total': total})

# Require user to be logged-in to increase items in cart
@login_required
def increase_cart_quantity(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user,
    )

    if cart_item.quantity < cart_item.print.stock:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart_view")

# Require user to be logged-in to remove items from cart
@login_required
def decrease_cart_quantity(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("cart_view")

@login_required
def remove_from_cart(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    cart_item.delete()

    return redirect("cart_view")

# Require user to be logged-in to proceed to checkout
@login_required
def create_checkout_session(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.cartitem_set.select_related("print")

    # Prevent checkout with an empty cart.
    if not cart_items.exists():
        return redirect("cart_view")



    line_items = []

    for item in cart_items:
        line_items.append({
            "price_data": {
                "currency": "eur",
                "product_data": {
                    "name": item.print.title,
                },
                "unit_amount": int(item.price_at_time * 100),
            },
            "quantity": item.quantity,
        })

    if not settings.STRIPE_SECRET_KEY:
        raise ImproperlyConfigured(
            "Stripe secret key is not configured."
        )
    session = stripe.checkout.Session.create(
        customer_email=request.user.email,
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        client_reference_id=str(request.user.id),
        success_url=(
            request.build_absolute_uri(
                reverse("payment_success")
            )
            + "?session_id={CHECKOUT_SESSION_ID}"
        ),

        cancel_url=request.build_absolute_uri(
            reverse("payment_cancel")
        )   
    )

    return redirect(session.url)


# Order history view
@login_required
def order_history(request):
    orders = Order.objects.filter(customer_email=request.user.email).prefetch_related("items__print")
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


@csrf_exempt
def stripe_webhook_view(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    event, status_code = handle_stripe_webhook(payload, sig_header)

    return HttpResponse(status=status_code)

# Payment  success view
def payment_success(request):
    return render(
        request,
        "shop/payment_success.html"
    )

# Payment cancel view
def payment_cancel(request):
    return render(
        request,
        "shop/payment_cancel.html"
    )