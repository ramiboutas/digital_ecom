import random
import decimal

from .models import Item


# helper function  get or  generate a cart_id (use it just in this module!)
def get_or_generate_cart_id(request):
    try:
        cart_id = request.COOKIES['cart_id'] # get the cookie cart_id from the request object
    except KeyError:
            cart_id = generate_cart_id() # generate one if it does not exist
    return cart_id


# helper function to generate a cart_id (use it just in this module!)
def generate_cart_id():
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id +=characters[random.randint(0, len(characters)-1)]
    return cart_id

# helper function to get item associated with a cart_id
def get_cart_items(cart_id):
    return Item.objects.filter(cart_id=cart_id)
    
