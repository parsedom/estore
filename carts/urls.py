from django.urls import path
from carts import views

app_name = 'carts'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', views.AddToCartView.as_view(), name='add_cart'),
    path('remove/<int:product_id>/', views.RemoveFromCartView.as_view(), name='remove_cart'),
    path('update_cart/<int:cart_id>/<str:action>/<int:quantity>', views.UpdateCartItemQuantityView.as_view(),
         name='update_cart'),
]
