from django.conf import settings

from .models import  Theme


def themes(request):
    return {"themes": Theme.objects.all()}


# Injects basic user info into templates if logged in
def user_profile(request):
    # Only include user info if authenticated
    if request.user.is_authenticated:
        return {"user_profile": request.user}
    # Otherwise return empty dict
    return {}


# Injects site-wide settings like name and currency
def site_settings(request):
    return {
        # Use SITE_NAME from settings.py or default to 'Art Shop'
        "site_name": getattr(settings, "SITE_NAME", "Art Shop"),
        # Use CURRENCY from settings.py or default to '€'
        "currency": getattr(settings, "CURRENCY", "€"),
    }
