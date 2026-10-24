from django.urls import path
from . import views
from django.urls import reverse

urlpatterns = [
    path("stripe/webhook/", views.stripe_webhook_view, 
         name="stripe-webhook"),
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
]