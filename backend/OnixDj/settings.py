"""
Django settings for OnixDj project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_URL = ""
SITE_HOST = os.getenv("SITE_HOST", "http://localhost/")

ENVIRONMENT = os.getenv("DJANGO_ENV", "development")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-i(#wq+z9yj3pb*t$!xkxmx+3hk*og-mq$j27jnwlzc-f6&jg8q",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False").lower() == "true"


ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost"
).split(",")

SITE_ID = 1

# Auth
AUTH_USER_MODEL = "users.CustomUser"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "auth",
    "JWT_AUTH_REFRESH_COOKIE": "refresh_cookie",
    "LOGIN_SERIALIZER": "users.serializers.CustomLoginSerializer",
    "REGISTER_SERIALIZER": "users.serializers.CustomRegisterSerializer",
    "USER_DETAILS_SERIALIZER": "users.serializers.CustomUserDetailsSerializer",
    # Optional
    "JWT_AUTH_HTTPONLY": False,
}

APPEND_SLASH = False


ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

EMAIL_CONFIRM_REDIRECT_BASE_URL = "/email/confirm/"
PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL = "/password-reset/confirm/"
# EMAILS
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 1025))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False").lower() == "true"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

# Oauth setup
SOCIALACCOUNT_PROVIDERS = {
    "github": {
        "APP": {
            "client_id": "Ov23liSytzggK8FPZmw5",  # replace me
            "secret": "014a7ba0fa5f34d325afc57ac9584c2b51daa80b",  # replace me
            "key": "",  # leave empty
        },
        "SCOPE": [
            "read:user",
            "user:email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "VERIFIED_EMAIL": True,
    },
}

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Rest framework
    "rest_framework",
    "rest_framework.authtoken",
    # Auth
    "users",
    "dj_rest_auth",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth.registration",
    "rest_framework_simplejwt.token_blacklist",
    # Social providers
    "allauth.socialaccount.providers.github",
    # Specs
    "drf_spectacular",
    "drf_spectacular_sidecar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Whitenoise
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # Auth
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "OnixDj.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "OnixDj.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
if ENVIRONMENT != "production":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.{}".format(
                os.getenv("DATABASE_ENGINE", "sqlite3")
            ),
            "NAME": os.getenv("POSTGRES_DB", "polls"),
            "USER": os.getenv("POSTGRES_USER", "myprojectuser"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "password"),
            "HOST": os.getenv("DATABASE_HOST", "127.0.0.1"),
            "PORT": os.getenv("DATABASE_PORT", 5432),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# DRF SPEC
SPECTACULAR_SETTINGS = {
    "TITLE": "OnixDj Backend",
    "DESCRIPTION": "A backend api for nuxt and other web apps with auth.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": False,
    # OTHER SETTINGS
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}
