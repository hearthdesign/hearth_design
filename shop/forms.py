# shop/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Print, Review


class PrintForm(forms.ModelForm):
    class Meta:
        model = Print
        fields = [
            "title",
            "image",
            "price",
            "type",
            "stock",
            "themes",
            "category",
            "description",
        ]


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label=_("Name"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Your name")}
        ),
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": _("Your email")}
        ),
    )
    message = forms.CharField(
        label=_("Message"),
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": _("Your message"), "rows": 5}
        ),
    )
    website = forms.CharField(required=False, widget=forms.HiddenInput)  # Honeypot
    privacy_agree = forms.BooleanField(
        label=_("I have read and agree to the Privacy Notice"), required=True
    )
    marketing_consent = forms.BooleanField(
        label=_(
            "I would like to receive updates about new art, offers, and newsletters"
        ),
        required=False,
    )


class ReviewForm(forms.ModelForm):
    # Honeypot field: real users won't see or fill this out
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"autocomplete": "off", "tabindex": "-1"}),
    )

    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(attrs={"class": "form-control"}),
            "comment": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Write your thoughts on this print..."}
            ),
        }

    def clean_website(self):
        """If a bot fills out this hidden field, throw a validation error."""
        website = self.cleaned_data.get("website")
        if website:
            raise forms.ValidationError("Spam detected.")
        return website


class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
