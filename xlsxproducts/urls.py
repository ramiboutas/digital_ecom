from django.urls import path, include

from .views import XlsxProductListView, XlsxProductDetailView

app_label = 'xlsxproducts'

urlpatterns = [
    path('', XlsxProductListView.as_view(), name='list'),
    path('<slug:slug>/', XlsxProductDetailView.as_view(), name='detail'),

]
