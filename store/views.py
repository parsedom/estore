from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from store.models import Product
from category.models import Category
from carts.models import CartItem, Cart
from eStore.utils import _get_cart_id


class StoreListView(ListView):
    model = Product
    template_name = 'store/store.html'
    products = Product.objects.all().filter(is_available=True)

    # all_categories = Category.objects.all()

    def get(self, request, *args, **kwargs):
        category_slug = self.kwargs.get('slug')
        if category_slug:
            categories = get_object_or_404(Category, slug=category_slug)
            self.products = self.products.filter(category=categories)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.products
        # context['categories'] = self.all_categories
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    # context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        in_cart = CartItem.objects.filter(cart__cart_id=_get_cart_id(self.request), product=product).exists()
        context['in_cart'] = in_cart
        return context
