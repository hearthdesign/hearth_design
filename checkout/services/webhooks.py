import logging
from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.db.models import F

from checkout.models import Cart, Order, OrderItem
from shop.models import Print

# Server-side logger for webhook verification, fulfillment, and anomaly tracking
# (not shown to end users).
logger = logging.getLogger(__name__)
User = get_user_model()


def handle_stripe_webhook(payload, sig_header):
    # Fail fast with 500 if webhook signing secret is missing so Stripe retries
    # once deployment configuration is fixed.
    if not settings.STRIPE_WEBHOOK_SECRET:
        logger.error("STRIPE_WEBHOOK_SECRET is not configured.")
        return None, 500

    # Verify HMAC signature against raw payload bytes to reject forged or tampered events.
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        logger.warning("Invalid Stripe webhook payload.")
        return None, 400
    except stripe.error.SignatureVerificationError:
        logger.warning("Invalid Stripe webhook signature.")
        return None, 400

    # Only fulfill once payment_status is confirmed as "paid" (covers both immediate
    # card checkout and asynchronous payment methods once succeeded).
    event_type = event.get("type")
    if event_type in {
        "checkout.session.completed",
        "checkout.session.async_payment_succeeded",
    }:
        session = event["data"]["object"]
        if session.get("payment_status") == "paid":
            handle_checkout_session(session, event_id=event.get("id"))
        else:
            logger.info(
                "Received %s (%s) with payment_status=%s; waiting for paid status.",
                event_type,
                event.get("id"),
                session.get("payment_status"),
            )

    return event, 200


def handle_checkout_session(session, event_id=None):
    """
    Handle the checkout session after payment is completed.

    Idempotently creates an Order and OrderItems from the user's cart items,
    marks the order paid, atomically decrements Print stock, and clears the
    cart. Safe against duplicate webhook deliveries and retries.
    """
    session_id = session.get("id")
    user_id = session.get("client_reference_id")

    if not session_id:
        logger.warning("Stripe session missing id in event %s.", event_id)
        return None

    # Fast idempotency check: if this Stripe session already produced a paid order,
    # return early without recreating items, re-deducting stock, or touching carts.
    existing = Order.objects.filter(stripe_session_id=session_id).first()
    if existing and existing.is_paid:
        return existing

    # Validate client_reference_id before resolving the buyer account.
    if not user_id or not str(user_id).isdigit():
        logger.warning(
            "Invalid or missing client_reference_id (%s) for session %s.",
            user_id,
            session_id,
        )
        return None

    try:
        user = User.objects.get(id=int(user_id))
    except User.DoesNotExist:
        logger.warning(
            "Unknown user %s referenced by Stripe session %s.",
            user_id,
            session_id,
        )
        return None

    with transaction.atomic():
        # Create or fetch the unique Order for this stripe_session_id, then lock
        # the row with select_for_update() to serialize concurrent deliveries.
        try:
            order, _created = Order.objects.get_or_create(
                stripe_session_id=session_id,
                defaults={
                    "user": user,
                    "customer_name": user.get_full_name() or user.username,
                    "customer_email": user.email,
                    "total_price": Decimal("0.00"),
                    "is_paid": False,
                },
            )
        except IntegrityError:
            order = Order.objects.get(stripe_session_id=session_id)

        order = Order.objects.select_for_update().get(pk=order.pk)
        if order.is_paid:
            return order

        # Lock the user's cart and prefetch related prints so item snapshots and
        # cart clearing happen consistently within the same transaction.
        cart = (
            Cart.objects.select_for_update()
            .filter(user=user)
            .prefetch_related("cartitem_set__print")
            .first()
        )
        cart_items = list(cart.cartitem_set.all()) if cart else []

        # If neither cart items nor existing order items exist (e.g., unknown/empty
        # state on retry), log and bail out cleanly without marking paid.
        if not cart_items and not order.items.exists():
            logger.warning(
                "No cart items or order items found for session %s and user %s.",
                session_id,
                user.id,
            )
            return None

        # Persist OrderItem rows using price_at_time so historical order totals are
        # preserved even if Print prices later change.
        if not order.items.exists():
            OrderItem.objects.bulk_create(
                [
                    OrderItem(
                        order=order,
                        print=item.print,
                        quantity=item.quantity,
                        price=item.price_at_time,
                    )
                    for item in cart_items
                ]
            )

        computed_total = sum(
            (item.price * item.quantity for item in order.items.all()),
            Decimal("0.00"),
        ).quantize(Decimal("0.01"))
        order.total_price = computed_total

        # Cross-check currency and total amount against Stripe session metadata/values
        # and log discrepancies for investigation.
        amount_total = session.get("amount_total")
        currency = session.get("currency")
        if currency and currency.lower() != "eur":
            logger.warning(
                "Unexpected currency %s for session %s (expected eur).",
                currency,
                session_id,
            )
        if amount_total is not None:
            expected_cents = int((computed_total * 100).to_integral_value())
            if int(amount_total) != expected_cents:
                logger.warning(
                    "Amount mismatch for session %s: Stripe=%s, computed_cents=%s.",
                    session_id,
                    amount_total,
                    expected_cents,
                )

        # Atomically decrement Print stock using F() expressions and clamp any
        # raced/oversold stock cleanly to 0 so inventory never goes negative.
        for order_item in order.items.select_related("print"):
            Print.objects.filter(
                pk=order_item.print_id, stock__gte=order_item.quantity
            ).update(stock=F("stock") - order_item.quantity)
            Print.objects.filter(pk=order_item.print_id, stock__lt=0).update(stock=0)

        order.is_paid = True
        order.save(update_fields=["total_price", "is_paid"])

        # Clear the user's cart only after order items, stock updates, and paid
        # status are prepared inside the atomic transaction.
        if cart:
            cart.cartitem_set.all().delete()

    return order