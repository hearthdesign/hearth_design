# shop/forms.py
from django import forms
from .models import Print

class PrintForm(forms.ModelForm):
    class Meta:
        model = Print
        fields = ['title', 'image', 'price', 'type', 'in_stock', 'themes', 'category', 'description']  

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your message', 'rows': 5})
    )
    website = forms.CharField(required=False, widget=forms.HiddenInput)  # Honeypot
