from django.contrib import admin
from .models import (
    Category, Theme, Print, Photography, Illustration,
    Cart, CartItem, Order, OrderItem, ContactSubmission
    )

# Register the Category Model with the Admin site
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "parent", "is_active", "created_at")
    list_filter = ("type", "is_active")
    search_fields = ("title", "slug", "description")
    prepopulated_fields = {"slug": ("title",)}

# Register the Theme Model with the admin site
@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}

# Register the Print Model with the Admin site
@admin.register(Print)
class PrintAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "format", "size", "price", "stock", "sku", "is_active", "in_stock")
    list_filter = ("type", "format", "is_active", "in_stock", "themes", "category")
    search_fields = ("title", "slug", "sku", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("title",)
    filter_horizontal = ('themes',)

# Register the Photography Model with the Admin site
@admin.register(Photography)
class PhotographyAdmin(admin.ModelAdmin):
    list_display = ("title", "print", "quantity", "price", "in_stock")
    list_filter = ("in_stock", "themes")
    search_fields = ("title", "slug", "description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('themes',)

# Register the Illustration Model with the Admin site
@admin.register(Illustration)
class IllustrationAdmin(admin.ModelAdmin):
    list_display = ("title", "print", "quantity", "price", "in_stock")
    list_filter = ("in_stock", "themes")
    search_fields = ("title", "slug", "description")
    prepopulated_fields = {"slug": ("title",)}

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
    list_display = ('id', 'customer_name', 'customer_email', 'total_price', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('customer_name', 'customer_email')
    date_hierarchy = "created_at"    

# Register the OrderItem Model with the Admin site
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "print", "quantity", "price")
    list_filter = ("print",)
    search_fields = ("order__customer_name", "print__title")

# Register the ContactSubmission Model with the Admin site
@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at', 'marketing_consent')
    readonly_fields = ('submitted_at', 'ip_hash', 'user_agent')
    search_fields = ('name', 'email', 'message')
    list_filter = ("marketing_consent", "submitted_at")
    date_hierarchy = "submitted_at"

