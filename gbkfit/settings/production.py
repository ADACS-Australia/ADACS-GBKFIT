from .base import *

DEBUG = False

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CONN_MAX_AGE = 900 # 15 minutes of persistent connection

EMAIL_HOST = 'mail.swin.edu.au'
EMAIL_PORT = 25

try:
    from .local import *
except ImportError:
    pass
