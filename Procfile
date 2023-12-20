# Procfile

web: python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn blogin_project.wsgi
