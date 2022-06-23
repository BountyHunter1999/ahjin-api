from django.contrib import admin

# Register your models here.
from .models import Product, Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'user_name', 'product_rating')

class ProductAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product)
admin.site.register(Review, ReviewAdmin)
