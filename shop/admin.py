# ==========================================
#            SHOP ADMIN REGISTRATION
# ==========================================

from django.contrib import admin

from .models import (
    Category,
    ContactSubmission,
    Print,
    Theme,
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
    list_display = ("title", "type", "format", "size", "price", "stock", "is_active")
    list_filter = ("type", "format", "is_active", "stock", "themes", "category")
    search_fields = ("title", "slug", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("title",)
    filter_horizontal = ("themes",)

# Register the ContactSubmission Model with the Admin site
@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "submitted_at", "marketing_consent")
    readonly_fields = ("submitted_at", "ip_hash", "user_agent")
    search_fields = ("name", "email", "message")
    list_filter = ("marketing_consent", "submitted_at")
    date_hierarchy = "submitted_at"
