from dj_rest_auth.registration.views import RegisterView

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


from rest_framework.generics import RetrieveUpdateAPIView


from rest_framework import viewsets, status

from rest_framework.response import Response
# class UserManager(BaseUserManager):

#     def create_superuser(self, email, password):
#         """
#         Creates and saves a new superuser
#         """
#         user = RegisterView.create(email, password)


# class AdminView(RegisterView):

#     def create_admin(self, request, *args, **kwargs):
#         print(request)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         print(serializer)
#         user = self.create_user(email, password)
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)

#         return 

from rest_framework.permissions import IsAuthenticated
# from dj_rest_auth.serializers import (
#     UserDetailsSerializer, 
# )
from .serializers import CustomRegisterSerializer, CustomUserDetailsSerializer, CustomLoginSerializer
from django.contrib.auth import get_user_model
from dj_rest_auth.views import LoginView

from rest_framework.response import Response


class CustomUserDetailsView(RetrieveUpdateAPIView):
    """
    Reads and updates UserModel fields
    Accepts GET, PUT, PATCH methods.
    Read-only fields: pk, email
    Returns UserModel fields.
    """
    # serializer_class = UserDetailsSerializer
    serializer_class = CustomUserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        # print(f"User is {type(self.request.user)}")
        # print(f"User is {self.request.user.is_superuser}")
        # self.request.user.is_admin = self.request.user.is_superuser
        response = self.request.user
        print("I am groot")
        response.is_admin =  self.request.user.is_superuser

        # self.user.refresh_from_db()
        # print("RESPONSE IS",response, type(response))
        return response

    def get_queryset(self):
        """
        Adding this method since it is sometimes called when using
        django-rest-swagger
        """
        print("This is also called")
        return get_user_model().objects.none()


class CustomLoginView(LoginView):

    serializer_class = CustomLoginSerializer


class CustomRegisterView(RegisterView):

    serializer_class = CustomRegisterSerializer



from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser 

from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """

    queryset = get_user_model().objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]

    def list(self, request):
        print("I am calling list")
        users = get_user_model().objects.all().order_by('-date_joined')
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

    def destroy(self, request, pk=None): # /api/orders/<str:id>
        # user = request.user
        print("deleting user hai")
        try:
            user = get_user_model().objects.get(pk=pk)
            self.check_object_permissions(request, user)
        except get_user_model().DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({"msg": "User Removed"}, status=status.HTTP_204_NO_CONTENT)
