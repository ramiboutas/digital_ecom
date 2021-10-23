

from django.db import models
from django.urls import reverse

from products.models import Product


class Cart(models.Model):
    cart_id = models.CharField(max_length=50, help_text='This is a cookie value') # use uuid4!!,m

class Item(models.Model):
    cart = models.ForeignKey(Cart, null=True, blank=True, related_name='items', on_delete=models.CASCADE)
    cart_id = models.CharField(max_length=50, help_text='This is a cookie value')
    date_added = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, unique=False, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date_added']

    def __str__(self):
        return f'{self.product.id} {self.title} (cart_id: {self.cart_id})'

    @property
    def title(self):
        return self.product.title

    @property
    def price(self):
        return self.product.price

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def remove_from_cart_url(self):
        return reverse('cart:remove-from-cart', kwargs={'item_id': self.id})
