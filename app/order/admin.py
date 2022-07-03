from django.contrib import admin

# Register your models here.
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'total_product', 'paid_with', 'product_delivered', 
                    'createdAt', 'updatedAt')


admin.site.register(Order, OrderAdmin)