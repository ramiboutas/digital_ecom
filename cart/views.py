from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.views.decorators.http import require_http_methods
from django.conf import settings

from products.models import Product
from .models import Item, Cart, get_or_create_cart


def add_to_cart_view(request, product_id):
    cart = get_or_create_cart(request)
    cart_items = cart.get_cart_items()
    added_product = get_object_or_404(Product, id=product_id)
    response = HttpResponse(f'{added_product.title} was added to the cart')
    product_in_cart = False # firstly we supose that the product has not been added to the cart yet
    for cart_item in cart_items:
        if cart_item.product.id == added_product.id: # then we check if it was already added
            product_in_cart = True
            response = HttpResponse(f'{added_product.title} is already in your cart')
    if not product_in_cart:
        new_cart_item = Item(cart=cart, product=added_product)
        new_cart_item.save()
    response.set_cookie('cart_id', cart.cookie_value)
    return response

@require_http_methods(["DELETE", "POST"])
def remove_from_cart_view(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(Item, id=item_id)
    if item in cart.get_cart_items():
        item.delete()
    return HttpResponse()


def show_cart_view(request):
    cart = get_or_create_cart(request)
    context = {'object_list':  cart.get_cart_items()}
    return render(request, 'cart/list.html', context)
