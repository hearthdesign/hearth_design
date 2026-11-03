from django.urls import path
from . import views
from django.urls import reverse

urlpatterns = [
    # Stripe webhook route moved to project urls.py.
    # This prevents language-prefix redirects from interfering
    # with Stripe webhook deliveries.

    path("checkout/", views.create_checkout_session, 
              name="create_checkout_session"),
    path(
        "success/",
        views.payment_success,
        name="payment_success"
    ),

    path(
        "cancel/",
        views.payment_cancel,
        name="payment_cancel"
    ),
    path(
        "cart/increase/<int:item_id>/",
        views.increase_cart_quantity,
        name="increase_cart_quantity"
    ),

    path(
        "cart/decrease/<int:item_id>/",
        views.decrease_cart_quantity,
        name="decrease_cart_quantity"
    ),
    path(
    "cart/remove/<int:item_id>/",
    views.remove_from_cart,
    name="remove_from_cart"
    
),
]