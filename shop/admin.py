from django.contrib import admin
from .models import Theme, Print

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

@admin.register(Print)
class PrintAdmin(admin.ModelAdmin):
    list_display = ('title', 'available')
    list_filter = ('available', 'themes')
    search_fields = ('title', 'description')
