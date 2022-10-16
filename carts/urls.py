from django.urls import path
from carts import views

app_name = 'carts'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', views.AddToCartView.as_view(), name='add_cart'),
]
