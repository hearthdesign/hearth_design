from django.conf import settings 
from .models import Print  # Import product model to calculate cart totals

def cart_count(request):
    # Get the cart dictionary from session
    cart = request.session.get('cart', {})
    
    # Return the total quantity of all items in the cart
    return {'cart_count': sum(cart.values())}

# Injects total price of cart into all templates
def cart_total(request):
    # Get the cart dictionary from session
    cart = request.session.get('cart', {})
    # Fetch all products currently in the cart
    items = Print.objects.filter(id__in=cart.keys())
    # Calculate total cost: price × quantity for each item
    total = sum(item.price * cart[str(item.id)] for item in items)
    # Return total price
    return {'cart_total': total}

# Injects basic user info into templates if logged in
def user_profile(request):
    # Only include user info if authenticated
    if request.user.is_authenticated:
        return {'user_profile': request.user}
    # Otherwise return empty dict
    return {}

# Injects site-wide settings like name and currency
def site_settings(request):
    return {
        # Use SITE_NAME from settings.py or default to 'Art Shop'
        'site_name': getattr(settings, 'SITE_NAME', 'Art Shop'),
        # Use CURRENCY from settings.py or default to '€'
        'currency': getattr(settings, 'CURRENCY', '€'),
    }