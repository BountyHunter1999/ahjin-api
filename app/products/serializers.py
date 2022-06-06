from rest_framework import serializers
from .models import Product, Review

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id',]

    # def create(self, validated_data):
    #     """
    #     Create and return a new Product instance, given a validated data
    #     """
    #     return Product.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing Product instance, given the validated data
    #     """
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.price_m = validated_data.get('price_m', instance.price_m)
    #     instance.price_a = validated_data.get('price_a', instance.price_a)
    #     instance.unique_feature = validated_data.get('unique_feature', instance.unique_feature)
    #     instance.created_at = validated_data.get('created_at', instance.created_at)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.cat = validated_data.get('cat', instance.cat)
    #     instance.d_cat = validated_data.get('d_cat', instance.d_cat)
    #     instance.rating = validated_data.get('rating', instance.rating)
    #     instance.discount = validated_data.get('discount', instance.discount)
    #     instance.save()
    #     return instance
