#!/usr/bin/env bash

set -e
set -x

cd /django-docker
bash ./wait-for-it.sh --timeout=30 ${DB_HOST}:${DB_PORT}
# The following has been set up for testing reasons, NEVER should prod run
# with runserver --insecure
# This would need to be run with a proper server, this is done for testing purposes only
# https://docs.djangoproject.com/en/2.2/ref/contrib/staticfiles/
python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:${DJANGO_PORT} --insecure
