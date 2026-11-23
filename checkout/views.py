# ==========================================
#          CHECKOUT & CART VIEWS
# ==========================================
import logging

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from shop.models import Print
from checkout.services.webhooks import handle_stripe_webhook

from .models import Cart, CartItem, Order

stripe.api_key = settings.STRIPE_SECRET_KEY
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

    # If the payment completed successfully, fulfill the order (clears cart 
    # & reduces stock)
    if (
        status_code == 200
        and _event
        and _event.get("type") == "checkout.session.completed"
    ):
        session = _event["data"]["object"]
        fulfill_order_from_stripe_session(session)

    return HttpResponse(status=status_code)


# ==========================================
#          PAYMENT RESULT PAGES
# ==========================================
@login_required
def payment_success(request):
    # Optional fallback fulfillment check if user hits success URL directly 
    # before webhook fires
    session_id = request.GET.get("session_id")
    if session_id and settings.STRIPE_SECRET_KEY:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if (
                session
                and session.get("payment_status") == "paid"
                and session.get("client_reference_id") == str(request.user.id)
            ):
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

