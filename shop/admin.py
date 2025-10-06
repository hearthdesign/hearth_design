from django.contrib import admin
from .models import Theme, Print, Photography, Category, Cart, CartItem, Product, Order, ContactSubmission

# Register the Theme Model with the admin site
@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

# Register the Print Model with the Admin site
@admin.register(Print)
class PrintAdmin(admin.ModelAdmin):
    list_display = ('title', 'in_stock', 'price')
    list_filter = ('in_stock', 'themes')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('themes',)

# Register the Print Model with the Admin site
@admin.register(Photography)
class PhotographyAdmin(admin.ModelAdmin):
    list_display = ('title', 'in_stock', 'price')
    list_filter = ('in_stock', 'themes')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('themes',)

# Register the Category Model with the Admin site
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'is_active')
    list_filter = ('type', 'is_active')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

# Register the Product Model with the Admin site
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'format', 'price', 'stock', 'sku', 'is_active')
    list_filter = ('format', 'is_active')
    search_fields = ('title', 'sku')
    prepopulated_fields = {'slug': ('title',)}

# Register the Order Model with the Admin site
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_email', 'total_price', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('customer_name', 'customer_email')


# Register the CartItem Model with the Admin site
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')

# Register the ContactSubmission Model with the Admin site
@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    readonly_fields = ('submitted_at', 'ip_hash', 'user_agent')
    search_fields = ('name', 'email', 'message')

