from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from products.models import Product, Parameter
from .models import Cart, Item


def _cart_session_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_param = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Parameter.objects.get(product=product, category_param__iexact=key,
                                                  value_param__iexact=value)
                product_param.append(variation)
            except:
                ...
    try:
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.get(cart_id=_cart_session_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_session_id(request)
        )
        cart.save()

    check_item = Item.objects.filter(product=product, cart=cart).exists()
    if check_item:
        cart_item = Item.objects.filter(product=product, cart=cart)
        par_list = []
        id = []
        for item in cart_item:
            existing_variation = item.parameters.all()
            par_list.append(list(existing_variation))
            id.append(item.id)

        if product_param in par_list:
            idx = par_list.index(product_param)
            item_id = id[idx]
            item = Item.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            if len(product_param) > 0:
                cart_item.parameters.clear()
                cart_item.parameters.add(*product_param)
            cart_item.save()
    else:
        cart_item = Item.objects.create(
            product=product,
            cart=cart,
            quantity=1,
        )
        if len(product_param) > 0:
            cart_item.parameters.clear()
            cart_item.parameters.add(*product_param)
        cart_item.save()
    return redirect('cart')

    # return HttpResponse(cart_item.product) check add


def remove_item_from_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_session_id(request))
    product = Product.objects.get(id=product_id)
    cart_item = Item.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def delete_from_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_session_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = Item.objects.get(product=product, cart=cart)
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
    except ObjectDoesNotExist:
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
