from dataclasses import fields
from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import  LoginSerializer, UserDetailsSerializer
from django.utils.translation import gettext_lazy as _

from core.models import CustomUser
# from core.models import GENDER_SELECTION, CustomUser
from django.contrib.auth import get_user_model

class CustomRegisterSerializer(RegisterSerializer):
    # gender = serializers.ChoiceField(choices=GENDER_SELECTION)
    phone_number = serializers.CharField(max_length=30)
    ahjin_coin = serializers.FloatField(default=0)
    user_hash = serializers.CharField(max_length=255, required=False)
    is_admin = serializers.BooleanField(default=False)

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        print("IN CUSTOM REGISTER")
        # print(f"request is: {request.data}")
        user = super().save(request)
        # user.gender = self.data.get('gender')
        user.phone_number = self.data.get('phone_number')
        user.ahjin_coin = self.data.get('ahjin_coin')
        user.user_hash = self.data.get('user_hash')
        # print("request on saving new user", request)
        user.is_admin = self.data.get('is_admin')
        user.save()  # CHANGE THIS
        # print("USER NOW, ", user)
        return user

from django.conf import settings

class CustomUserDetailsSerializer(UserDetailsSerializer):
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
        model = CustomUser
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # CustomUser.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not


        # # model = CustomUser
        fields = (
            'pk', 'email', 'phone_number', 
            'ahjin_coin', 'is_superuser', 'user_hash',
            'username'
        )
        # extra_kwargs = {
        #     'first_name': {'required': True},
        #     'last_name': {'required': True}
        # }
        # read_only_fields = ('pk', 'email',)


from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate

class CustomLoginSerializer(LoginSerializer):

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

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



from django.contrib.auth import get_user_model

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['pk', 'username', 'email', 'phone_number', 'phone_number']




# FOr password reset
from dj_rest_auth.forms import AllAuthPasswordResetForm

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.urls.base import reverse
from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import user_pk_to_url_str, user_username
from allauth.utils import build_absolute_uri
from dj_rest_auth.forms import AllAuthPasswordResetForm
from dj_rest_auth.serializers import PasswordResetSerializer

from django.conf import settings

class CustomAllAuthPasswordResetForm(AllAuthPasswordResetForm):
    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator',
                                     default_token_generator)
        print("I am in the form")
        for user in self.users:

            temp_key = token_generator.make_token(user)

            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            # send the password reset email
            path = reverse(
                'password_reset_confirm',
                args=[user_pk_to_url_str(user), temp_key],
            )
            if settings.PASSWORD_RESET_URL:
                url = settings.PASSWORD_RESET_URL+"/"+user_pk_to_url_str(user)+"/"+ temp_key
            else:
                url = build_absolute_uri(None, path) # PASS NONE INSTEAD OF REQUEST
                # url = build_absolute_uri(request, path)
            context = {
                'current_site': current_site,
                'user': user,
                'password_reset_url': url,
                'request': request,
            }
            if app_settings.AUTHENTICATION_METHOD != app_settings.AuthenticationMethod.EMAIL:
                context['username'] = user_username(user)
            get_adapter(request).send_mail('account/email/password_reset_key',
                                           email, context)
        return self.cleaned_data['email']

class CustomPasswordResetSerializer(PasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        return CustomAllAuthPasswordResetForm