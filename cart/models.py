from django.db import models
from products.models import Product


class Item(models.Model):
    cart_id = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, unique=False, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date_added']

    def title(self):
        return self.product.title

    def price(self):
        return self.product.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()


class Cart(models.Model):
    pass
