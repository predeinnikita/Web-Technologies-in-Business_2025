# views.py

import stripe
from django.contrib.auth.decorators import login_required
from django.db import transaction
from locale import currency
from re import template
from django.conf import settings

from django.http import HttpResponse
from django.http import HttpRequest

from django.shortcuts import render, redirect
from Domain.models import Product, Order, OrderDetail
from Domain.Cart import Cart
from Domain.forms import ProductForm

from django.contrib import messages
from django.contrib.auth.models import User
from .forms import *

from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
import requests
import json

def mainPage(request):
    products = Product.objects.all()
    return render(request, "index.html", { 'products': products })

def contactPage(request):
    return render(request, "contact.html")
    
def checkoutPage(request):
    cart = Cart(request)
    cart_items = []
    total_cart = 0
    for key, value in cart.cart.items():
        subtotal = float(value['price']) * value['quantity']
        total_cart += subtotal
        cart_items.append({
            'product_id': value['product_id'],
            'name': value['name'],
            'price': value['price'],
            'quantity': value['quantity'],
            'subtotal': subtotal,
        })

    return render(request, "checkout.html", {
        'cart_items': cart_items,
        'total_cart': total_cart,
    })


def pagServicios(request):
    return render(request, "servicios.html", {})

def productDetails(request, id):
    product = Product.objects.get(id=id)

    return render(request, "details.html",  {'form': product})


def addProduct(request):
    data = {
        'form': ProductForm()
    }
    if request.method == "POST":
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            data["message"] = "Product added successfully"
            messages.success(request, "Product added successfully!")
        else:
            data["message"] = "Failed to add product"
            messages.error(request, "Failed to add product.")

    return render(request, "product_add.html", data)


def editProduct(request, id):
    product = Product.objects.get(id=id)

    data = {
        'form': ProductForm(instance=product)
    }
    if request.method == "POST":
        form = ProductForm(
            data=request.POST, instance=product, files=request.FILES)
        if form.is_valid():
            form.save()
            data["message"] = "Product updated successfully"
            messages.success(request, "Product updated successfully!")
        else:
            data["message"] = "Failed to update product"
            messages.error(request, "Failed to update product.")

        data["form"] = ProductForm(
            instance=Product.objects.get(id=id)) # Обновляем форму после сохранения

    return render(request, "editProduct.html", data)


def deleteProduct(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect(to="productList")


def productList(request):
    products = Product.objects.all()

    data = {
        'products': products
    }
    return render(request, "product_list.html", data)


def cart_view(request):
    return render(request, "cart.html", {} )


def add_to_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.add(product)
    messages.success(request, f"'{product.name}' added to cart")
    return redirect(to="mainPage")


def increase_product(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.add(product)
    messages.info(request, f"Quantity of '{product.name}' increased.")
    return redirect("cart")


def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.remove(product)
    messages.warning(request, f"'{product.name}' removed from cart.")
    return redirect("cart")


def decrease_product(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.subtract(product)
    messages.info(request, f"Quantity of '{product.name}' decreased.")
    return redirect("cart")


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, "Cart cleared.")
    return redirect("cart")


@login_required
@transaction.atomic
def create_order_without_payment(request):
    if request.method == 'POST':
        cart = Cart(request)

        if not cart.cart.items():
            messages.error(request, "Your cart is empty. Cannot create order.")
            return redirect('cart')

        try:
            order = Order.objects.create(
                user=request.user,
                total=0
            )

            for key, value in cart.cart.items():
                product_id = int(key)
                try:
                    original_product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    original_product = None

                OrderDetail.objects.create(
                    order=order,
                    product=original_product,
                    product_name=value['name'],
                    unit_price=value['price'],
                    quantity=value['quantity']
                )

            cart.clear()
            messages.success(request, "Your order has been successfully created! Confirmation has been sent to your email.")
            return redirect('my_orders')

        except Exception as e:
            messages.error(request, f"An error occurred while creating the order: {e}")
            return redirect('cart')
    else:
        messages.error(request, "Invalid request method for creating an order.")
        return redirect('cart')

def send_email(mail, request):
    context = {
        'mail': mail,
        'cart_items': request.session.get('cart', {}).items(),
        'total_cart': request.session.get('total_cart', 0)
    }
    template = get_template('email.html')
    content = template.render(context, request)
    email = EmailMultiAlternatives(
        'Purchase receipt',
        'Order it now!',
        settings.EMAIL_HOST_USER,
        [mail]
    )

    email.attach_alternative(content, 'text/html')
    email.send()


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'User {username} created')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'register.html', context)
    
    
@login_required
@transaction.atomic
def create_order(request):
    if request.method == 'POST':
        cart = Cart(request)

        if not cart.cart.items():
            messages.error(request, "Your cart is empty.")
            return redirect('cart')

        try:
            order = Order.objects.create(
                user=request.user,
                total=cart.total_cart
            )

            for key, value in cart.cart.items():
                product_id = int(key)
                try:
                    original_product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    original_product = None

                OrderDetail.objects.create(
                    order=order,
                    product=original_product,
                    product_name=value['name'],
                    unit_price=value['price'],
                    quantity=value['quantity']
                )
            cart.clear()
            messages.success(request, "Your order has been successfully created!")
            return redirect('mainPage')

        except Exception as e:
            messages.error(request, f"An error occurred while creating the order: {e}")
            return redirect('cart')
    else:
        messages.error(request, "Invalid request method for creating an order.")
        return redirect('cart')

from django.contrib.auth.decorators import login_required

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, 'my_orders.html', context)

