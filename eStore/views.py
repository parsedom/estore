from django.shortcuts import render
from django.views.generic import ListView
from store.models import Product


class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    products = Product.objects.all().filter(is_available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.products
        return context


def home(request):
    return render(request, 'home.html')
