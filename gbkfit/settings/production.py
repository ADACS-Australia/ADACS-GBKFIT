from .base import *

DEBUG = False

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CONN_MAX_AGE = 900 # 15 minutes of persistent connection

EMAIL_HOST = 'mail.swin.edu.au'
EMAIL_PORT = 25

ROOT_SUBDIRECTORY_PATH = 'projects/gbkfit/live/'
STATIC_URL = '/projects/gbkfit/live/static/'

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static/')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "..", "gbkfit_web", "static/"),
]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media/')

SITE_URL = 'https://supercomputing.swin.edu.au/projects/gbkfit/live'

try:
    from .local import *
except ImportError:
    pass
