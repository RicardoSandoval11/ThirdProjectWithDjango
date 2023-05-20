from .base import *

DEBUG = False

ALLOWED_HOSTS = ['164.92.204.132']

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR.child('static')]
STATIC_ROOT = BASE_DIR.child('staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.child('media')