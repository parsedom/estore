from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.views import View

from carts.models import Cart, CartItem
from store.models import Product
from category.models import Category


class CartDetailView(TemplateView):
    model = Cart
    template_name = 'store/cart.html'
    # products = Cart.objects.all().filter(is_available=True)

    # all_categories = Category.objects.all()

    # def get(self, request, *args, **kwargs):
    #     category_slug = self.kwargs.get('slug')
    #     if category_slug:
    #         categories = get_object_or_404(Category, slug=category_slug)
    #         self.products = self.products.filter(category=categories)
    #     return super().get(request, *args, **kwargs)
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['products'] = self.products
    #     # context['categories'] = self.all_categories
    #     return context


class CartView(View):
    model = Cart
    # template_name = 'store/cart.html'
    fields = ['quantity']


# class AddToCartView(TemplateView):
#     model = Cart
#     template_name = 'store/cart.html'
#     fields = ['quantity']
#
#     def get(self, request, *args, **kwargs):
#         product_id = self.kwargs.get('product_id')
#         product = Product.objects.get(id=product_id)
#         try:
#             cart = Cart.objects.get(cart_id=self._get_cart_id(request))
#         except Cart.DoesNotExist:
#             cart = Cart.objects.create(
#                 cart_id=self._get_cart_id(request)
#             )
#             cart.save()
#
#         try:
#             cart_item = CartItem.objects.get(product=product, cart=cart)
#             if cart_item.quantity < cart_item.product.stock:
#                 cart_item.quantity += 1
#             cart_item.save()
#         except CartItem.DoesNotExist:
#             cart_item = CartItem.objects.create(
#                 product=product,
#                 quantity=1,
#                 cart=cart
#             )
#             cart_item.save()
#
#         return super().get(request, *args, **kwargs)
#
#     def get_redirect_url(self):
#         return redirect('carts:cart_detail')
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context['products'] = self.products
#     #     return context
#
#     def _get_cart_id(self, request):
#         cart = request.session.session_key
#         if not cart:
#             cart = request.session.create()
#         return cart
#

def add_to_cart(request, *args, **kwargs):
    product_id = kwargs.get('product_id')
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_get_cart_id(request)
        )
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()

    return redirect('carts:cart_detail')


def _get_cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
