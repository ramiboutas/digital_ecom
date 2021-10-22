from django.urls import path, include
from .views import (CreateProductCheckoutSessionView,
                    ProductSuccessView,
                    ProductCancelView,
                    StripePaymentProductIntentView,
                    stripe_webhook,
                    show_cart,
                    add_to_cart)


app_label = 'cart'

urlpatterns = [
    path('', show_cart, name='cart'),
    path('add/<int:id>/', add_to_cart, name='add-to-cart'),
    path('create-product-checkout-session/<slug:slug>/', CreateProductCheckoutSessionView.as_view(), name='create-product-checkout-session'),
    path('create-product-payment-intent/<slug:slug>/', StripePaymentProductIntentView.as_view(), name='create-product-payment-intent'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('sucess/', ProductSuccessView.as_view(), name='sucess'),
    path('cancel/', ProductCancelView.as_view(), name='cancel'),
]
