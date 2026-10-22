from django.urls import path
from . import views

urlpatterns = [
    path("stripe/webhook/", views.stripe_webhook_view, 
         name="stripe-webhook"),
    path("checkout/", views.create_checkout_session, 
              name="create_checkout_session"),
]