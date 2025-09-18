release: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py setup_roles && python .\manage.py create_superuser
web: gunicorn djapp.wsgi
