# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Changed

- Split from the monolitic [python-social-auth](https://github.com/omab/python-social-auth)
  codebase
- Use host 0.0.0.0 for test servers
- Fix bug with example-flask-peewee import
- Fix bug with example-cherrypy import (Specify parent package name when importing setting, local_setting modules)
- Changed the DB session creation, DB connection closing, and DB model creation to align with SQLAlchemy 2. (for example-flask program)
- Removed flask-script package from requirements.txt as it doesn't work with recent flasks (programs: example-flask, example-flask-mongoengine, example-flask-peewee)
- Configured the manage.py file to use the CLI environment built into flask (programs: example-flask, example-flask-mongoengine, example-flask-peewee) as the flask-script package has been removed
- Changed the part that binds the DB session to comply with SQLAlchemy 2 (for example-pyramid program)
- Changed the part that fetches authenticated users from DB to be SQLAlchemy 2 based (for example-pyramid program)
- Removed all entries in the SOCIAL_AUTH_KEYS dictionary in local_settings.py.template into a single variable (tests showed that adding provider-supplied key information in SOCIAL_AUTH_KEYS caused errors on social login) (for example-pyramid program)
- Changed the DB model creation part. (for example-pyramid program)
- Error occurred when social login integration was completed because it was supposed to find google plus ID in the redirected URL. google plus is discontinued, so delete the part that gets plus ID. (for example-pyramid program)
- Changed the part that binds the DB session and creates the Base Model class to comply with SQLAlchemy 2 (for example-tornado, example-webpy program)
- Added local_settings.py.template file to reference other programs to easily generate local_settings.py (for example-tornado, example-webpy program)
- Fixed an error importing the local_settings module from settings.py (for the example-tornado program)
- Change the declaration of the Model class based on SQLAlchemy 2 (corresponds to the example-tornado, example-webpy program)
- Fix bug with example-webpy import
- Separated AUTHENTICATION_BACKENDS and PIPELINE entries into separate settings.py entries as web.config entries in app.py (for example-webpy program)
