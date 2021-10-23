release: python manager/manage.py makemigrations
release: python manager/manage.py migrate --run-syncdb
web: gunicorn --pythonpath manager manager.wsgi