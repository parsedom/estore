from django.urls import path
from carts import views

app_name = 'carts'

urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart_detail'),
]
