from ast import Or
from django.shortcuts import render
from rest_framework import viewsets, status

from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer


from rest_framework.permissions import IsAuthenticated, IsAdminUser


# USER_REQUEST = ['retrieve_user_order', 'create', 'retrieve_order']
USER_REQUEST = ['retrieve_user_order', 'create']
ADMIN_REQUEST = ['list', 'update', 'partial_update', 'destroy']


from django.contrib.auth import get_user_model as User


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def list(self, request): 
        print(request.GET.get("delivered"), "delivered data")
        orders = Order.objects.all()
        # for order in orders:
        #     print(order, order.user)

        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)
    
    def create(self, request):
        # print("I AM CREATING")
        data = request.data

        print(request.user.id, "user bandai xa")
        data['user'] = request.user.id
        # print(data)
        self.check_object_permissions(request, data)
        # serializer = OrderSerializer(data=request.data, many=True)
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve_order(self, request, pk=None): # /api/order/<str:id>  

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

    def retrieve_user_order(self, request, pk=None): # /api/order/<str:id>   user_id

        # superusers = User.objects
        # print(User().objects.filter(is_superuser=True)[0].ahjin_coin)
        # print(superusers)
        # print(request)
        orders = Order.objects.all()
        try:
            user = User().objects.get(pk=pk)
            self.check_object_permissions(request, orders)
        except User().DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        order = orders.get(user=request.user)
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