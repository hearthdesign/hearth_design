# ==========================================
#          CHECKOUT APP MODELS
# ==========================================
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


# ==========================================
#                CART MODEL
# ==========================================
class Cart(models.Model):
    # Each user has a single active shopping cart
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # String reference avoids top-level circular imports with shop.models
    prints = models.ManyToManyField("shop.Print", through="CartItem")

    class Meta:
        # Preserve existing table name during extraction from shop
        db_table = "shop_cart"
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    def __str__(self):
        return f"Cart of {self.user.username}"


# ==========================================
#              CART ITEM MODEL
# ==========================================
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    print = models.ForeignKey(
        "shop.Print",
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(default=1)
    price_at_time = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = "shop_cartitem"
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")
        constraints = [
            models.UniqueConstraint(fields=["cart", "print"], name="unique_cart_print"),
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0), name="cartitem_quantity_gt_0"
            ),
        ]

    def __str__(self):
        if self.print:
            return f"{self.quantity} x {self.print.title} in {self.cart.user.username}'s cart"
        return f"{self.quantity} item(s) in {self.cart.user.username}'s cart"


# ==========================================
#                ORDER MODEL
# ==========================================
class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    # Unique Stripe session ID prevents duplicate order fulfillment
    stripe_session_id = models.CharField(
        max_length=255,
        blank=True,
        default="",
        unique=True,
    )
    prints = models.ManyToManyField("shop.Print", through="OrderItem")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        db_table = "shop_order"
        ordering = ["-created_at"]
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def calculate_total(self):
        return sum(
            (item.price * item.quantity for item in self.items.all()),
            Decimal("0.00"),
        )

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


# ==========================================
#              ORDER ITEM MODEL
# ==========================================
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    print = models.ForeignKey("shop.Print", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "shop_orderitem"
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return f"{self.quantity} x {self.print.title} in Order #{self.order.id}"
