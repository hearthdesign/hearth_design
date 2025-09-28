from django.contrib import admin
from .models import Theme, Print

# Register the Theme Model with the admin site
@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

# Register the Print Model with the Admin site
@admin.register(Print)
class PrintAdmin(admin.ModelAdmin):
    list_display = ('title', 'in_stock')
    list_filter = ('in_stock', 'themes')
    search_fields = ('title', 'description')
