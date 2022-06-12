from dj_rest_auth.registration.views import RegisterView

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


from rest_framework.generics import RetrieveUpdateAPIView


class UserManager(BaseUserManager):

    def create_superuser(self, email, password):
        """
        Creates and saves a new superuser
        """
        user = RegisterView.create(email, password)


class AdminView(RegisterView):

    def create_admin(self, request, *args, **kwargs):
        print(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer)
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return 

from rest_framework.permissions import IsAuthenticated
# from dj_rest_auth.serializers import (
#     UserDetailsSerializer, 
# )
from .serializers import CustomUserDetailsSerializer, CustomLoginSerializer
from django.contrib.auth import get_user_model
from dj_rest_auth.views import LoginView

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
        response.is_admin =  self.request.user.is_superuser
        # self.user.refresh_from_db()
        print(response)
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