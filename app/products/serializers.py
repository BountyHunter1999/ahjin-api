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
    # user_data = serializers.ForeignKeyRealatedField(source='user.id', read_only=True)
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    # username = serializers.CharField(max_length=255)
    # email = serializers.EmailField(max_length=255)
    # username = serializers.SlugRelatedField(slug_field='username', read_only=True)
    # email = serializers.SlugRelatedField(slug_field='email', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'rating', 'comment',
                  'product', 
                  'createdAt', 'updatedAt',
                  'user')
                #   'username', 'email', )
        # fields = '__all__'
        # read_only_fields = ['id', '']
    
    