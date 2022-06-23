import re
from rest_framework import serializers
from .models import Product, Review

class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id',]
    
    def get_reviews(self, obj):
        reviews = obj.review_set.all() # reviews ma product parent xa tyo parent ho obj
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data

class ReviewSerializer(serializers.ModelSerializer):
    # reviews = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        # read_only_fields = ['id', '']

    