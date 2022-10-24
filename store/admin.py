from django.contrib import admin
from store.models import Product
from store.models import Variation


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'category', 'price', 'stock', 'modified_date', 'is_available']
    prepopulated_fields = {'slug': ('product_name',)}


class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation_category', 'variation_value', 'is_active']
    list_editable = ['is_active']
    list_filter = ['product', 'variation_category', 'variation_value']


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
