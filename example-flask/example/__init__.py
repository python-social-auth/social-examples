import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import Flask, g, url_for
from flask_login import LoginManager, current_user

from common import filters
from common.utils import common_context

from social_flask.routes import social_auth
from social_flask.template_filters import backends
from social_flask_sqlalchemy.models import init_social


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
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(Session)

app.register_blueprint(social_auth)
init_social(app, db_session)

login_manager = LoginManager()
login_manager.login_view = 'main'
login_manager.login_message = ''
login_manager.init_app(app)

from example import models
from example import routes


@login_manager.user_loader
def load_user(userid):
    try:
        return models.user.User.query.get(int(userid))
    except (TypeError, ValueError):
        pass


@app.before_request
def global_user():
    # evaluate proxy value
    g.user = current_user._get_current_object()


@app.teardown_appcontext
def commit_on_success(error=None):
    if error is None:
        db_session.commit()
    else:
        db_session.rollback()

    db_session.remove()


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
        getattr(g, 'user', None),
        app.config.get('SOCIAL_AUTH_GOOGLE_PLUS_KEY')
    )

@app.context_processor
def url_func():
    def url(endpoint, **kwargs):
        urls_mapping = {
            'social:begin': 'social.auth',
            'social:complete': 'social.complete',
            'social:disconnect_individual': 'social.disconnect'
        }
        endpoint = urls_mapping.get(endpoint, endpoint)
        return url_for(endpoint.replace(':', '.'), **kwargs)
    return { 'url': url }

app.context_processor(backends)
app.jinja_env.filters['backend_name'] = filters.backend_name
app.jinja_env.filters['backend_class'] = filters.backend_class
app.jinja_env.filters['icon_name'] = filters.icon_name
app.jinja_env.filters['social_backends'] = filters.social_backends
app.jinja_env.filters['legacy_backends'] = filters.legacy_backends
app.jinja_env.filters['oauth_backends'] = filters.oauth_backends
app.jinja_env.filters['filter_backends'] = filters.filter_backends
app.jinja_env.filters['slice_by'] = filters.slice_by
