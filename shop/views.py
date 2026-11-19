# shop views

import hashlib
import logging

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.core.paginator import Paginator  # For pagination
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, translate_url
from django.utils import timezone, translation
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from shop.services.webhooks import handle_stripe_webhook

from .forms import ContactForm, CustomSignupForm, PrintForm, ReviewForm

# Import all models
from .models import Cart, CartItem, ContactSubmission, Order, Print, Theme

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)


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

    return render(
        request,
        "shop/homepage.html",
        {
            "page_obj": page_obj,
            "category": print_type,
            "theme": theme,
            "login_url": reverse("login"),
        },
    )


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

    return render(
        request,
        "shop/illustration_gallery.html",
        {
            "page_obj": page_obj,
            "category": "illustration",
            "theme": None,
        },
    )


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

    return render(
        request,
        "shop/photography_gallery.html",
        {
            "page_obj": page_obj,
            "category": "photo",
            "theme": None,
        },
    )


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
            "selected_theme": theme,
            "print_type": print_type,
            "category": print_type,
        },
    )


# ==========================================
#               ADD TO CART
# ==========================================
# Require login to access cart and checkout routes
# Add to cart (model-based, not session)
@login_required
def add_to_cart(request):

    print_id = request.POST.get("print_id")

    # Validate incoming product ID
    # Reject missing or non-numeric IDs before querying the database
    if not print_id or not print_id.isdigit():
        messages.error(request, _("Invalid product selection."))
        return redirect("cart_view")

    print_obj = get_object_or_404(Print, id=print_id)

    # Validate requested quantity
    # Fall back to a safe value if invalid data is submitted
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        # Invalid quantity entered, set to 1 and show a warning message
        messages.warning(
            request, _("Invalid quantity entered. Quantity has been reset to 1.")
        )
        quantity = 1

    # Prevent zero or negative quantities
    # quantity = max(1, quantity)
    if quantity < 1:
        messages.warning(
            request,
            _("Quantity must be greater than zero. Quantity has been reset to 1."),
        )
        quantity = 1

    # Prevent quantities exceeding available stock

    if quantity > print_obj.stock:
        messages.warning(
            request,
            _("Only %(stock)s item(s) currently available.")
            % {"stock": print_obj.stock},
        )
        quantity = print_obj.stock

    # Prevent adding unavailable products
    if print_obj.stock <= 0:
        messages.error(request, _("This item is currently out of stock."))
        return redirect("cart_view")

    cart, _created = Cart.objects.get_or_create(user=request.user)

    cart_item, _created = CartItem.objects.get_or_create(
        cart=cart,
        print=print_obj,
        defaults={"price_at_time": print_obj.price},
    )

    if _created:
        cart_item.quantity = quantity

    else:
        requested_total = cart_item.quantity + quantity

        if requested_total > print_obj.stock:
            messages.error(request, _("Requested quantity exceeds available stock."))

        cart_item.quantity = min(
            requested_total,
            print_obj.stock,
        )
    cart_item.save()

    messages.success(
        request, _('"%(title)s" added to your cart.') % {"title": print_obj.title}
    )
    return redirect("cart_view")


# Require user to be logged in to view their cart
@login_required
def cart_view(request):
    cart, _created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.select_related("print")

    items = []
    for item in cart_items:
        items.append(
            {
                "id": item.id,
                "print": item.print,
                "quantity": item.quantity,
                "price_at_time": item.price_at_time,
                "total": item.price_at_time * item.quantity,
            }
        )

    total = sum(item["total"] for item in items)
    return render(request, "shop/cart.html", {"cart_items": items, "cart_total": total})


# ==========================================
#  INCREASE / DECREASE / REMOVE Q.TITY
# ==========================================
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
        messages.success(
            request,
            _('Quantity of "%(title)s" increased to %(qty)s.')
            % {
                "title": cart_item.print.title,
                "qty": cart_item.quantity,
            },
        )
    else:
        messages.warning(request, _("No additional stock is available for this item."))

    return redirect("cart_view")


# Require user to be logged-in to remove items from cart
@login_required
def decrease_cart_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.info(
            request,
            _('Quantity of "%(title)s" decreased to %(qty)s.')
            % {
                "title": cart_item.print.title,
                "qty": cart_item.quantity,
            },
        )

    else:
        item_title = cart_item.print.title
        cart_item.delete()
        messages.info(
            request,
            _("'%(title)s' has been removed from your cart.") % {"title": item_title},
        )

    return redirect("cart_view")


@login_required
def remove_from_cart(request, item_id):

    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    item_title = cart_item.print.title
    cart_item.delete()

    remaining_items = CartItem.objects.filter(cart__user=request.user).exists()

    if remaining_items:
        messages.warning(
            request,
            _('"%(title)s" has been removed from your cart.') % {"title": item_title},
        )

        if not remaining_items:
            messages.info(
                request,
                _(
                    "Your cart is now empty. Browse the gallery to discover more artwork."
                ),
            )

    return redirect("cart_view")


# ==========================================
#              CHECKOUT
# ==========================================
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
        line_items.append(
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": item.print.title,
                    },
                    "unit_amount": int(item.price_at_time * 100),
                },
                "quantity": item.quantity,
            }
        )

    if not settings.STRIPE_SECRET_KEY:
        raise ImproperlyConfigured("Stripe secret key is not configured.")
    session = stripe.checkout.Session.create(
        customer_email=request.user.email,
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        client_reference_id=str(request.user.id),
        success_url=(
            request.build_absolute_uri(reverse("payment_success"))
            + "?session_id={CHECKOUT_SESSION_ID}"
        ),
        cancel_url=request.build_absolute_uri(reverse("payment_cancel")),
    )

    return redirect(session.url)


# ==========================================
#             ORDER HISTORY
# ==========================================
@login_required
def order_history(request):
    orders = Order.objects.filter(customer_email=request.user.email).prefetch_related(
        "items__print"
    )
    return render(request, "shop/order_history.html", {"orders": orders})


@login_required  # Ensures only logged-in users can leave reviews
def add_review(request, print_id):
    print_item = get_object_or_404(Print, id=print_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Create the review object but don't save to DB yet
            review = form.save(commit=False)

            # Attach the print item and the currently logged-in user
            review.print_item = print_item
            review.user = request.user

            # Now save it permanently to the database
            review.save()

            # Redirect back to the print detail page or gallery
            return redirect(
                "homepage"
            )  # Replace with your actual detail or redirect URL
    else:
        form = ReviewForm()

    return render(
        request, "shop/add_review.html", {"form": form, "print_item": print_item}
    )


# ==========================================
#              SET LANGUAGE
# ==========================================
def custom_set_language(request):
    """
    Custom language switcher view that safely handles i18n URL prefixes
    and prevents redirect loops.
    """
    next_url = request.POST.get("next", request.GET.get("next", "/"))
    lang_code = request.POST.get("language", request.GET.get("language"))

    if lang_code and lang_code in [lang[0] for lang in settings.LANGUAGES]:
        # Activate language and set translation environment
        translation.activate(lang_code)

        # Strip current language prefix from next_url if present (e.g., '/de/about/' -> '/about/')
        # FIX: Use .lower() to match lowercase URL prefixes like '/zh-hans/'
        for lang in [lang[0] for lang in settings.LANGUAGES]:
            prefix = f"/{lang}/".lower()
            if next_url.lower().startswith(prefix):
                next_url = next_url[len(prefix) - 1 :]  # Keeps the leading slash
                break
            elif next_url.lower() == f"/{lang}".lower():
                next_url = "/"
                break

        # Translate the URL into the new language prefix pattern
        translated_url = translate_url(next_url, lang_code)

        # Create response and set the official Django language cookie
        response = HttpResponseRedirect(translated_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
        return response

    return HttpResponseRedirect("/")


# ==========================================
#             CONTACT FORM
# ==========================================
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Honeypot check
            if form.cleaned_data.get("website"):
                return redirect("thank_you")

            # Privacy checkbox server-side validation
            if not form.cleaned_data.get("privacy_agree"):
                form.add_error(
                    "privacy_agree", _("You must agree to the Privacy Notice")
                )
            else:
                # Metadata
                ip = request.META.get("REMOTE_ADDR", "")
                user_agent = request.META.get("HTTP_USER_AGENT", "")
                ip_hash = hashlib.sha256(ip.encode()).hexdigest()

                # Save to database
                ContactSubmission.objects.create(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"],
                    message=form.cleaned_data["message"],
                    ip_hash=ip_hash,
                    user_agent=user_agent,
                    submitted_at=timezone.now(),
                    marketing_consent=form.cleaned_data.get("marketing_consent", False),
                )

                # Send email to admin
                send_mail(
                    subject=_("New Contact Form Submission from %(name)s")
                    % {"name": form.cleaned_data["name"]},
                    message=form.cleaned_data["message"],
                    from_email=form.cleaned_data["email"],
                    recipient_list=["1.space.channel.1@gmail.com"],
                )

                # Confirmation email to user
                subject = _("Thank you for contacting Hearth Design")
                message = _(
                    "Hi %(name)s,\n\n"
                    "Thank you for reaching out to us. "
                    "We've received your message and will get back to you shortly.\n\n"
                    "Best regards,\n"
                    "Hearth Design Team"
                ) % {"name": form.cleaned_data["name"]}
                send_mail(
                    subject=subject,
                    message=message,
                    from_email="noreply@hearth.design",
                    recipient_list=[form.cleaned_data["email"]],
                )

                return redirect("thank_you")
    else:
        form = ContactForm()
    return render(request, "shop/contact.html", {"form": form})


# ==========================================
#              SIGNUP
# ==========================================
def signup(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_mail(
                subject="Welcome to Hearth Shop!",
                message=f"Thank you for signing up, {user.username}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return redirect("login")
    else:
        form = CustomSignupForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def thank_you(request):
    return render(request, "shop/thank_you.html")


# ==========================================
#   STRIPE FULFILLMENT & WEBHOOK HANDLERS
# ==========================================
def fulfill_order_from_stripe_session(session):
    """
    Fulfills the order: marks it paid, decrements product stock,
    and clears the user's cart. Safe to run multiple times (idempotent).
    """
    session_id = session.get("id")
    client_ref_id = session.get("client_reference_id")

    try:
        order = Order.objects.get(stripe_session_id=session_id)
    except Order.DoesNotExist:
        return  # Order hasn't been created yet

    if order.is_paid:
        return  # Already fulfilled, prevent double-deducting stock

    with transaction.atomic():
        # 1. Mark order as paid
        order.is_paid = True
        order.save()

        # 2. Reduce stock for each purchased print
        for item in order.items.select_related("print").all():
            print_obj = item.print
            print_obj.stock = max(0, print_obj.stock - item.quantity)
            print_obj.save()

        # 3. Clear the user's cart using client_reference_id (user ID)
        if client_ref_id:
            Cart.objects.filter(user_id=client_ref_id).delete()


@csrf_exempt
def stripe_webhook_view(request):
    print("WEBHOOK VIEW HIT")
    if request.method != "POST":
        return HttpResponse(status=405)

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    _event, status_code = handle_stripe_webhook(payload, sig_header)

    # If the payment completed successfully, fulfill the order (clears cart & reduces stock)
    if (
        status_code == 200
        and _event
        and _event.get("type") == "checkout.session.completed"
    ):
        session = _event["data"]["object"]
        fulfill_order_from_stripe_session(session)

    return HttpResponse(status=status_code)


# Payment success view
@login_required
def payment_success(request):
    # Optional fallback fulfillment check if user hits success URL directly before webhook fires
    session_id = request.GET.get("session_id")
    if session_id and settings.STRIPE_SECRET_KEY:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = None
        try:
            # If your stripe utility or API lets you fetch the session, you can trigger fulfillment here too
            if session.get("payment_status") == "paid":
                fulfill_order_from_stripe_session(session)
        except stripe.error.StripeError:
            logger.exception(
                "Failed to retrieve Stripe checkout session %s", session_id
            )

    return render(request, "shop/payment_success.html")


# Payment cancel view
@login_required
def payment_cancel(request):
    return render(request, "shop/payment_cancel.html")


@login_required
def checkout_thanks(request):
    return render(request, "shop/checkout_thanks.html")


# Terms of Service
def terms_of_service(request):
    return render(request, "shop/terms.html")


# Private Policy
def privacy_policy(request):
    return render(request, "shop/privacy_policy.html")


# robots.txt
class RobotsTxtView(TemplateView):
    template_name = "robots.txt"
