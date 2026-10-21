def get_cart_with_items(user):
    return Cart.objects.prefetch_related("cartitem_set__print").get(user=user)