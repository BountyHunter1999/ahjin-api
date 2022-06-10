from dj_rest_auth.registration.views import RegisterView

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


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