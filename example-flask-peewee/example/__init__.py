import os

from flask import Flask, g, url_for
from flask_login import LoginManager, current_user

from peewee import SqliteDatabase

from common import filters
from common.utils import common_context, url_for as common_url_for

from social_flask.utils import load_strategy
from social_flask.routes import social_auth
from social_flask.template_filters import backends
from social_flask_peewee.models import init_social

from .models.user import database_proxy, User


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# App
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'common', 'templates')
)
app.config.from_object('example.settings')

try:
    app.config.from_object('example.local_settings')
except ImportError:
    pass

# DB
database = SqliteDatabase(app.config['DATABASE_URI'])
database_proxy.initialize(database)

app.register_blueprint(social_auth)
init_social(app, database)

login_manager = LoginManager()
login_manager.login_view = 'main'
login_manager.login_message = ''
login_manager.init_app(app)

from example import models
from example import routes


@login_manager.user_loader
def load_user(userid):
    try:
        return User.get(User.id == userid)
    except User.DoesNotExist:
        pass


@app.before_request
def global_user():
    # evaluate proxy value
    g.user = current_user._get_current_object()


@app.context_processor
def inject_user():
    try:
        return {'user': g.user}
    except AttributeError:
        return {'user': None}


@app.context_processor
def load_common_context():
    return common_context(
        app.config['SOCIAL_AUTH_AUTHENTICATION_BACKENDS'],
        load_strategy(),
        getattr(g, 'user', None),
        app.config.get('SOCIAL_AUTH_GOOGLE_PLUS_KEY')
    )

app.context_processor(backends)
app.jinja_env.filters['backend_name'] = filters.backend_name
app.jinja_env.filters['backend_class'] = filters.backend_class
app.jinja_env.filters['icon_name'] = filters.icon_name
app.jinja_env.filters['social_backends'] = filters.social_backends
app.jinja_env.filters['legacy_backends'] = filters.legacy_backends
app.jinja_env.filters['oauth_backends'] = filters.oauth_backends
app.jinja_env.filters['filter_backends'] = filters.filter_backends
app.jinja_env.filters['slice_by'] = filters.slice_by
app.jinja_env.globals['url'] = common_url_for
