from shop.models import Cart

"""
Checkout service helpers.
Provides cart retrieval and checkout-related
database operations.
"""
def get_cart_with_items(user):
    return (
        Cart.objects
        .prefetch_related("cartitem_set__print")
        .get(user=user)
    )