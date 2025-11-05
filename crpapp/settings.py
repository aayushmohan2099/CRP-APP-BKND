# crpapp/settings.py
import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'replace-this-secret-for-dev')

DEBUG = True

ALLOWED_HOSTS = ['ayush3bdo.pythonanywhere.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'background_task',
    'django_cleanup.apps.CleanupConfig',
    'drf_yasg',
    'django_filters',

    # local apps
    'core',
    'epSakhi',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'crpapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'crpapp.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DATABASES - dual DB: default -> upsrlm_epsakhi, master -> upsrlm
DATABASES = {
    # epsakhi data (Django-managed app tables, auth, caching table, background tasks etc.)
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'upsrlm_epsakhi',
        'USER': 'techno_sakhi_db',
        'PASSWORD': 'techno@2025',   
        'HOST': '204.11.58.166',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4'
        }
    },

    # upsrlm master data (shared master_* tables used by multiple apps)
    'master': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'upsrlm',
        'USER': 'techno_dev',
        'PASSWORD': 'techno@2025',
        'HOST': '204.11.58.166',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4'
        }
    }
}

# Tell Django to use the router that routes core -> master DB
DATABASE_ROUTERS = ['core.dbrouters.MasterDBRouter']

# Cache — DB cache (no Redis)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache_table',
    }
}

# Create the cache table with: python manage.py createcachetable --database=default

# Password validation — keep defaults
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Use custom authentication backend (master_user)
AUTHENTICATION_BACKENDS = (
    'core.backends.MasterUserBackend',  # custom backend to read from DB
    'django.contrib.auth.backends.ModelBackend',  # fallback
)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# DRF + JWT (simplejwt)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend', 'rest_framework.filters.SearchFilter', 'rest_framework.filters.OrderingFilter'],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
}

# CORS - restrict later to mobile app origin if needed
CORS_ALLOW_ALL_ORIGINS = True

# File upload limits (enforced in code too)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 6 * 1024 * 1024   # 6MB
