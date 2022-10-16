from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from store.models import Product
from category.models import Category


class StoreListView(ListView):
    model = Product
    template_name = 'store/store.html'
    products = Product.objects.all().filter(is_available=True)

    # all_categories = Category.objects.all()

    def get(self, request, *args, **kwargs):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            categories = get_object_or_404(Category, slug=category_slug)
            self.products = self.products.filter(category=categories)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.products
        # context['categories'] = self.all_categories
        return context
