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
    current_user = request.user
    product = Product.objects.get(id=product_id)  # get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Parameter.objects.get(product=product, category_param__iexact=key,
                                                      value_param__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = Item.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = Item.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.parameters.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = Item.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = Item.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.parameters.clear()
                    item.parameters.add(*product_variation)
                item.save()
        else:
            cart_item = Item.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.parameters.clear()
                cart_item.parameters.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    # If the user is not authenticated
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Parameter.objects.get(product=product, category_param__iexact=key,
                                                      value_param__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        try:
            cart = Cart.objects.get(cart_id=_cart_session_id(request))  # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_session_id(request)
            )
        cart.save()

        is_cart_item_exists = Item.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = Item.objects.filter(product=product, cart=cart)
            # existing_variations -> database
            # current variation -> product_variation
            # item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.parameters.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = Item.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = Item.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.parameters.clear()
                    item.parameters.add(*product_variation)
                item.save()
        else:
            cart_item = Item.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.parameters.clear()
                cart_item.parameters.add(*product_variation)
            cart_item.save()
        return redirect('cart')


def remove_item_from_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = Item.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_session_id(request))
            cart_item = Item.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def delete_from_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = Item.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_session_id(request))
        cart_item = Item.objects.get(product=product, cart=cart, id=cart_item_id)
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


def checkout(request, total=0, quantity=0, cart_items=None, tax=0):
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
    return render(request, 'store/checkout.html', context)