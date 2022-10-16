from django.db import models
from category.models import Category
from django.urls import reverse


class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    # image_url = models.CharField(max_length=2083)
    image = models.ImageField(upload_to='photos/products/', blank=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # class Meta:
    #     db_table = 'Product'

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('store:product_detail', args=[self.slug])
