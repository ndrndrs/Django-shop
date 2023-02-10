from django.urls import path
from .views import cart, add_to_cart, remove_item_from_cart, delete_from_cart


urlpatterns = [
    path('', cart, name='cart'),
    path('add_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('del_cart/<int:product_id>/', delete_from_cart, name='delete_from_cart'),
    path('rem_item/<int:product_id>/z', remove_item_from_cart, name='remove_item_from_cart'),
]