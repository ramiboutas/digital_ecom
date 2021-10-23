from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.conf import settings

from products.models import Product
from .models import Item
from .utils import get_or_generate_cart_id, generate_cart_id, get_cart_items

# change for cart_id as cookie
def add_to_cart_view(request, product_id):
    cart_id = get_or_generate_cart_id(request)
    added_product = get_object_or_404(Product, id=product_id)
    cart_products = get_cart_items(cart_id)
    response = HttpResponse(f'{added_product.title} was added to the cart')
    product_in_cart = False # firstly we supose that the product has not been added to the cart yet
    for cart_item in cart_products:
        if cart_item.product.id == added_product.id: # then we check if it was already added
            product_in_cart = True
            response = HttpResponse(f'{added_product.title} is already in your cart')
    if not product_in_cart:
        Item(product = added_product, cart_id = cart_id).save()
    response.set_cookie('cart_id', cart_id)
    return response

def remove_from_cart_view(request, item_id):
    # security checks
    # remove item
    print(request.method)
    if request.method == "DELETE":
        print("DELETE method")
    return HttpResponse(f"Item ID={item_id} removed from cart")


def show_cart_view(request):
    cart_id = get_or_generate_cart_id(request)
    context = {'object_list': get_cart_items(cart_id)}
    return render(request, 'cart/list.html', context)



# def add_to_cart_view(request, product_id):
#     cart_id = get_or_generate_cart_id(request)
#     added_product = get_object_or_404(Product, id=product_id)
#     cart_products = get_cart_items(cart_id)
#     response = HttpResponse(f'{added_product.title} was added to the cart')
#     product_in_cart = False # firstly we supose that the product has not been added to the cart yet
#     for cart_item in cart_products:
#         if cart_item.product.id == added_product.id: # then we check if it was already added
#             product_in_cart = True
#             response = HttpResponse(f'{added_product.title} is already in your cart')
#     if not product_in_cart:
#         Item(product = added_product, cart_id = cart_id).save()
#     response.set_cookie('cart_id', cart_id)
#     return response
