# shop/forms.py
from django import forms
from .models import Print

class PrintForm(forms.ModelForm):
    class Meta:
        model = Print
        fields = ['title', 'image', 'price', 'type', 'in_stock', 'themes', 'category', 'description']  