from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from store import views

urlpatterns = [
    path('', views.StoreListView.as_view(), name='store'),
]
