from ast import Or
from django.shortcuts import render
from rest_framework import viewsets, status

from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer


from rest_framework.permissions import IsAuthenticated, IsAdminUser


USER_REQUEST = ['list', 'create']
ADMIN_REQUEST = ['update', 'partial_update', 'destroy']


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def list(self, request): 
        orders = Order.objects.all()

        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)
    
    def create(self, request):
        self.check_object_permissions(request, request.data)
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None): # /api/products/<str:id>

        # superusers = User.objects
        # print(User().objects.filter(is_superuser=True)[0].ahjin_coin)
        # print(superusers)
        # print(request)
        try:
            order = Order.objects.get(pk=pk)
            self.check_object_permissions(request, order)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # count = len(order)
        # new_data = {"count": count}
        serializer = OrderSerializer(order)
        # new_data.update(serializer.data)
        return Response(serializer.data)
        # return Response(new_data)
    
    def destroy(self, request, pk=None): # /api/orders/<str:id>
        # user = request.user
        try:
            order = Order.objects.get(pk=pk)
            self.check_object_permissions(request, order)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response({"msg": "Order Removed"}, status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action in USER_REQUEST:
            permission_classes = [
                IsAuthenticated,
            ]
        elif self.action in ADMIN_REQUEST:
            permission_classes = [
                IsAuthenticated,
                IsAdminUser
            ]
        else:
            permission_classes = [IsAdminUser,]
        
        return [permission() for permission in permission_classes]