from django.shortcuts import render
from products.models import Product

def homepage(request):
    products = Product.objects.all().filter(is_available=True)
    context = {
        'products': products
    }
    return render(request, 'homepage.html', context)
