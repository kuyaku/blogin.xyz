# Procfile

web: python manage.py makemigrations users && python manage.py makemigrations blogs && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn blogin_project.wsgi
