from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView


from .models import Product
from .forms import ProductAddToCartForm

class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'

    def get(self, request, *args, **kwargs):
        # demo for setting up session keys
        num_visits = request.session.get('num_visits', 0)
        request.session['num_visits'] = num_visits + 1
        print(f'num_visits = {num_visits}')
        return super().get(request, *args, **kwargs)


class ProductDetailView(DetailView):
    model = Product
    # form_class = ProductAddToCartForm
    template_name = 'products/detail.html'
