from django.urls import path
from carts import views

app_name = 'carts'

urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_cart'),
]
