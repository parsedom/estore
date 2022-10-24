import decimal

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.views import View

from carts.models import Cart, CartItem
from store.models import Product
from category.models import Category

from eStore.utils import _get_cart_id


class CartView(TemplateView):
    model = Cart
    template_name = 'store/cart.html'
    fields = ['quantity']
    context_object_name = 'cart'
    tax = decimal.Decimal(0.02)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            cart = Cart.objects.get(cart_id=_get_cart_id(self.request))
            all_items = CartItem.objects.filter(is_active=True, cart=cart)
            context['cart_items'] = all_items
            context['total_price_before_tax'] = round(sum(item.sub_total() for item in all_items), 2)
            context['total_tax'] = round(sum(item.sub_total() * self.tax for item in all_items), 2)
            context['total_price_after_tax'] = context['total_price_before_tax'] + context['total_tax']
            context['cart_size'] = all_items.count()
        except ObjectDoesNotExist:
            pass
        return context


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


class AddToCartView(TemplateView):
    # model = Cart

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        color = request.GET.get('color')
        size = request.GET.get('size')
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

    def post(self, request, *args, **kwargs):
        breakpoint()
        product_id = kwargs.get('product_id')
        color = request.POST.get('color')
        size = request.POST.get('size')
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


class RemoveFromCartView(TemplateView):

    def get(self, request, *args, **kwargs):
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
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass

        return redirect('carts:cart_detail')


class UpdateCartItemQuantityView(TemplateView):
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        action = kwargs.get('action', 'add')
        quantity = kwargs.get('quantity', 1)
        product = get_object_or_404(Product, id=product_id)

        try:  # TODO
            cart = Cart.objects.get(cart_id=_get_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_get_cart_id(request)
            )
            cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            if cart_item.quantity >= 1 and action == 'remove' and cart_item.quantity <= quantity:
                cart_item.delete()

            elif cart_item.quantity >= 1 and action == 'remove' and cart_item.quantity > quantity:
                cart_item.quantity -= quantity
                cart_item.save()

            elif action == 'add':
                total_addable = product.stock - cart_item.quantity
                if total_addable > quantity:
                    cart_item.quantity += quantity
                else:
                    cart_item.quantity += total_addable

                cart_item.save()
        except CartItem.DoesNotExist:
            pass

        return redirect('carts:cart_detail')
