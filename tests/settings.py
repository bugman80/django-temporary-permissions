import os

SITE_ID = 1
STATIC_URL = '/static/'
SECRET_KEY = ';klkj;okj;lkn;lklj;lkj;kjmlliuewhy2ioqwjdkh'
ALLOWED_HOSTS = ('127.0.0.1',)
PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)

AUTH_USER_MODEL = 'auth.User'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django_temporary_permissions',
    'tests',
)

AUTHENTICATION_BACKENDS = (
    'django_temporary_permissions.backends.TempPermissionsBackend',
)


# DATABASES
DATABASES_SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'HOST': '',
        'PORT': ''
    }
}

DATABASES_POSTGRES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dj_temp_perm',
        'HOST': '127.0.0.1',
        'PORT': '',
        'USER': 'postgres',
        'PASSWORD': '',
    },
}

db = os.environ.get('DBENGINE', 'postgres')

if db == 'sqlite':
    DATABASES = DATABASES_SQLITE
elif db == 'postgres':
    DATABASES = DATABASES_POSTGRES
else:
    raise Exception('Unknown database `%s`' % db)

print('\n# Using DATABASE.ENGINE={}'.format(DATABASES['default']['ENGINE']))


# MIDDLEWARE
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)-8s: %(asctime)s %(name)10s: %(funcName)40s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
}

MANAGE_ANONYMOUS_USER = True
ANONYMOUS_USERID = 0
