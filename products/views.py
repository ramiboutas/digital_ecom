from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView


from .models import Product
from .forms import ProductAddToCartForm

class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'


class ProductDetailView(DetailView):
    model = Product
    # form_class = ProductAddToCartForm
    template_name = 'products/detail.html'
