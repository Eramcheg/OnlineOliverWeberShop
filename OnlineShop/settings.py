"""
Django settings for OnlineShop project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

import firebase_admin
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv
from firebase_admin import credentials, firestore

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
# load_dotenv(dotenv_path)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
dotenv_path = BASE_DIR / 'OnlineShop/.env'

load_dotenv(dotenv_path)
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-av+bzqy62h9m=9%^%c11v16=7h(aq(e*j2zn9-vk6r20wpn%_n'
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
STRIPE_ENDPOINT_SECRET = os.getenv('STRIPE_ENDPOINT_SECRET')

PAYPAL_MODE = os.getenv('PAYPAL_MODE', 'sandbox')  # По умолчанию 'sandbox' для тестирования
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')
# SECURITY WARNING: don't run with debug turned on in production!

FIREBASE_CREDENTIALS_FILE = os.path.join(BASE_DIR, "shop", "static", "key2.json")

# Инициализация Firebase (только один раз)
if not firebase_admin._apps:
    FIREBASE_CREDENTIALS = credentials.Certificate(FIREBASE_CREDENTIALS_FILE)
    firebase_admin.initialize_app(FIREBASE_CREDENTIALS)

# Firestore client (глобальный объект)
FIRESTORE_CLIENT = firestore.client()

GEOIP_config = os.path.join(BASE_DIR, "shop", "static", "GEOIP", "GeoLite2-Country.mmdb")

DEBUG = True

ALLOWED_HOSTS = ["*"]

GEOIP_PATH = os.path.join(BASE_DIR, 'shop/static/GEOIP'),

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'background_task',
    'widget_tweaks',
    'shop',
    # 'autotranslate',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'shop.middleware.ensure_anon_session_middleware.EnsureAnonymousSessionMiddleware',
    'shop.middleware.redirect_en_to_gb_middleware.RedirectENtoGBMiddleware',
    # 'shop.middleware.DefaultLanguageMiddlware.DefaultLanguageMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',

]
# CACHE_MIDDLEWARE_ALIAS = 'default'
# CACHE_MIDDLEWARE_SECONDS = 600  # Cache for 10 minutes
# CACHE_MIDDLEWARE_KEY_PREFIX = ''
ROOT_URLCONF = 'OnlineShop.urls'
CSRF_COOKIE_HTTPONLY = False  # Убедитесь, что JavaScript может читать cookie
CSRF_COOKIE_SECURE = True     # Только если используется HTTPS
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'shop/templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processor.user_role',
                'shop.context_processor.user_is_special',
                'shop.context_processor.customer_type',
                'shop.context_processor.shop_page_url',
            ],
        },
    },
]

WSGI_APPLICATION = 'OnlineShop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'gb'

TIME_ZONE = 'UTC'
LOGIN_URL = 'login'
USE_I18N = True
USE_L10N = True
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
from django.utils.translation import gettext_lazy as _
LANGUAGES = [
    ('gb', _('English')),
    ('de', _('German')),
    ('it', _('Italian')),
    ('fr', _('French')),
    ('es', _('Spanish')),
    ('ru', _('Russian')),
]

USE_TZ = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'westadatabase@gmail.com'
# EMAIL_HOST_PASSWORD = 'avrt uxcf vahg ixbe'
EMAIL_HOST_PASSWORD = 'thfx sduu sgeu urhz'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'shop/static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'shop/media')
# URL, по которому файлы будут доступны
MEDIA_URL = '/media/'
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
