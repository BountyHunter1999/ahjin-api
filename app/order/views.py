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
from products.models import Product
from django.db import transaction


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def list(self, request): 
        is_delivered = request.GET.get("delivered", None)
        if is_delivered == "T":
            orders = Order.objects.filter(delivered = True)
            # print(orders.get(delivered=True))
        # for order in orders:
        #     print(order, order.user)
        elif is_delivered == "F":
            orders = Order.objects.filter(delivered = False)
        else:
            orders = Order.objects.all()

        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)
    
    def create(self, request):
        # print("I AM CREATING")
        data = request.data

        print(request.user.id, "user ko order bandai xa")
        data['user'] = request.user.id
        print(data)


            
            # print(target_product.unique_feature[chosen]["quantity"])
            # print(product)
        try:
            with transaction.atomic():
                # product = Product.objects.get(data)
                self.check_object_permissions(request, data)
                # serializer = OrderSerializer(data=request.data, many=True)
                serializer = OrderSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                # after order place update will be triggered
                for product in data['products']:
                    product_id = product['product']
                    decrease_count = product['quantity']
                    chosen = product['productChosen']
                    # print(product_id)
                    target_product = Product.objects.get(pk=product_id)
                    target_product.unique_feature[chosen]["count"] -= decrease_count
                    target_product.save() 
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IndexError:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
    
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
        order = orders.filter(user=request.user)
        print(order)
        serializer = OrderSerializer(order, many=True)
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
    
    def update(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
            self.check_object_permissions(request, order)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(instance=order, data=request.data)
        serializer.is_valid(raise_exception=True)
        print("valid")
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

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