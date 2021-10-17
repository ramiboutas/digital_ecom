import stripe
from django.shortcuts import render
from django.views import View
from django.conf import settings


stripe.api_key = settings.STRIPE_PUBLIC_KEY


class CreateCheckoutSessionView(View):
    def post(self, request, pk, *args, **kwargs):
        try:
            print(pk)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # TODO: replace this with the `price` of the product you want to sell
                        'price': '{{PRICE_ID}}',
                        'quantity': 1,
                    },
                ],
                payment_method_types=[
                  'card',
                  'sofort',
                ],
                mode='payment',
                success_url = request.get_host() + '/success/',
                cancel_url = request.get_host() + '/cancel/',
            )
        except Exception as e:
            return str(e)
        return redirect(checkout_session.url, code=303)
