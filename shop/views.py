from django.shortcuts import render
from .models import Print

# Illustration gallery view
def illustration_gallery(request):
    prints = Print.objects.filter(type='illustration', is_active=True)
    return render(request, 'shop/illustration_gallery.html', {'prints': prints})

# photography gallery view
def photography_gallery(request):
    prints = Print.objects.filter(type='photo', is_active=True)
    return render(request, 'shop/photography_gallery.html', {'prints': prints})