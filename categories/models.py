from django.db import models
from django.shortcuts import reverse
# Create your models here.


class Category(models.Model):
    cat_name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    cat_description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    @property
    def short_description(self):
        return self.cat_description if len(self.cat_description) < 35 \
            else (self.cat_description[:33] + "..")

    def get_url(self):
        return reverse('products_in_category', args=[self.slug])

    def __str__(self):
        return self.cat_name