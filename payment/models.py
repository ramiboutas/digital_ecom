from django.db import models
from django.contrib.auth import get_user_model

from cart.models import Cart

User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, related_name='orders', on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, )
