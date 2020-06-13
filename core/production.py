# -*- coding: utf-8 -*-
# core/production.py

import dj_database_url
from core.settings import *

DEBUG = TEMPLATE_DEBUG = False

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()

#  Add configuration for static files storage using whitenoise

ALLOWED_HOSTS = ['*']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
