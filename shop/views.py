# shop views
from django.shortcuts import render, get_object_or_404
from .models import Print, Theme
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator # For pagination
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

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

def cart_view(request):
    cart_ids = request.session.get('cart', [])
    items = Print.objects.filter(id__in=cart_ids)
    return render(request, 'shop/cart.html', {'items': items})

def create_checkout_session(request, product_id):
    product = get_object_or_404(Print, id=product_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {'name': product.title},
                'unit_amount': int(product.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/success/',
        cancel_url='http://127.0.0.1:8000/cancel/',
    )
    return redirect(session.url)