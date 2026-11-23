# ==========================================
#          CHECKOUT ADMIN REGISTRATION
# ==========================================
from django.contrib import admin


from .models import (
    Cart,
    CartItem,
    Order,
    OrderItem,
)

# Register the Cart Model with the Admin site
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username", "user__email")


# Register the CartItem Model with the Admin site
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "print", "quantity")
    list_filter = ("print",)
    search_fields = ("cart__user__username", "print__title")


# Register the Order Model with the Admin site
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "customer_email",
        "total_price",
        "is_paid",
        "created_at",
    )
    list_filter = ("is_paid", "created_at")
    search_fields = ("customer_name", "customer_email")
    date_hierarchy = "created_at"

# Register the OrderItem Model with the Admin site
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "print", "quantity", "price")
    list_filter = ("print",)
    search_fields = ("order__customer_name", "print__title")