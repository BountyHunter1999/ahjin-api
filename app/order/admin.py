from django.contrib import admin

# Register your models here.
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'user_name', 'paid_with', 'product_delivered', 
                    'createdAt', 'updatedAt')


admin.site.register(Order, OrderAdmin)