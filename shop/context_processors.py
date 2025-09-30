def cart_count(request):
    # Get the cart dictionary from session
    cart = request.session.get('cart', {})
    
    # Return the total quantity of all items in the cart
    return {'cart_count': sum(cart.values())}
