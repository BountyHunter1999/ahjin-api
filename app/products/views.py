import email
from rest_framework import viewsets, status #, mixins
from rest_framework.response import Response
from .models import Product, Review

from django.contrib.auth import get_user_model as User
from django.shortcuts import get_object_or_404

from .serializers import ProductSerializer

from rest_framework.permissions import IsAuthenticated, IsAdminUser


USER_REQUEST = ['list', 'retrieve']
ADMIN_REQUEST = ['create', 'update', 'partial_update', 'destroy']

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

        # superusers = User.objects
        # print(User().objects.filter(is_superuser=True)[0].ahjin_coin)
        # print(superusers)
        # print(request)
        try:
            product = Product.objects.get(pk=pk)
            self.check_object_permissions(request, product)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        count = len(product)
        new_data = {"count": count}
        serializer = ProductSerializer(product)
        new_data.update(serializer.data)
        return Response(new_data)
    
    # def update(self, request, pk=None): # /api/products/<str:id>
    #     try:
    #         product = Product.objects.get(pk=pk)
    #         self.check_object_permissions(request, product)
    #     except Product.DoesNotExist:
    #         return Response({}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = ProductSerializer(instance=product, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def partial_update(self, request, pk=None): # /api/products/<str:id>
        try:
            product = Product.objects.get(pk=pk)
            self.check_object_permissions(request, product)
        except Product.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None): # /api/products/<str:id>
        try:
            product = Product.objects.get(pk=pk)
            self.check_object_permissions(request, product)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({"msg": "Product Removed"}, status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action in USER_REQUEST:
            permission_classes = [
                IsAuthenticated,
            ]
        # elif self.action in ADMIN_REQUEST:
        #     permission_classes = [
        #         IsAdminUser,
        #     ]
        else:
            permission_classes = [IsAdminUser,]

        return [permission() for permission in permission_classes]