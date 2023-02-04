from django.shortcuts import render, redirect
from products.models import Product
from .models import Cart, Item


# Create your views here.

class DoesNotExist(Exception):
    ...


def _cart_session_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_session_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_session_id(request)
        )
        cart.save()
    try:
        cart_item = Item.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except Item.DoesNotExist:
        cart_item = Item.objects.create(
            product=product,
            cart=cart,
            quantity=1,
        )
        cart_item.save()
    return redirect('cart')


def cart(request):
    return render(request, 'store/cart.html')
