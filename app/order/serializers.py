from dataclasses import field
from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Order
        fields =  ["user", "quantity", "paymentMethod",
                   "delivered", "total", "createdAt",
                   "updatedAt", "username", "email"]
        
        