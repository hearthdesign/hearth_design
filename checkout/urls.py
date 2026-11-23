# ==========================================
#          CHECKOUT APP URL ROUTES
# ==========================================
from django.urls import path

from . import views


    # Note: The Stripe webhook endpoint is registered at the project level in
    # hearth_shop/urls.py outside i18n_patterns
    # This prevents language-prefix redirects from interfering
    # with Stripe webhook deliveries.
urlpatterns = [
    # Cart actions
    path("cart/", views.cart_view, name="cart_view"),
    path("cart/add/", views.add_to_cart, name="add_to_cart"),
    path(
        "cart/increase/<int:item_id>/",
        views.increase_cart_quantity,
        name="increase_cart_quantity",
    ),
    path(
        "cart/decrease/<int:item_id>/",
        views.decrease_cart_quantity,
        name="decrease_cart_quantity",
    ),
    path(
        "cart/remove/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    # Checkout & order history
    path(
        "checkout/",
        views.create_checkout_session,
        name="create_checkout_session",
    ),
    path("checkout/success/", views.payment_success, name="payment_success"),
    path("checkout/cancel/", views.payment_cancel, name="payment_cancel"),
    path("checkout/thanks/", views.checkout_thanks, name="checkout_thanks"),
    path("orders/", views.order_history, name="order_history"),
]