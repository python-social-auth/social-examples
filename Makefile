DEFAULT_IFACE := 0.0.0.0
DEFAULT_PORT := 8001

check-local-settings:
	@ test -f ${example_path}/local_settings.py || ( \
		echo "====================================================================\n"; \
		echo "         Missing ${example_path}/local_settings.py\n"; \
		echo "===================================================================="; \
		exit 1; \
	)

install-dependencies:
	@ pip install -r ${example_path}/requirements.txt

run-django:
	@ ${MAKE} check-local-settings example_path=example-django/example
	@ ${MAKE} install-dependencies example_path=example-django
	@ python example-django/manage.py migrate
	@ python example-django/manage.py runserver $(DEFAULT_IFACE):$(DEFAULT_PORT)

run-django-mongoengine:
	@ ${MAKE} check-local-settings example_path=example-django-mongoengine/example
	@ ${MAKE} install-dependencies example_path=example-django-mongoengine
	@ python example-django-mongoengine/manage.py migrate
	@ python example-django-mongoengine/manage.py runserver $(DEFAULT_PORT)

run-flask:
	@ ${MAKE} check-local-settings example_path=example-flask/example
	@ ${MAKE} install-dependencies example_path=example-flask
	@ python example-flask/manage.py syncdb
	@ python example-flask/manage.py runserver -h $(DEFAULT_IFACE) -p $(DEFAULT_PORT)

run-flask-peewee:
	@ ${MAKE} check-local-settings example_path=example-flask-peewee/example
	@ ${MAKE} install-dependencies example_path=example-flask-peewee
	@ python example-flask-peewee/manage.py syncdb
	@ python example-flask-peewee/manage.py runserver -h $(DEFAULT_IFACE) -p $(DEFAULT_PORT)

run-flask-mongoengine:
	@ ${MAKE} check-local-settings example_path=example-flask-mongoengine/example
	@ ${MAKE} install-dependencies example_path=example-flask-mongoengine
	@ python example-flask-mongoengine/manage.py runserver -h $(DEFAULT_IFACE) -p $(DEFAULT_PORT)

run-webpy:
	@ ${MAKE} check-local-settings example_path=example-webpy
	@ ${MAKE} install-dependencies example_path=example-webpy
	@ python example-webpy/manage.py syncdb
	@ python example-webpy/manage.py $(DEFAULT_IFACE):$(DEFAULT_PORT)

run-cherrypy:
	@ ${MAKE} check-local-settings example_path=example-cherrypy/example
	@ ${MAKE} install-dependencies example_path=example-cherrypy
	@ python example-cherrypy/manage.py syncdb
	@ python example-cherrypy/manage.py $(DEFAULT_IFACE):$(DEFAULT_PORT)

run-tornado:
	@ ${MAKE} check-local-settings example_path=example-tornado/example
	@ ${MAKE} install-dependencies example_path=example-tornado
	@ python example-tornado/manage.py syncdb
	python example-tornado/manage.py $(DEFAULT_IFACE):$(DEFAULT_PORT)

run-pyramid:
	@ ${MAKE} check-local-settings example_path=example-pyramid/example
	@ ${MAKE} install-dependencies example_path=example-pyramid
	@ cd example-pyramid && \
		python setup.py develop && \
		initialize_example_db development.ini && \
		pserve development.ini

clean:
	@ find . -name '*.py[co]' -delete
	@ find . -name '__pycache__' -delete
	@ find . -name '*.sqlite3' -delete
