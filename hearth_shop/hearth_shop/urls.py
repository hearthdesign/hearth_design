"""
URL configuration for hearth_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from shop import views
from django.conf import settings
from django.conf.urls.static import static
from shop.views import contact_view, signup
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),  # homepage view
    path('gallery/illustrations/', views.illustration_gallery, name='illustration_gallery'),
    path('gallery/photographies/', views.photography_gallery, name='photography_gallery'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('theme-filter/', views.theme_filter, name='theme_filter'), # Theme filter view
    path('gallery/filter/', views.theme_filter, name='theme_filter'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/<int:product_id>/', views.create_checkout_session, name='checkout'),
    path('static/', include('django.contrib.staticfiles.urls')),
    path('upload/', views.upload_print, name='upload_print'),
    path('contact/', contact_view, name='contact'),
    path('thank-you/', TemplateView.as_view(template_name='thank_you.html'), name='thank_you'),
    path('i18n/', include('django.conf.urls.i18n')), # enables set_language
    path('signup/', signup, name='signup'),  # User signup view
    path('accounts/', include('django.contrib.auth.urls')), # for login/logout/password reset
]

urlpatterns += i18n_patterns(
    path('', views.homepage, name='homepage'),
    path('gallery/illustrations/', views.illustration_gallery, name='illustration_gallery'),
    path('gallery/photographies/', views.photography_gallery, name='photography_gallery'),
    path('upload/', views.upload_print, name='upload_print'),
    # path('login/', views.login, name='login'),
    # path('password_reset/', views.password_reset, name='password_reset'),
    path('signup/', views.signup, name='signup'),
    path('cart/', views.cart_view, name='cart_view'),
    path('thank_you/', TemplateView.as_view(template_name='shop/thank_you.html'), name='thank_you'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('contact/', views.contact_view, name='contact_view'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)