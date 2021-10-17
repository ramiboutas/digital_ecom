from django.db import models


class CartAbstract(models.Model):
    pass


class CartItem(CartAbstract):
    pass


class Cart(CartAbstract):
    pass
