from django.contrib import admin

# Register your models here.
from .models import Product, Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'user_name', 'product_rating')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price_m', 'price_a', 'updated', 'featured', 'count')

admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
