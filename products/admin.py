from django.contrib import admin
from .models import Product


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = [
        'category', 'product_name', 'price', 'quantity', 'is_available', 'modified_date', 'image', 'image_img'
    ]
    list_display_links = [
        'product_name'
    ]
    readonly_fields = ['image_img', ]
    ordering = ('-category', )
    list_per_page = 35


admin.site.register(Product, ProductAdmin)
