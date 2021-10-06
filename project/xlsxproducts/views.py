from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import XlsxProduct


class XlsxProductListView(ListView):
    model = XlsxProduct
    template_name = 'xlsxproducts/list.html'


class XlsxProductDetailView(DetailView):
    model = XlsxProduct
    template_name = 'xlsxproducts/detail.html'
