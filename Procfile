web: gunicorn blog_project.wsgi
web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn blog_project.wsgi
