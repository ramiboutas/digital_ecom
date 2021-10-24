from django.urls import path, include
from .views import add_to_cart_view, show_cart_view, remove_from_cart_view

app_label = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', add_to_cart_view, name='add-to-cart'),
    path('remove/<int:item_id>/', remove_from_cart_view, name='remove-from-cart'),
    path('', show_cart_view, name='show-cart'),
]
