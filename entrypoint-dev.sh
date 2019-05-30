#!/usr/bin/env bash

set -e
set -x

ls
cd /django-docker
bash ./wait-for-it.sh --timeout=30 ${DB_HOST}:${DB_PORT}
python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:${DJANGO_PORT}