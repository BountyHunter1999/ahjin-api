from django.urls import path, re_path, include
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView, ConfirmEmailView
from dj_rest_auth.views import LoginView, LogoutView, \
                               PasswordResetView, PasswordResetConfirmView, \
                               UserDetailsView

from rest_framework_simplejwt.views import TokenVerifyView
from dj_rest_auth.jwt_auth import get_refresh_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='account_signup'),
    path('login/', LoginView.as_view(), name='account_login'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
    path('detail/', UserDetailsView.as_view(), name='rest_user_details'),

    path('verify-email/',
         VerifyEmailView.as_view(), name='rest_verify_email'),
    path('account-confirm-email/',
         VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$',
         VerifyEmailView.as_view(), name='account_confirm_email'),
    path('password-reset/', PasswordResetView.as_view()),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'), 
     path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
     path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
]