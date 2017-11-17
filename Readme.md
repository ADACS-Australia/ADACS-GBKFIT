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

Specify the base and media directories
```python
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_URL = '../media/'
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL)
```

Specify the location of the mounted shared data directory
```python
DATA_MOUNT_DIR = '/data/' # Must end in trailing slash
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

Set the REST framework permissions. E.g.
```python
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
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


Running with MySQL, Docker and docker-compose
=============================================

To run the website using docker and MySQL, modify the `local.py` configuration file. Instead of using the `sqlite` setting described above, use something in the lines of the following:

```
DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'gbkfit_dev',
    'USER': 'django',
    'PASSWORD': 'test-docker_#1',
    'HOST': 'db',
    'PORT': 3306,
    }
}
```

The user and password information should be in accordance with the information provided in the file `docker-compose.yml` included at the root of the project repository. In particular, the content of `docker-compose.yml` should look something like this: 

```
version: '3'

services:
  db:
    image: mysql
    environment:
      MYSQL_ROOT_PASSWORD: example
      MYSQL_DATABASE: gbkfit_dev
      MYSQL_USER: django
      MYSQL_PASSWORD: test-docker_#1
  web:
    build: ./
    command: python3 development-manage.py runserver 0.0.0.0:8000
    volumes:
      - ./:/code
    ports:
      - "8000:8000"
    depends_on:
      - db
```

This file defines two modules: `db` (the database) and `web` (the gbkfit website).

From there, the website can be set and run using docker and docker-compose. 

##### Build:
`docker-compose build -f path/to/docker-compose.yml`

##### Run:
`docker-compose up -f path/to/docker-compose.yml`

##### Stop:
`docker-compose down -f path/to/docker-compose.yml`

##### Building one specific container only 
`docker-compose build web`

### Execute common Django actions with docker-compose

When a model is modified, or when running the server for the first time, one needs to make migrations, and migrate the database so the web application and the database are in sync with one another.

##### Make migrations:
`python development-manage.py makemigrations`

##### Migrate:
`python development-manage.py migrate`

##### Create a super user:
`python development-manage.py createsuperuser`

Using docker, this is still done via these commands. The main difference is the need to connect to the docker process, like so: 

##### 1. start the web server and database:
`docker-compose up -f path/to/docker-compose.yml -d` 

> Note the `-d` to run the processes in detached mode. 

##### 2. Display docker running containers :
`docker ps`

which results in something like:
```
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
040b6ee54f20        adacsgbkfit_web     "python3 developme..."   3 seconds ago       Up 2 seconds        0.0.0.0:8000->8000/tcp   adacsgbkfit_web_1
9a5542872556        mysql               "docker-entrypoint..."   4 seconds ago       Up 3 seconds        3306/tcp                 adacsgbkfit_db_1
```

##### 3. Find the container id of the web application and log into it:
`docker exec -t -i 040b6ee54f20 bash`

##### 4. Now that you are logged in, go to the right folder and act as usual.

e.g. `python development-manage.py makemigrations`
...

