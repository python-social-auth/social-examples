import os
import sys

import cherrypy
import settings
from common import filters
from common.utils import common_context, url_for
from jinja2 import Environment, FileSystemLoader
from social_cherrypy.utils import backends, load_strategy
from social_cherrypy.views import CherryPyPSAViews
from social_core.utils import setting_name

from .db.saplugin import SAEnginePlugin
from .db.satool import SATool
from .db.user import User

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_NAME = "sqlite:///{dbname}".format(dbname=os.path.join(BASE_DIR, "db.sqlite3"))

SAEnginePlugin(cherrypy.engine, DATABASE_NAME).subscribe()


class PSAExample(CherryPyPSAViews):
    @cherrypy.expose
    def index(self):
        return self.render_home()

    @cherrypy.expose
    def done(self):
        return self.render_home()

    @cherrypy.expose
    def logout(self):
        raise cherrypy.HTTPRedirect("/")

    def render_home(self):
        context = common_context(
            cherrypy.config[setting_name("AUTHENTICATION_BACKENDS")],
            load_strategy(),
            user=getattr(cherrypy.request, "user", None),
            plus_id=cherrypy.config.get(setting_name("SOCIAL_AUTH_GOOGLE_PLUS_KEY")),
        )
        return cherrypy.tools.jinja2env.get_template("home.html").render(**context)


def load_user():
    user_id = cherrypy.session.get("user_id")
    if user_id:
        cherrypy.request.user = cherrypy.request.db.query(User).get(user_id)
    else:
        cherrypy.request.user = None


def session_commit():
    cherrypy.session.save()


def get_settings(module):
    return {
        key: value
        for key, value in module.__dict__.items()
        if key not in module.__builtins__ and key not in ["__builtins__", "__file__"]
    }


SOCIAL_SETTINGS = get_settings(settings)

try:
    import local_settings

    SOCIAL_SETTINGS.update(get_settings(local_settings))
except ImportError:
    raise RuntimeError(
        "Define a local_settings.py using " "local_settings.py.template as base"
    )


def run_app(listen_address="0.0.0.0:8001"):
    host, port = listen_address.rsplit(":", 1)
    cherrypy.config.update(
        {
            "server.socket_port": int(port),
            "server.socket_host": host,
            "tools.sessions.on": True,
            "tools.sessions.storage_type": "ram",
            "tools.db.on": True,
            "tools.authenticate.on": True,
            "SOCIAL_AUTH_USER_MODEL": "example.db.user.User",
            "SOCIAL_AUTH_LOGIN_URL": "/",
            "SOCIAL_AUTH_LOGIN_REDIRECT_URL": "/done",
        }
    )
    cherrypy.config.update(SOCIAL_SETTINGS)
    cherrypy.tools.jinja2env = Environment(
        loader=FileSystemLoader(os.path.join(BASE_DIR, "common", "templates"))
    )
    cherrypy.tools.jinja2env.filters.update(
        {
            "backend_name": filters.backend_name,
            "backend_class": filters.backend_class,
            "icon_name": filters.icon_name,
            "social_backends": filters.social_backends,
            "legacy_backends": filters.legacy_backends,
            "oauth_backends": filters.oauth_backends,
            "filter_backends": filters.filter_backends,
            "slice_by": filters.slice_by,
        }
    )
    cherrypy.tools.jinja2env.globals.update({"url": url_for})
    cherrypy.tools.db = SATool()
    cherrypy.tools.authenticate = cherrypy.Tool("before_handler", load_user)
    cherrypy.tools.session = cherrypy.Tool("on_end_resource", session_commit)
    cherrypy.quickstart(PSAExample())
