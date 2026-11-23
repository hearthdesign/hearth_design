from django.conf import settings

from .models import Cart


def cart_count(request):

    if not request.user.is_authenticated:
        return {"cart_count": 0}

    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return {"cart_count": 0}

    count = sum(item.quantity for item in cart.cartitem_set.all())

    return {"cart_count": count}


def cart_total(request):
    if not request.user.is_authenticated:
        return {"cart_total": 0}

    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return {"cart_total": 0}

    total = 0
    for item in cart.cartitem_set.select_related("print"):
        total += item.print.price * item.quantity

    return {"cart_total": total}
