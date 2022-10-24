from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from store.models import Product
from category.models import Category
from carts.models import CartItem, Cart
from eStore.utils import _get_cart_id
from django.core.paginator import Paginator
from django.db.models import Q


class StoreListView(ListView):
    paginate_by = 5
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
        self.products = self.products.order_by('-id')
        products = Paginator(self.products, self.paginate_by)
        product_count = self.products.count()
        page = self.request.GET.get('page', 1)
        context['products'] = products.get_page(page)
        context['page_ob'] = products.get_page(page)
        context['product_count'] = product_count
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


class SearchStoreListView(ListView):
    paginate_by = 5
    model = Product
    template_name = 'store/store.html'
    products = Product.objects.all().filter(is_available=True)

    # all_categories = Category.objects.all()

    def get(self, request, *args, **kwargs):
        category_slug = self.kwargs.get('slug')
        if category_slug:
            categories = get_object_or_404(Category, slug=category_slug)
            self.products = self.products.filter(category=categories)

        # handle search
        query = request.GET.get('q')
        if query:
            self.products = self.products.filter(Q(product_name__icontains=query) | Q(description__icontains=query))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.products = self.products.order_by('-id')
        products = Paginator(self.products, self.paginate_by)
        product_count = self.products.count()
        page = self.request.GET.get('page', 1)
        context['products'] = products.get_page(page)
        context['page_ob'] = products.get_page(page)
        context['product_count'] = product_count
        # context['categories'] = self.all_categories
        return context
