from django.db import models
from django.contrib.auth.models import AbstractUser

# from django.contrib.auth.models import (
#     BaseUserManager, AbstractBaseUser, PermissionsMixin
# )

# GENDER_SELECTION = [
#     ('M', 'Male'),
#     ('F', 'Female'),
#     ('O', 'Others'),
# ]


class CustomUser(AbstractUser):
    # We don't need to define the email attribute because is inherited from AbstractUser
    # gender = models.CharField(max_length=20, choices=GENDER_SELECTION)
    phone_number = models.CharField(max_length=30)
    ahjin_coin = models.FloatField(default=0)
    user_hash = models.CharField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField(default=False, blank=True, null=True)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


    # print("Created user")
    # USERNAME_FIELD = 'email'

# from django.contrib.auth.base_user import BaseUserManager
# class UserManager(BaseUserManager):

#     def create_superuser(self, email, password):
#         print("I was called")
#         if password is None:
#             raise TypeError('Superusers must have a password')

#         user = self.create_user(email, password)
#         user.is_admin = True
#         user.is_superuser = True
#         user.save()

#         return user

# class UserManager(BaseUserManager):

#     def create_user(self, email, password, **extra_fields):
#         """
#         Create and saves a new user
#         """
#         if not email:
#             raise ValueError("Users must have an email address")
#         user = self.model(email=self.normalize_email(email), **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)

#         return user

#     def create_superuser(self, email, password):
#         """
#         Creates and saves a new superuser
#         """
#         user = self.create_user(email, password)
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)

#         return user 


# class User(AbstractBaseUser, PermissionsMixin):
#     """
#     Custom user model that supports using email instead of username
#     """
#     email = models.EmailField(max_length=255, unique=True)
#     name = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=30)
#     ahjin_coin = models.FloatField(default=0)
#     user_hash = models.CharField(max_length=255, blank=True, null=True)


#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     # REQUIRED_FIELDS = ['email', 'password']