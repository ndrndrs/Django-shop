from django.shortcuts import render, redirect
from django.http import HttpResponse
from products.models import Product
from .models import Cart, Item


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
    # return HttpResponse(cart_item.product) check add


def remove_from_cart(request, product_id):

    cart = Cart.objects.get(cart_id=_cart_session_id(request))
    product = Product.objects.get(id=product_id)
    cart_item = Item.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None, tax=0):
    try:
        cart = Cart.objects.get(cart_id=_cart_session_id(request))
        cart_items = Item.objects.filter(cart=cart, is_available=True)

        for item in cart_items:
            total += item.product.price * item.quantity
            quantity += item.quantity
        tax = round((5 * total) / 100, 2)
        tax_total = round(total + tax, 2)
    except Exception:
        ...
    total = round(total, 2)
    context = {
        'tax': tax,
        'total': total,
        'quantity': quantity,
        'tax_total': tax_total,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)
