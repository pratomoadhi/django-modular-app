#!/bin/bash
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py setup_roles
python manage.py create_superuser