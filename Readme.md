**Project Overview**
====================

The aim of the project is to facilitate user interface for GBKFIT-cloud 
where the users will be able to submit job requests that will be served 
by the GBKFIT-cloud. This project is currently made using the django 
framework.

Setup
=====

## Local Settings ##
The project is required to have customised machine specific settings.
Those settings need to included or overridden in the local settings file.
Create one `local.py` in the settings module next to the other settings
files (`base.py`, `development.py`, `production.py` etc.)

The following settings needs to be present in the `local.py` settings file.

Specify the base directory
```python
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

The admins of the site who will receive error emails.
```python
ADMINS = [
    ('Your Name', 'youremail@dd.ress'),
]

MANAGERS = ADMINS
```

The address from where the server emails will be sent.
```python
SERVER_EMAIL = 'serveremail@dd.ress'
```

The address from where the notification emails will be sent.
```python
EMAIL_FROM = 'mail@dd.ress'
```

Set up the log file settings.
```python
LOG_DIRECTORY = os.path.join(BASE_DIR, 'path/to/log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(levelname)s (%(name)s): %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIRECTORY, 'gbkfit.log'),
            'formatter': 'standard',
            'when': 'midnight',
            'interval': 1,
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'gbkfit_web': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

Set up the database settings. Replace it with MySQL or other database 
if required.
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}
```

(Optional) Force the https protocol even if the request is not secure
in links. Specially helpful in case server is hosted in different 
machine and apache redirect is there.
```python
HTTP_PROTOCOL = 'https'
```

## Required Steps ##
The required steps include the following:
* `virtualenv venv` (create the virtual environment)
* `git pull` (clone the code)
* `source venv/bin/activate` (activate the virtual environment)
* `cd gbkfit/gbkfit/settings` (enter the settings directory)
* `touch local.py` (create the file for local settings - refer above
for setting up a local settings file)
* `cd ../../` (enter the root directory of the project)
* `./development-manage.py migrate` (migrate, for staging or production 
specify the required manage.py file instead)
* `./development-manage.py runserver` (running the server)
