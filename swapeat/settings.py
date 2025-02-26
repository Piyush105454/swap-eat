from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#t^q$=_^+q00lk6uvi8aon^mazx+_&43-t7x0+pd254e!5h!2#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Set to False in production

ALLOWED_HOSTS = ['toxic-ilse-piyush105454-c639ba90.koyeb.app', 'localhost', '127.0.0.1']
# Add this if you want to allow all hosts. Ensure DEBUG = False for this.
# ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'swapfood',
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Handles various security settings
    'django.middleware.common.CommonMiddleware',    # Handles common tasks like APPEND_SLASH
    'django.middleware.csrf.CsrfViewMiddleware',    # Protects against cross-site request forgery
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Manages user authentication
    'django.contrib.messages.middleware.MessageMiddleware',      # Enables messages framework
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Prevents clickjacking attacks
]

ROOT_URLCONF = 'swapeat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'swapeat.wsgi.application'
ASGI_APPLICATION = "swapeat.asgi.application"
CHANNEL_LAYERS = {

    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"},
}

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# To include the directory where your static files are located:
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Redirect after login
LOGIN_URL = '/login/'  # Where users are redirected if not logged in
LOGIN_REDIRECT_URL = '/home/'  # Default page after login
LOGOUT_REDIRECT_URL = '/login/'  # Redirect after logout

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Use Gmail or any other email service provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'swapeatmail@gmail.com'  # Replace with your email
EMAIL_HOST_PASSWORD = 'ivud didb rgrd ciil'  # Replace with your app password
DEFAULT_FROM_EMAIL = 'your_email@gmail.com'

# Added for HTTPS in production environments on Koyeb
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') # Tells Django to trust the proxy
CSRF_TRUSTED_ORIGINS = [
    'https://toxic-ilse-piyush105454-c639ba90.koyeb.app' # Needed for CSRF
]

