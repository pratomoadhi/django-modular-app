#!/bin/sh
set -e

echo "=== Running migrations ==="
python manage.py migrate

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

echo "=== Setting up roles ==="
python manage.py setup_roles

echo "=== Creating superuser ==="
python manage.py createsuperuser

echo "=== Release tasks completed ==="
