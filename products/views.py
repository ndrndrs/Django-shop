from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Product
from categories.models import Category
from clothes_cart.models import Cart, Item
from clothes_cart.views import _cart_session_id


def store(request, category_slug=None):
    category_products = None
    products = None

    if category_slug != None:
        category_products = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=category_products, is_available=True)
        product_count = products.count()
        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        product_count = products.count()
        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        item_in_cart = Item.objects.filter(cart__cart_id=_cart_session_id(request), product=single_product).exists()


    except Exception as e:
        raise e
    context = {
        'single_product': single_product,
        'item_in_cart': item_in_cart,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    context = {}
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-create_date').filter(Q(product_name__icontains=keyword) | Q(product_description__icontains=keyword))

        if products:
            context = {
                'products': products,
                'product_count': products.count,
            }

    return render(request, 'store/store.html', context)
