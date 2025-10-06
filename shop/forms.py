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
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    website = forms.CharField(required=False, widget=forms.HiddenInput)