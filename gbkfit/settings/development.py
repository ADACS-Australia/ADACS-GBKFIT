from .base import *

DEBUG = True

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'mail.swin.edu.au'
EMAIL_PORT = 25

ROOT_SUBDIRECTORY_PATH = ''
STATIC_URL = '/static/'

try:
    from .local import *
except ImportError:
    pass
