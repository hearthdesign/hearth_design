from requests import session
import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from shop.models import Cart, Order, OrderItem

def handle_stripe_webhook(payload, sig_header):
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return None, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return None, 400

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session(session)

    return event, 200

# The function handels the checkout session after the payment is completed.
# It creates an order and order items based on the cart items, and then 
# clears the cart.
def handle_checkout_session(session):

    print("=== STRIPE PAYMENT COMPLETED ===")
    print(session)
    user_id = session.get("client_reference_id")

    if not user_id:
        return

    User = get_user_model()

    try:
        user = User.objects.get(id=user_id)
        cart = Cart.objects.get(user=user)
    except (User.DoesNotExist, Cart.DoesNotExist):
        return

    total_price = sum(
        item.price_at_time * item.quantity
        for item in cart.cartitem_set.all()
    )

    order = Order.objects.create(
        customer_name=user.username,
        customer_email=user.email,
        stripe_session_id=session["id"],
        total_price=total_price,
        is_paid=True,
    )

    for cart_item in cart.cartitem_set.select_related("print"):
        OrderItem.objects.create(
            order=order,
            print=cart_item.print,
            quantity=cart_item.quantity,
            # Stores the purchase price permanently.
            price=cart_item.price_at_time,
        )

    cart.cartitem_set.all().delete()
    print("ORDER CREATED:", order.id)