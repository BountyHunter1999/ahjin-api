from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import  LoginSerializer

from core.models import CustomUser
# from core.models import GENDER_SELECTION, CustomUser
from django.contrib.auth import get_user_model
UserModel = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    # gender = serializers.ChoiceField(choices=GENDER_SELECTION)
    phone_number = serializers.CharField(max_length=30)
    ahjin_coin = serializers.FloatField(default=0)
    user_hash = serializers.CharField(max_length=255, required=False)


    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        print(f"request is: {request.data}")
        user = super().save(request)
        # user.gender = self.data.get('gender')
        user.phone_number = self.data.get('phone_number')
        user.ahjin_coin = self.data.get('ahjin_coin')
        user.user_hash = self.data.get('user_hash')
        user.save()
        return user

from django.conf import settings

class CustomUserDetailsSerializer(RegisterSerializer):
    """
    User model w/o password
    """

    # @staticmethod
    # def validate_username(username):
    #     if 'allauth.account' not in settings.INSTALLED_APPS:
    #         # We don't need to call the all-auth
    #         # username validator unless its installed
    #         return username

    #     from allauth.account.adapter import get_adapter
    #     username = get_adapter().clean_username(username)
    #     return username

    class Meta:
        extra_fields = []
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # UserModel.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'ahjin_coin'):
            extra_fields.append('ahjin_coin')
        if hasattr(UserModel, 'user_hash'):
            extra_fields.append('user_hash')
        if hasattr(UserModel, 'is_admin'):
            extra_fields.append('is_admin')
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)


from rest_framework.exceptions import ValidationError

class CustomLoginSerializer(LoginSerializer):

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        user = self.get_auth_user(username, email, password)

        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise ValidationError(msg)

        # Did we get back an active user?
        self.validate_auth_user_status(user)

        # If required, is the email verified?
        if not user.is_superuser:
            print("Checking is it admin")
            if 'dj_rest_auth.registration' in settings.INSTALLED_APPS:
                self.validate_email_verification_status(user)

        attrs['user'] = user
        return attrs