import random

from django.db import models
from django.urls import reverse
from django.shortcuts import get_object_or_404

from products.models import Product


def generate_cookie_value():
    cookie_value = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cookie_value_length = 50
    for y in range(cookie_value_length):
        cookie_value +=characters[random.randint(0, len(characters)-1)]
    return cookie_value


class Cart(models.Model):
    # cookie = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cookie_value = models.CharField(default=generate_cookie_value(), max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cookie_value

    def get_cart_items(self):
        return self.items.all()

    class Meta:
        ordering = ['created_at']


class Item(models.Model):
    cart = models.ForeignKey(Cart, null=True, blank=True, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, unique=False, on_delete=models.CASCADE)

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


# helper function  get or  create a cart
def get_or_create_cart(request):
    try:
        cart_cookie_value = request.COOKIES['cart_id'] # get the cookie from the request object
    except KeyError:
        # if it does not exist, create new one
        cart = Cart()
        cart.save()
        return cart
    cart = get_object_or_404(Cart, cookie_value=cart_cookie_value)
    return cart
