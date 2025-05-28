# urls.py

"""Presentation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from unicodedata import name

from django.contrib import admin
from django.urls import path,include

from django.contrib.auth.views import LoginView, logout_then_login
from Domain.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', mainPage, name='mainPage'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('cart/', cart_view, name='cart'),
    path('create_order/', create_order_without_payment, name='create_order_without_payment'),
    path('create_order_paid/', create_order, name='create_order'),
    path('contact/', contactPage, name='contact'),
    path('checkout/', checkoutPage, name='checkout'),
    path('services/', pagServicios, name='services'),
    path('my_orders/', my_orders, name='my_orders'),
    path('add_product/', addProduct, name='addProduct'),
    path('edit_product/<id>/', editProduct, name='editProduct'),
    path('product_list/', productList, name='productList'),
    path('delete_product/<id>/', deleteProduct, name='deleteProduct'),
    path('register/', register, name='register'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='Add'),
    path('increase/<int:product_id>/', increase_product, name='Sum'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='Del'),
    path('decrease/<int:product_id>/', decrease_product, name='Sub'),
    path('clear_cart/', clear_cart, name='CLS'),
    path('details/<id>/', productDetails, name='details'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

