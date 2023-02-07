from django.db import models
from products.models import Product, Parameter


# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=100, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    parameters = models.ManyToManyField(Parameter, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def product_total_price(self):
        total = round(self.quantity * self.product.price, 2)
        return total

    def __unicode__(self):
        return self.product
