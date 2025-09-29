# shop views
from django.shortcuts import render, get_object_or_404
from .models import Print, Theme
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator # For pagination

#Homepage view
def homepage(request):
    login_url = reverse('login')  # URL for the login page
    return render(request, 'shop/homepage.html', {'login_url': login_url})

# Illustration gallery view
# def illustration_gallery(request):
#     prints = Print.objects.filter(type='illustration', in_stock=True)
#     return render(request, 'shop/illustration_gallery.html', {'prints': prints})
def illustration_gallery(request):
    prints = Print.objects.filter(type='illustration', in_stock=True)
    paginator = Paginator(prints, 20)  # 20 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/illustration_gallery.html', {'page_obj': page_obj})


# Photography gallery view
def photography_gallery(request):
    prints = Print.objects.filter(type='photo', in_stock=True)
    paginator = Paginator(prints, 20)  # 20 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/photography_gallery.html', {'page_obj': page_obj})

# Theme filter view with optional category
def theme_filter(request):
    slug = request.GET.get('theme')
    category = request.GET.get('type')  # 'illustration' or 'photography'
    theme = get_object_or_404(Theme, slug=slug)

    prints = Print.objects.filter(themes=theme)

    if category == 'illustration':
        prints = prints.filter(type='illustration')
        template = 'shop/illustration_gallery.html'
    elif category == 'photography':
        prints = prints.filter(type='photo')
        template = 'shop/photography_gallery.html'
    else:
        template = 'shop/theme_filtered_gallery.html'

    return render(request, template, {
        'prints': prints,
        'theme': theme,
        'category': category
    })


def add_to_cart(request):
    product_id = request.POST.get('product_id')
    cart = request.session.get('cart', [])
    cart.append(product_id)
    request.session['cart'] = cart
    return JsonResponse({'status': 'added'})
