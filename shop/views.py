# shop views
from django.shortcuts import render, get_object_or_404
from .models import Print, Theme
from django.urls import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator # For pagination
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import PrintForm

stripe.api_key = settings.STRIPE_SECRET_KEY

#Homepage view
def homepage(request):
    login_url = reverse('login')  # URL for the login page
    return render(request, 'shop/homepage.html', {'login_url': login_url})

# Form for uploading prints
@login_required
def upload_print(request):
    if request.method == 'POST':
        form = PrintForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('illustration_gallery')  
    else:
        form = PrintForm()
    return render(request, 'shop/upload.html', {'form': form})

# Illustration gallery view
def illustration_gallery(request):
    prints = Print.objects.filter(type='illustration', in_stock=True)
    paginator = Paginator(prints, 20)  # 20 items per page
    page_number = request.GET.get('page')  # get current page number
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

# only logged-in users can access cart and checkout routes
# Require user to be logged in to access this view
@login_required
def add_to_cart(request):
    
    product_id = request.POST.get('product_id')  # Get the product ID
    # Get the quantity default to 1
    quantity = int(request.POST.get('quantity', 1))  
    # Retrieve the current cart from the session, or initialize an empty dict
    cart = request.session.get('cart', {})

    # If the product is already in the cart, increase its quantity
    if product_id in cart:
        cart[product_id] += quantity
    else:
        # Otherwise, add it with the selected quantity
        cart[product_id] = quantity
    # Save the updated cart back into the session
    request.session['cart'] = cart
    # Mark the session as modified to ensure Django saves it
    request.session.modified = True
    # Redirect the user to the cart view page
    return redirect('cart_view')

# Require user to be logged in to view their cart
@login_required
def cart_view(request):
    # Get the cart dictionary from the session
    cart = request.session.get('cart', {})
    # Fetch all Print objects whose IDs are in the cart
    items = Print.objects.filter(id__in=cart.keys())
    # Prepare a list of cart items with quantity and total price
    cart_items = []
    for item in items:
        cart_items.append({
            'product': item,  # The Print object
            'quantity': cart[str(item.id)],  # Quantity from session
            'total': item.price * cart[str(item.id)],  # Total cost
        })

    # Render the cart template with the cart_items context
    return render(request, 'shop/cart.html', {'cart_items': cart_items})


@login_required
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