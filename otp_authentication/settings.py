"""
Django settings for otp_authentication project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zu8@&qn7h0rh^cy1e-4-k1z!k$in8q5^7s_*!@e=7+^g!u0%gp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'rest_framework',
	'accounts',
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

ROOT_URLCONF = 'otp_authentication.urls'

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

WSGI_APPLICATION = 'otp_authentication.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'


REST_FRAMEWORK = {
	# Use Django's standard `django.contrib.auth` permissions,
	# or allow read-only access for unauthenticated users.
	'DEFAULT_PERMISSION_CLASSES': [
		# 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
		'rest_framework.permissions.AllowAny',

	],
	'DEFAULT_AUTHENTICATION_CLASSES': (
		# 'rest_framework.authentication.BasicAuthentication',
		'accounts.authentication.TokenAuthentication',
	)
}
REST_AUTH_TOKEN_MODEL = 'accounts.models.Token'
REST_AUTH_TOKEN_CREATOR = 'accounts.models.multiple_token_creator'


LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		# 'verbose': {
		# 	'format':
		# 		'%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
		# },
		# 'simple': {
		# 	'format': '%(levelname)s %(message)s'
		# },
		# 'advanced': {
		# 	'format': '%(asctime)s %(levelname)s\t %(message)s'
		# },
		'standard': {
			'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
			'datefmt': "%d/%b/%Y %H:%M:%S"
		},
		# 'timestampthread': {
		# 	'format': "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]"
		# 		" [%(name)-20.20s]  %(message)s",
		# },
	},
	'handlers': {
		'null': {
			'level': 'DEBUG',
			'class': 'logging.NullHandler',
		},
		'console': {
			'level': 'DEBUG',
			# 'filters': ['require_debug_true'],
			'class': 'logging.StreamHandler',
			'formatter': 'standard'
		},
	},
	'loggers': {
		'django': {
			'handlers': ['console'],
			'propagate': False,
			'level': 'INFO',
		},
		'django.db.backends': {
			'handlers': ['console'],  # Quiet by default!
			'propagate': False,
			'level': 'ERROR',
		},
		'': {
			'handlers': ['console'],
			'level': 'DEBUG',  # this level or higher goes to the console,
		},
	}
}
