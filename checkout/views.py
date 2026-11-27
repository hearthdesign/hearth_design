# ==========================================
#          CHECKOUT & CART VIEWS
# ==========================================
import logging

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from checkout.services.webhooks import handle_stripe_webhook
from shop.models import Print

from .models import Cart, CartItem, Order

# Configure Stripe SDK secret key from Django settings; webhook verification
# uses STRIPE_WEBHOOK_SECRET inside checkout.services.webhooks.
stripe.api_key = settings.STRIPE_SECRET_KEY
# Server-side logger for diagnostic/security events (not user-facing; keep un-translated)
logger = logging.getLogger(__name__)


# ==========================================
#               CART MANAGEMENT
# ==========================================

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

    # Snapshot price_at_time when creating the item so cart pricing stays
    # consistent during the user's session
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

        # Clamp to current stock so cart quantity never exceeds available inventory
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
    # select_related("print") avoids N+1 queries when rendering print details/prices
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
    return render(
        request, "checkout/cart.html", {"cart_items": items, "cart_total": total}
    )


# ==========================================
#  INCREASE / DECREASE / REMOVE Q.TITY
# ==========================================
# Require user to be logged-in to increase items in cart
@login_required
def increase_cart_quantity(request, item_id):

    # Scope lookup by cart__user=request.user so users can only modify their own cart items
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
            _("'%(title)s' has been removed from your cart.") % {"title": item_title},
        )

    # Notify the user when the last cart item is removed
    if not remaining_items:
        messages.info(
            request,
            _(
                "Your cart is now empty. Browse the gallery to discover more artwork."
            ),
        )

    return redirect("cart_view")


# ==========================================
#          STRIPE CHECKOUT & ORDERS
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

    # Build Stripe line items in minor currency units (EUR cents); final payment
    # fulfillment, order creation, stock decrement, and cart clearing occur in the
    # verified webhook handler rather than on checkout start or success redirect.
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

    # Attach client_reference_id so the webhook handler can reconcile the session
    # back to the authenticated user idempotently.
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
    # Match orders linked to the current user, plus legacy/unlinked orders matching
    # their email only when user is null so foreign user accounts are never exposed.
    user_filter = Q(user=request.user)
    if request.user.email:
        user_filter |= Q(user__isnull=True, customer_email__iexact=request.user.email)

    orders = (
        Order.objects.filter(user_filter)
        .prefetch_related("items__print")
        .distinct()
    )
    return render(request, "checkout/order_history.html", {"orders": orders})


# ==========================================
#          STRIPE WEBHOOK HANDLER
# ==========================================
# Exempt from CSRF because Stripe sends server-to-server POST requests signed
# with HTTP_STRIPE_SIGNATURE; signature verification happens in handle_stripe_webhook.
@csrf_exempt
def stripe_webhook_view(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    # Pass raw request.body so Stripe's signature HMAC matches the exact wire payload
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    # Order creation, payment verification, atomic stock updates, and cart clearing
    # are handled inside handle_stripe_webhook / handle_checkout_session.
    _event, status_code = handle_stripe_webhook(payload, sig_header)
    return HttpResponse(status=status_code)


# ==========================================
#          PAYMENT RESULT PAGES
# ==========================================
@login_required
def payment_success(request):
    # Strictly read-only: visiting or refreshing the success URL must never mark
    # orders paid, decrement stock, or clear carts; only look up orders owned by
    # request.user so unknown or foreign session_ids fail safely.
    session_id = request.GET.get("session_id", "").strip()
    order = None

    if session_id:
        order = (
            Order.objects.filter(stripe_session_id=session_id, user=request.user)
            .prefetch_related("items__print")
            .first()
        )
        if not order:
            logger.info(
                "Success view accessed with unknown or non-owned session_id %s by user %s.",
                session_id,
                request.user.id,
            )

    return render(
        request,
        "checkout/payment_success.html",
        {
            "order": order,
            "session_id": session_id,
        },
    )


# Payment cancel view
@login_required
def payment_cancel(request):
    return render(request, "checkout/payment_cancel.html")


@login_required
def checkout_thanks(request):
    return render(request, "checkout/checkout_thanks.html")