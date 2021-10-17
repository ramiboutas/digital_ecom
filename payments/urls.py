from django.urls import path, include

from .views import CreateCheckoutSessionView


app_label = 'payments'

urlpatterns = [
    path('create-checkout-session/<int:pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),

]
