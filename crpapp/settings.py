# crpapp/settings.py
import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# ---- HARD-CODED SECRET (you asked to keep everything in settings.py) ----
SECRET_KEY = 'replace-this-secret-for-dev-CHANGE-TO-PROD-SECRET'

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

# --------------------- DATABASES (HARD-CODED) ---------------------
# default -> upsrlm_epsakhi (Django-managed)
# master -> upsrlm (shared master_* tables)
DATABASES = {
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

# Database router: core -> master, others -> default
DATABASE_ROUTERS = ['core.dbrouters.MasterDBRouter']

# --------------------- CACHE (DB-backed) ---------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache_table',
    }
}
# createcachetable command for default DB:
# python manage.py createcachetable --database=default

# --------------------- AUTH / PASSWORDS ---------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Custom auth backend that uses master_user table
AUTHENTICATION_BACKENDS = (
    'core.backends.MasterUserBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# --------------------- STATIC / MEDIA ---------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'    # run collectstatic -> files go here
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'           # uploaded files (images, certificates)

# Ensure the /media/ directory exists
os.makedirs(MEDIA_ROOT, exist_ok=True)

# --------------------- REST FRAMEWORK / JWT ---------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # No forced DEFAULT_PERMISSION_CLASSES here — your mobile app will send JWTs.
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter'
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
}

# CORS
CORS_ALLOW_ALL_ORIGINS = True

# File upload limits (enforced in code too)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 6 * 1024 * 1024   # 6MB
