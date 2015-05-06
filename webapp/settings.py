"""
Django settings for webapp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import ConfigParser
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6(s&7hlh4isp&2l$0*8$zrls=fx@e#yb)4l@4_rl=4)2q4#=2+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

# Login Related
# Used by the authentication system for the private-todo-list application.
# URL to use if the authentication system requires a user to log in.
LOGIN_URL = '/login'
# Default URL to redirect to after a user logs in.
LOGIN_REDIRECT_URL = '/'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tmate',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)


ROOT_URLCONF = 'webapp.urls'

WSGI_APPLICATION = 'webapp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = ('tmate/static/tmate/', )
STATIC_ROOT = 'staticfiles'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}

### Server Setting (Heroku) ###
if 'DATABASE_URL' in os.environ:

    DEBUG = False

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Allow all host headers
    ALLOWED_HOSTS = ['*']

    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

### Database ###
    # Deployed Settings
    DATABASES = {'default': dj_database_url.config(default=os.environ['DATABASE_URL'])}

### Email ###
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = os.environ['GMAIL_USER']
    EMAIL_HOST_PASSWORD = os.environ['GMAIL_PASSWORD']
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

### Static Storage ###
    # S3
    AWS_ACCESS_KEY = os.environ['S3_AccessKey']
    AWS_SECRET_ACCESS_KEY = os.environ['S3_SecretKey']
    S3_BUCKET = os.environ['S3_Bucket']

    # Parse database configuration from $DATABASE_URL
    # Enable Connection Pooling
    DATABASES['default']['ENGINE'] = 'django_postgrespool'

else:

    config = ConfigParser.ConfigParser()
    config.read(BASE_DIR + '/config.ini')

### Email ###
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = config.get('Gmail', 'User')
    EMAIL_HOST_PASSWORD = config.get('Gmail', 'Password')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

# S3
### Static Storage ###
    AWS_ACCESS_KEY = config.get('S3', 'AccessKey')
    AWS_SECRET_ACCESS_KEY = config.get('S3', 'SecretKey')
    S3_BUCKET = config.get('S3', 'Bucket')

