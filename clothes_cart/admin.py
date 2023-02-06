from django.contrib import admin
from .models import Cart, Item
# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = [
        'cart_id', 'date_added'
    ]

class CartItem(admin.ModelAdmin):
    list_display = [
        'cart', 'product',  'quantity'
    ]

admin.site.register(Cart, CartAdmin)
admin.site.register(Item, CartItem)