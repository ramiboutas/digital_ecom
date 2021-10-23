import json
import stripe

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.conf import settings

from products.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateProductCheckoutSessionView(View):
    def post(self, request, slug, *args, **kwargs):
        try:
            product = get_object_or_404(Product, slug=slug)
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
