"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.9.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import datetime
import environ

env = environ.Env(
    DEBUG=(bool, True)
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-z+i4b&ay4-%rx$ml7)604efg7wr!$997siy(n9!ukp&#31szvr"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "daphne",  # must be the first
    "channels",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "users.apps.UsersConfig",
    "events.apps.EventsConfig",

    'corsheaders',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'dj_rest_auth',
    
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'dj_rest_auth.registration',

    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',




]

CORS_ALLOW_ALL_ORIGINS =True




REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

   'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
   'PAGE_SIZE': 20
}
REST_AUTH = {
    'USE_JWT': True,
}

SIMPLE_JWT = {
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=180),
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "corsheaders.middleware.CorsMiddleware",

    "allauth.account.middleware.AccountMiddleware"
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",



            ],
        },
    },
]
ROOT_URLCONF = "core.urls"

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

# Django Channels
# Adding Django Channel Layers

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",

    },
}

# End Django Channels


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Email settings
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


AUTH_USER_MODEL = "users.CustomUser"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]



SITE_ID = 1

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = [

    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",

]

ACCOUNT_AUTHENTICATION_METHOD = 'username'

ACCOUNT_EMAIL_VERIFICATION = 'none'

ACCOUNT_EMAIL_REQUIRED = False




# client id
# W1qJEAuv6pwXDeORBo8e45e7rdCQt47GOiI4jUgX

# client secret
# oWWaIDkXKtU9lFNVqZLKf8nQo253lvDiWuaa7RxzxaVO31uaAYOeftDUmtNW4iYY79IPS52B0eEXqMhWaPPk7PQDOrZOqL24DiqHqlKdeldTrsDpfKFOOtnDkr6LdnHM