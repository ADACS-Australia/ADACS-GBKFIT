**Project Overview**
====================

The aim of the project is to facilitate user interface for GBKFIT-cloud 
where the users will be able to submit job requests that will be served 
by the GBKFIT-cloud. This project is currently made using the django 
framework.

# Prerequisites

- Python 3.6+
- MySQL 5.7+ (tested with 5.7)

Optional

- Docker and Docker-Compose (If you want to use skip manual setup steps and just want to run the UI as a
  docker container)

Setup
=====

## Configuration Steps

The required steps include the following:

- `virtualenv -p python3.6 venv` (create the virtual environment, e.g. with https://docs.python.org/3/library/venv.html or https://github.com/pyenv/pyenv)
- `git pull` (clone the code)
- `cd ADACS-GBKFIT` (enter to the directory)
- `git submodule foreach --recursive git pull origin master` (pulls any submodules (django_hpc_job_controller))
- `source ../venv/bin/activate` (activate the virtual environment)
- `cd gbkfit/settings` (enter the settings directory)
- `touch local.py` (create the file for local settings - refer to the Local Settings section for setting up a local settings file)
- `cd ../../` (enter the root directory of the project)
- `pip3 install -r requirements.txt` (install required python packages)
- `pip3 install -r django_hpc_job_controller/server/requirements.txt` (install required python packages for the django_hpc_job_controller server)
- `./development-manage.py migrate` (migrate, for staging or production)
- `./development-manage.py createsuperuser` (create an admin account) (specify the required manage.py file instead)
- `./development-manage.py runserver 8000` (running the server)

## Local Settings ##
The project is required to have customised machine specific settings.
Those settings need to included or overridden in the local settings file.
Create one `local.py` in the settings module next to the other settings
files (`base.py`, `development.py`, `production.py` etc.)

The following settings needs to be present in the `local.py` settings file.

Specify the base and media directories:
```python
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_URL = '/media/'   # The media URL
MEDIA_ROOT = '/data/'   # The location on disk, set this to the location of the shared mounted filesystem
```

The secret key used to authenticate the workflow with the UI API
```python
WORKFLOW_SECRET = 'some really long string with $YMb0l$'
```

You should also specify where to which page a user should be redirected after login in:

```python
LOGIN_REDIRECT_URL='/jobs'
```

Specify if the GBKFIT was configured with CUDA or OpenMP:

```python
OMP_OR_CUDA = 'cuda'
```
or 

```python
OMP_OR_CUDA = 'omp'
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
  nginx:
    image: nginx:latest
    container_name: ng01
    ports:
      - "8010:8000"
    volumes:
      - ./nginx/:/etc/nginx/conf.d
      - ./static:/static
    depends_on:
      - web
  db:
    image: mysql:5.7
    container_name: ms01
    environment:
      MYSQL_ROOT_PASSWORD: example
      MYSQL_DATABASE: gbkfit_dev
      MYSQL_USER: django
      MYSQL_PASSWORD: test-docker_#1
    volumes:
      - var_lib_mysql_gbkfit:/var/lib/mysql
  web:
    build: ./
    container_name: dg01
    command: bash -c "python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn gbkfit.wsgi -b 0.0.0.0:8000"
    ports:
      - "8000"
      - "8001"
    volumes:
      - ./:/code
      - ./static:/static
    depends_on:
      - db

volumes:
  var_lib_mysql_gbkfit:
```

This file defines three modules: `nginx` (the webserver), `db` (the database) and `web` (the gbkfit website).

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

## Local Job Submission Setup

Local job submission setup is relatively simple:

- Create a Python 3.6 virtual environment in the local `django_hpc_job_controller/client/venv` and install the client requirements as described in https://github.com/ADACS-Australia/django_hpc_job_controller#installation-steps
- Configure a new cluster in the Django admin that uses `localhost` for the host name as described in https://github.com/ADACS-Australia/django_hpc_job_controller#configure-a-cluster and also has the client path set to the absolute path to the job controller client folder, eg: `/home/user/projects/ADACS-SS18B-PLasky/django_hpc_job_controller/client`
- Copy the three files from `misc/job_controller_scripts/local/` to `django_hpc_job_controller/client/settings/`
- Configure the local submission script paths in `django_hpc_job_controller/client/settings/gbkfit_local.sh` to match the paths on your system.
- Configure the local job working directory (where job output folders will be created) in `django_hpc_job_controller/client/settings/local.py`, eg: `HPC_JOB_WORKING_DIRECTORY = '/home/user/gbkfit/jobs/'`
- Set up the `make_image` virtual environment
  - Change in to the make image source directory `misc/make_image/`
  - Create a python 2.7 virtual environment
    - `module load python/2.7.14`
    - `virtualenv -p python2.7 venv`
  - Activate the virtual environment `. venv/bin/activate`
  - Install the `make_image` requirements `pip install -r requirements.txt`

## Slurm Job Submission Setup

Slurm job submission is similar to the local job submission steps.

- Follow the client setup instructions in https://github.com/ADACS-Australia/django_hpc_job_controller#installation-steps on the remote cluster
- Configure a new cluster in the Django admin for the remote cluster as described in https://github.com/ADACS-Australia/django_hpc_job_controller#configure-a-cluster 
- Copy the three files from `misc/job_controller_scripts/slurm/` to `.../django_hpc_job_controller/client/settings/` on the remote cluster
- Configure the slurm submission script paths in `.../django_hpc_job_controller/client/settings/gbkfit_slurm.sh`, on the remote cluster, to match the correct paths on the remote cluster.
- Configure the slurm job working directory on the remote cluster (where job output folders will be created) in `.../django_hpc_job_controller/client/settings/local.py`, eg: `HPC_JOB_WORKING_DIRECTORY = '/home/user/gbkfit/jobs/'`
- Set up the `make_image` virtual environment
  - Change in to the make image source directory `misc/make_image/`
  - Create a python 2.7 virtual environment
    - `module load python/2.7.14`
    - `virtualenv -p python2.7 venv`
  - Activate the virtual environment `. venv/bin/activate`
  - Install the `make_image` requirements `pip install -r requirements.txt`

## Nginx Configuration

The Django server currently exports two ports, one for handling HTTP, and the other for handling Websocket connections. Typically, we would recommend running the web app with gunicorn in a production environment (as configured in the provided docker configurations). By default the Websocket server will listen on port 8001. For the Swinburne/OzSTAR deployment, we use an nginx reverse proxy to map the incoming Websocket connections on /ws/ to the websocket server, and all other requests are sent to the normal Django port.

The nginx config for our docker release at Swinburne looks like this:

```nginx
server {
  location /projects/gbkfit/live/static/ {
    autoindex on;
    alias /static/;
  }

  location /projects/gbkfit/live/ws/ {
    proxy_pass http://web:8001/;
 
    proxy_http_version  1.1;
    proxy_set_header    Upgrade $http_upgrade;
    proxy_set_header    Connection "upgrade";
    
    proxy_connect_timeout 7d;
    proxy_send_timeout 7d;
    proxy_read_timeout 7d;
  }

  location / {
    proxy_pass http://web:8000;
  }
 
  listen 8000;
  server_name localhost;
}
```

The connection upgrade configuration is very important for successful websocket connection.

