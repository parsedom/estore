from django.shortcuts import render
from django.views.generic import ListView

from store.models import Product


class StoreListView(ListView):
    model = Product
    template_name = 'store/store.html'
    products = Product.objects.all().filter(is_available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.products
        return context
