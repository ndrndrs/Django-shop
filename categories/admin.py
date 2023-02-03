from django.contrib import admin
from .models import Category

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('cat_name', )}
    list_display = [
        'cat_name', 'slug', 'cat_image', 'short_description'
    ]

admin.site.register(Category, CategoryAdmin)

