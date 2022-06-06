from math import prod
from os import stat
from rest_framework import viewsets, status #, mixins
from rest_framework.response import Response
from .models import Product, Review

from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):

    def list(self, request): # GET /api/products
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        # print(serializer)
        return Response(serializer.data)

    def create(self, request): # POST /api/products
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None): # /api/products/<str:id>
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        count = len(product)
        new_data = {"count": count}
        serializer = ProductSerializer(product)
        new_data.update(serializer.data)
        return Response(new_data)
    
    def update(self, request, pk=None): # /api/products/<str:id>
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None): # /api/products/<str:id>
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
