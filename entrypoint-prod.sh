#!/usr/bin/env bash

set -e
set -x

bash wait-for-it.sh --timeout=30 ${DB_HOST}:${DB_PORT}
cd /django-docker && python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:80
