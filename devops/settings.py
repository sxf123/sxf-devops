"""
Django settings for devops project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import datetime
import ldap
from django_auth_ldap.config import LDAPSearch,LDAPSearchUnion,GroupOfNamesType,PosixGroupType
import djcelery

djcelery.setup_loader()
BROKER_URL = "redis://10.252.214.43:6379/0"
CELERY_TIMEZONE = "Asia/Shanghai"
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

AUTHENTICATION_BACKENDS = (
    "django_auth_ldap.backend.LDAPBackend",
    "django.contrib.auth.backends.ModelBackend",
)

AUTH_LDAP_SERVER_URI = "ldap://ldap.zhexinit.com"
AUTH_LDAP_BIND_DN="cn=songxiaofeng,ou=ProductRDCenter,dc=zhexinit,dc=com"
AUTH_LDAP_BIND_PASSWORD="Xiao!@34"
OU="DC=zhexinit,DC=com"
AUTH_LDAP_USER_SEARCH=LDAPSearch(OU,ldap.SCOPE_SUBTREE,"(uid=%(user)s)")
AUTH_LDAP_USER_ATTR_MAP={
    "first_name": "displayName",
    "last_name": "sn",
    "email": "mail"
}
#
AUTH_LDAP_GROUP_TYPE = PosixGroupType()
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=group,dc=zhexinit,dc=com",ldap.SCOPE_SUBTREE,"(objectClass=posixGroup)")
AUTH_LDAP_REQUIRE_GROUP = "cn=cmdb,ou=group,dc=zhexinit,dc=com"
# # AUTH_LDAP_MIRROR_GROUPS = True
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$jh$c^5!3!%&dhp%&-yu-fph5n&-ntjd8$pkbs)q*2nhedm41a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["10.100.119.36","127.0.0.1","10.100.243.9","dxops-test.dx-groups.com","10.100.122.236","dxops-dev.dx-groups.com"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'common',
    'cmdb',
    'rest_framework',
    'dxwf',
    'dj_pagination',
    'cmdbapi',
    'config_software',
    'deploy',
    'account',
    'ldapmanage',
    'djcelery'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'dj_pagination.middleware.PaginationMiddleware'
]

ROOT_URLCONF = 'devops.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'devops.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'devops',
        'USER': 'devops',
        'PASSWORD': 'devops',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS':{
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR,'static')

STATICFILES_DIRS = (
    ('assets',os.path.join(STATIC_ROOT,'assets').replace('\\', '/')),
    ('plugin',os.path.join(STATIC_ROOT,'plugin').replace('\\','/'))
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SALT_REST_URL = "http://192.168.64.128:8888"
SALT_API_USER = "saltapi"
SALT_API_PASSWD = "saltapi"

LOGGING = {
    "version" : 1,
    "disable_existing_loggers" : False,
    "formatters" : {
        "standard" : {
            "format" : "%(levelname)s [ %(message)s] %(asctime)s %(pathname)s %(filename)s %(module)s %(funcName)s %(lineno)d"
        },
    },
    "handlers" : {
        "console" : {
            "level" : "INFO",
            "class" : "logging.StreamHandler",
            "formatter" : "standard"
        }
    },
    "loggers" : {
        "default" : {
            "handlers" : ["console"],
            "level" : "INFO",
            "propagate" : True
        },
        "django_auth_ldap":{
            "handlers":["console"],
            "level":"DEBUG",
            "propatage":True,
        }
    }
}

DEFAUTL_LOGGER = "django_auth_ldap"

# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES':(
#         'rest_framework.permissions.IsAuthenticated',
#     ),
#     'DEFAULT_AUTHENTICATION_CLASSES':(
#         'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
#     )
# }

JWT_AUTH = {
    "JWT_EXPRATION_DELTA": datetime.timedelta(seconds=3600),
}

DISCONF_URL = "http://10.100.246.23:8000"
DISCONF_USER = "admin"
DISCONF_PASSWORD = "jcsz#system1OF"

GITLAB_URL = "http://10.100.243.17"
GITLAB_TOKEN = "GTjuzMesS7Fgwih-L9tr"

DNS_CONF_FILE = "/var/named/dx-groups.com.zone"
DNS_SERVER = "dxsz-pro-ops-dns01"

REDIS_HOST = "192.168.64.128"
REDIS_PORT = 6379

DXWF_PKG_DIR = "/root/projdir"

GET_JAVA_PROCESS_SCRIPT = "salt://scripts/get_jvm_process.sh"

JENKINS_USER = "songxiaofeng"
JENKINS_TOKEN = "5dd2e8a1150295b48d234be65a41badb"
JENKINS_URL = "http://10.252.214.43:8080"

DEPLOY_UPLOAD_PATH = os.path.join(os.path.join(BASE_DIR,"deploy"),"uploadfile")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = "it@zhexinit.com"
EMAIL_HOST_PASSWORD = "zGRZENTgjJ1v"
DEFAULT_FROM_MAIL = "it@zhexinit.com"

ZABBIX_URL = "http://121.40.237.72/zabbix"
ZABBIX_URL_VPC = "http://121.196.197.17:880/zabbix"
ZABBIX_USER = "songxiaofeng"
ZABBIX_PASSWORD = "songxiaofeng123"