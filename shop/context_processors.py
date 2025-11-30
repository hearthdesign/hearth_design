from django.conf import settings 
from .models import Print  # Import product model to calculate cart totals
from .models import Cart

def cart_count(request):
    # Get the cart dictionary from session
    cart = request.session.get('cart', {})
    
    # Return the total quantity of all items in the cart
    return {'cart_count': sum(cart.values())}

def cart_total(request):
    if not request.user.is_authenticated:
        return {'cart_total': 0}

    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return {'cart_total': 0}

    total = 0
    for item in cart.cartitem_set.select_related('print'):
        total += item.print.price * item.quantity

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