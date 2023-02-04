from django.urls import path
from .views import cart, add_to_cart


urlpatterns = [
    path('', cart, name='cart'),
    path('add_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
]