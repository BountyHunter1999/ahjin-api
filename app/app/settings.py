"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
import logging.config
from django.core.management.utils import get_random_secret_key

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

my_env = os.environ


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECRET_KEY = os.getenv("SECRET_KEY",
#         get_random_secret_key()
        # )

SECRET_KEY = my_env['DJANGO_SECRET_KEY']
# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = os.getenv('DJANGO_DEBUG', "False") == "True"
# DEBUG = True

# ALLOWED_HOSTS = [
#     '0.0.0.0',
#     'localhost',
#     '127.0.0.1',
# ]
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',

    'rest_framework',
    # 'rest_framework.authtoken',


    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth',
    'dj_rest_auth.registration',

    "corsheaders",

    'core',
    'user',
    'products',
    'order',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('POSTGRES_HOST'),
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_ROOT = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'core.CustomUser'

SITE_ID = 1

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_EMAIL_VERIFICATION = my_env['EMAIL_VERIFICATION_OPTION']
ACCOUNT_EMAIL_VERIFICATION = os.getenv('EMAIL_VERIFICATION_OPTION', "mandatory")

ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# LOGIN_URL = 'http://localhost:8000/api/user/login'
LOGIN_URL = f"{os.getenv('FRONT_END_URL', 'http://localhost:3000')}/login"

# Password change
OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False

# Password reset
PASSWORD_RESET_URL = f"{os.getenv('FRONT_END_URL', 'http://localhost:3000')}/user/change-password"

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'user.serializers.CustomRegisterSerializer',
}

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'user.serializers.CustomUserDetailsSerializer',
    'PASSWORD_RESET_SERIALIZER': 'user.serializers.CustomPasswordResetSerializer',

}


# CORS_ORIGIN_WHITELIST = [
#     'https://localhost:3000',
#     'https://localhost:8000',
# ]


AUTHENTICATION_BACKENDS = [
    # allauth specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    # Needed to login by username in Django admin, regardless of allauth
    'django.contrib.auth.backends.ModelBackend',
]
REST_AUTH_TOKEN_MODEL = None # we using stateless JWT no need for a model

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    )
}
# PERMISSIONS
# IsAuthenticated
# IsAuthenticatedOrReadOnly
# AllowAny

REST_USE_JWT = True

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# For every authenticated session, dj-rest-auth would return a Set-Cookie header
# Set-Cookie: my-app-auth=xxxxxxxxxxxxx; expires=Sun, 17 Feb 2021 14:21:00 GMT; HttpOnly; Max-Age=300; Path=/
JWT_AUTH_COOKIE = 'my-app-auth'

# EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
# SENDGRID_API_KEY = my_env["SENDGRID_API_KEY"]
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", None)

# EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 
                    'django.core.mail.backends.console.EmailBackend'
                )
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'               
# EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"

EMAIL_HOST_USER = os.getenv("GMAIL_ACC") # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = os.getenv("GMAIL_PW")
EMAIL_HOST = os.getenv("EMAIL_HOST")
# TLS is 587 SSL 465
# EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_PORT = 587
# EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", True) == True
EMAIL_USE_TLS =  True
# EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", False)

CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:8000',
#     'http://localhost:3000',
# ]
# ]

# Logging Configuration
# Logging Configuration

# Clear prev config
# LOGGING_CONFIG = None

# # Get loglevel from env
# LOGLEVEL = os.getenv('DJANGO_LOGLEVEL', 'info').upper()

# logging.config.dictConfig({
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'console': {
#             'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s',
#         },
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'console',
#         },
#     },
#     'loggers': {
#         '': {
#             'level': LOGLEVEL,
#             'handlers': ['console',],
#         },
#     },
# })