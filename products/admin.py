from django.contrib import admin
from .models import Product, Parameter


# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = [
        'category', 'product_name', 'price', 'quantity',
        'is_available', 'modified_date', 'image_img',
    ]
    list_display_links = [
        'product_name'
    ]
    readonly_fields = ['image_img', ]
    ordering = ('-category', )
    list_per_page = 35


class ParameterAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'category_param', 'value_param', 'created_date', 'is_available'
    )
    list_editable = ('is_available', )

    list_filter = (
        'product', 'category_param', 'value_param',
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Parameter, ParameterAdmin)
