from pathlib import Path
import os

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings
SECRET_KEY = 'django-insecure-1wdw#-v0^0*n#p6bpr^wrib67c_^jx3))yh+88=aouslu(06^u'
DEBUG = True
ALLOWED_HOSTS = [
    'icereddot.onrender.com',
    'campus-blood.onrender.com',
    '127.0.0.1',
    'localhost'
]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blood',
    'widget_tweaks',  # for form styling
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Updated for Render deployment
ROOT_URLCONF = 'campus_blood.urls'
WSGI_APPLICATION = 'campus_blood.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # templates folder
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

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Login settings
LOGIN_URL = '/login/'   
LOGIN_REDIRECT_URL = '/'  

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Media files (for profile pictures)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static files (CSS, JS, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]        # dev static
STATIC_ROOT = BASE_DIR / "staticfiles"          # collectstatic destination

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Settings (Mailjet)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'in-v3.mailjet.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get('EMAIL_USER', 'fcabc45474378db83bf843b994581f67')  # Mailjet API Key
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS', 'd87a0be2738844f3935ff7db4703e5db')  # Mailjet Secret Key
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'reon128633@gmail.com')  # Verified sender
