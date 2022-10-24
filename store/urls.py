from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from store import views

app_name = 'store'

urlpatterns = [
    path('', views.StoreListView.as_view(), name='store'),
    path('category/<slug:slug>/', views.StoreListView.as_view(), name='products_by_category'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('search/', views.SearchStoreListView.as_view(), name='search_results'),
]
