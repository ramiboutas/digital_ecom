import stripe
import json
import random
import decimal

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.conf import settings

from .models import Item
from products.models import Product

# helper function to generate a card_id (use it just in this module!)
def _generate_cart_id():
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id +=characters[random.randint(0, len(characters)-1)]
    return cart_id

# helper function to get item associated with a card_id
def get_cart_items(cart_id):
    return Item.objects.filter(cart_id=cart_id)


def add_to_cart(request, id):
    try:
        card_id = request.COOKIES['cart_id']
    except KeyError:
        card_id = _generate_cart_id()

    added_product = get_object_or_404(Product, id=id)
    cart_products = get_cart_items(card_id)
    response = HttpResponse(f'You added this product: {added_product.title}')
    # firstly we supose that the product has not been added to the cart yet
    product_in_cart = False
    # then we check if it was already added
    for cart_item in cart_products:
        if cart_item.product.id == added_product.id:
            product_in_cart = True
            response = HttpResponse(f'The product {added_product.title} has been already added to the cart')
    if not product_in_cart:
        Item(product = added_product, cart_id = card_id).save()
        # item.product = added_product
        # item.cart_id = card_id
        # item.save()
    response.set_cookie('cart_id', card_id)
    return response



def show_cart(request):
    context = {}
    return render(request, 'cart/cart.html', context)



    # p = get_object_or_404(Product, slug=product_slug)
    # cart_products = get_cart_items(request)
    # product_in_cart = False
    # for cart_item in cart_products:
    #     if cart_item.product.id == p.id:
    #         product_in_cart = True
    # if not product_in_cart:
    #     item = Item()
    #     item.product = p
    #     item.cart_id = _cart_id(request)
    #     item.save()


stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateProductCheckoutSessionView(View):
    def post(self, request, slug, *args, **kwargs):
        try:
            product = Product.objects.get(slug=slug)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # TODO: replace this with the `price` of the product you want to sell
                        'price': str(product.price),
                        'quantity': 1,
                    },
                ],
                payment_method_types=[
                  'card',
                  'sofort',
                ],
                metadata = {
                    'slug': slug
                },
                mode='payment',
                success_url = request.get_host() + reverse('cart:success'),
                cancel_url = request.get_host() + reverse('cart:cancel'),
            )
        except Exception as e:
            return str(e)
        return redirect(checkout_session.url, code=303)


class ProductSuccessView(TemplateView):
    template_name = 'cart/sucess.html'


class ProductCancelView(TemplateView):
    template_name = 'cart/cancel.html'

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        slug = session["metadata"]["slug"]

        product = Product.objects.get(slug=slug)

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
            recipient_list=[customer_email],
            from_email="matt@test.com"
        )

        # TODO - decide whether you want to send the file or the URL

    elif event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)
        customer_email = stripe_customer['email']
        slug = intent["metadata"]["slug"]
        product = Product.objects.get(slug=slug)

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
            recipient_list=[customer_email],
            from_email="rami@test.com"
        )

    return HttpResponse(status=200)


class StripePaymentProductIntentView(View):
    def post(self, request, slug, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            product = Product.objects.get(slug=slug)
            intent = stripe.PaymentIntent.create(
                amount=product.price,
                currency='usd',
                customer=customer['id'],
                metadata={
                    "product_id": product.id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({ 'error': str(e) })
