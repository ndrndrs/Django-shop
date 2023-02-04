from django.db import models
from django.shortcuts import reverse
from categories.models import Category

# Create your models here.

class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    product_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    product_description = models.TextField(max_length=600, blank=True)
    price = models.FloatField()
    old_price = models.FloatField(null=True)
    image = models.ImageField(upload_to='photos/products')
    quantity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def image_img(self):
        if self.image:
            from django.utils.safestring import mark_safe
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(self.image.url))
        else:
            return 'No image'

    image_img.short_description = 'Main Image'
    image_img.allow_tags = True

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
