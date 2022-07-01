import email
from rest_framework import viewsets, status #, mixins
from rest_framework.response import Response
from .models import Product, Review

from django.contrib.auth import get_user_model as User
from django.shortcuts import get_object_or_404

from .serializers import ProductSerializer, ReviewSerializer

from rest_framework.permissions import IsAuthenticated, IsAdminUser


USER_REQUEST = ['list', 'retrieve']
ADMIN_REQUEST = ['create', 'update', 'partial_update', 'destroy']

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def _get_cat(self, data, cat):
        data = data.filter(cat=cat)
        return data

    def list(self, request): # GET /api/products
        products = Product.objects.all()
        # print(request.query_params)
        old_list = self.request.query_params.get("new") == "False"
        cat = self.request.query_params.get("cat")

        # print("filter product", products.filter(cat=cat))
        cat_data = self._get_cat(products, cat)
        products = cat_data if cat else products
        serializer = ProductSerializer(products, many=True)
        if old_list:
            data = serializer.data[::-1] 
        # print(serializer.data[:2])
        else:
            data = serializer.data
        return Response(data)

    def create(self, request): # POST /api/products
        serializer = ProductSerializer(data=request.data)
        # serializer = ProductSerializer(data=request.data, many=True)
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
        print("valid")
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
                # IsAuthenticated,
            ]
        # elif self.action in ADMIN_REQUEST:
        #     permission_classes = [
        #         IsAdminUser,
        #     ]
        else:
            permission_classes = [IsAdminUser,]

        return [permission() for permission in permission_classes]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def list(self, request, pk): # GET /api/products/reviews/<str:prod_id>
        try:
            product = Product.objects.get(pk=pk)
            self.check_object_permissions(request, product)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # product = Product.objects.get(pk=pk)
        reviews = product.review_set.all()
        data = list()
        for i in range(len(reviews)):
            review = reviews[i]
            print("ussername", review.user.username)
            print("email", review.user.email)

            user = {
                "username": review.user.username,
                "email": review.user.email,
                "pk": review.user.id
            }
            # print(review.user, review.user.id, review.user.username)
            # print(i, type(review))
            print(review.user.username)
            data.append({
                "id": review.id,
                "rating": review.rating,
                "comment": review.comment,
                "product": review.product,
                "user": review.user,
                # "username": review.user.username,
                # "email": review.user.email,
                "createdAt": review.createdAt,
                "updatedAt": review.updatedAt,
                # "user": user,
            })
        serializer = ReviewSerializer(data, many=True)
        return Response(serializer.data)


    def create(self, request, pk): # POST /api/reviews
        # print(f"request in review: {request.data}")
        # print(f"request user in review: {request.user.id}")
        # reviews = Review.objects.all()
        try:
            product = Product.objects.get(pk=pk)
            self.check_object_permissions(request, product)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user
        data = request.data
        # print("I WAS HERE HAI CREATE")
        # Review already exists, don't allow them to spam reviews
        alreadyExists = product.review_set.filter(user=user).exists()

        if alreadyExists:
            content = {"detail": "Product already reviewed"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        # No Rating or 0 Rating
        elif data['rating'] == 0:
            content = {"detail": "Please select a rating"}
            return Response(content, status.HTTP_400_BAD_REQUEST)
        
        # Create Review
        else:
            print(user)
            review = Review.objects.create(
                user = user,
                product = product,
                # name = user.username if user.username ,
                rating = data['rating'],
                comment = data['comment']
            )
            reviews = product.review_set.all()
            product.numReviews = len(reviews)

            total = 0

            for i in reviews:
                total += i.rating
            
            product.rating = total / len(reviews)
            product.save()

            return Response({"msg":"Review Added"}, status.HTTP_201_CREATED)

        # data = request.data
        # data['user'] = request.user.id
        # data['product'] = pk
        # serializer = ReviewSerializer(data=data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk):
        # try:
        #     product = Product.objects.get(pk=pk)
        #     self.check_object_permissions(request, product)
        # except Product.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)

        # # product = Product.objects.get(pk=pk)
        # reviews = product.review_set.all()
        # data = dict()
        # for i in range(len(reviews)):
        #     review = None
        #     reviewer_id = reviews[i].user.id
        #     requester_id = request.user.id
        #     if reviewer_id == requester_id:
        #         review = reviews[i] 
            
        # if review:
        #     # data['rating'] = request.data.get("rating", review.rating)
        #     # data['comment'] = request.data.get("comment", review.comment)
        #     # data['product'] = review.product
        #     # data['user'] = review.user

        #     serializer = ReviewSerializer(instance= review, data=request.data)
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save()
        #     # return Response(serializer.data)
        #     return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        # else:
        #     return Response({"msg":"Unauthorized"}, status.HTTP_401_UNAUTHORIZED)
        try:
            review = Review.objects.get(pk=pk)
            self.check_object_permissions(request, review)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user == review.user or request.user.is_superuser:
            serializer = ReviewSerializer(instance=review, data=request.data)
            serializer.is_valid(raise_exception=True)
            print("valid")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response({"msg":"Unauthorized"}, status.HTTP_401_UNAUTHORIZED)


    def destroy(self, request, pk): # /api/products/<str:id>/reviews/
        try:
            review = Review.objects.get(pk=pk)
            self.check_object_permissions(request, review)
        except Review.DoesNotExist:
            return Response({"msg": "No such review"}, status=status.HTTP_404_NOT_FOUND)

        if request.user == review.user or request.user.is_superuser:
            review.delete()
            return Response({"msg": "Review removed"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"msg":"Unauthorized"}, status.HTTP_401_UNAUTHORIZED)


        # product = Product.objects.get(pk=pk)
        # try:
        #     product = Product.objects.get(pk=pk)
        #     self.check_object_permissions(request, product)
        # except Product.DoesNotExist:
        #     return Response({"msg": "No such product"}, status=status.HTTP_404_NOT_FOUND)
        # # product = Product.objects.get(pk=pk)

        
        # # bulk delete
        # reviews = product.review_set.all()
        # review_id = self.request.query_params.get("review")

        # for i in range(len(reviews)):
        #     review = reviews[i]
        #     reviewer_id = review.user.id
        #     requester_id = request.user.id
        #     has_permission = reviewer_id == requester_id or request.user.is_superuser
        #     correct_review = int(review_id) == review.id
        #     if has_permission and correct_review:
        #         # reviews[i].delete()
        #         review.delete()
            
            # return Response({"msg": "Review Removed"}, status=status.HTTP_204_NO_CONTENT)
        # return Response({"msg": "Bad Request Bruh"}, status=status.HTTP_400_BAD_REQUEST)
    
    # def get_permissions(self):
    #     if self.action in USER_REQUEST:
    #         permission_classes = [
    #             # IsAuthenticated,
    #         ]
    #     # elif self.action in ADMIN_REQUEST:
    #     #     permission_classes = [
    #     #         IsAdminUser,
    #     #     ]
    #     else:
    #         permission_classes = [IsAdminUser,]

    #     return [permission() for permission in permission_classes]


