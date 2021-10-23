from django.urls import path, include

from .views import (CreateProductCheckoutSessionView,
                    ProductSuccessView,
                    ProductCancelView,
                    StripePaymentProductIntentView,
                    stripe_webhook)


app_label = 'payment'

urlpatterns = [
    path('create-product-checkout-session/<slug:slug>/', CreateProductCheckoutSessionView.as_view(), name='create-product-checkout-session'),
    path('create-product-payment-intent/<slug:slug>/', StripePaymentProductIntentView.as_view(), name='create-product-payment-intent'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('sucess/', ProductSuccessView.as_view(), name='sucess'),
    path('cancel/', ProductCancelView.as_view(), name='cancel'),
]
