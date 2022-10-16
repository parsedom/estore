from django.contrib import admin
from store.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'category', 'price', 'stock', 'modified_date', 'is_available']
    prepopulated_fields = {'slug': ('product_name',)}


admin.site.register(Product, ProductAdmin)
