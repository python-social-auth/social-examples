DEFAULT_IFACE := 0.0.0.0
DEFAULT_PORT := 8001

run-django:
	@ python example-django/manage.py migrate
	@ python example-django/manage.py runserver $(DEFAULT_PORT)

run-flask:
	@ python example-flask/manage.py syncdb
	@ python example-flask/manage.py runserver -p $(DEFAULT_PORT)

run-flask-peewee:
	@ python example-flask-peewee/manage.py syncdb
	@ python example-flask-peewee/manage.py runserver -p $(DEFAULT_PORT)

run-webpy:
	@ python example-webpy/manage.py syncdb
	@ python example-webpy/manage.py $(DEFAULT_IFACE):$(DEFAULT_PORT)

clean:
	@ find . -name '*.py[co]' -delete
	@ find . -name '__pycache__' -delete
	@ find . -name '*.sqlite3' -delete
