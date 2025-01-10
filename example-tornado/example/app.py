import os

import tornado.options
import tornado.web
from common import filters
from common.utils import common_context, url_for
from jinja2 import Environment, FileSystemLoader
from social_tornado.routes import SOCIAL_AUTH_ROUTES
from social_tornado.utils import load_strategy
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from tornado_jinja2 import Jinja2Loader

from example import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_NAME = "sqlite:///{dbname}".format(  # fix: skip
    dbname=os.path.join(BASE_DIR, "db.sqlite3")
)

engine = create_engine(DATABASE_NAME, echo=False)
session = Session(engine)


class Base(DeclarativeBase):
    pass


class BaseHandler(tornado.web.RequestHandler):
    def render_home(self, **extra):
        from example.models import User

        user_id = self.get_secure_cookie("user_id")

        if user_id:
            user = session.get(User, int(user_id))
        else:
            user = None

        context = common_context(
            settings.SOCIAL_AUTH_AUTHENTICATION_BACKENDS,
            load_strategy(self),
            user=user,
            plus_id=getattr(settings, "SOCIAL_AUTH_GOOGLE_PLUS_KEY", None),
            **extra,
        )

        self.render("home.html", **context)


class MainHandler(BaseHandler):
    def get(self):
        self.render_home()


class DoneHandler(BaseHandler):
    def get(self):
        self.render_home()


class EmailRequiredHandler(BaseHandler):
    def get(self):
        strategy = load_strategy(self)
        partial_token = self.request.arguments.get("partial_token")
        partial = strategy.partial_load(partial_token)
        self.render_home(
            email_required=True,
            partial_backend_name=partial.backend,
            partial_token=partial_token,
        )


class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.request.redirect("/")


jinja2env = Environment(
    loader=FileSystemLoader(os.path.join(BASE_DIR, "common", "templates"))
)
jinja2env.filters.update(
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
jinja2env.globals.update({"url": url_for})
jinja2loader = Jinja2Loader(jinja2env)

tornado.options.parse_command_line()
tornado_settings = {
    k: getattr(settings, k) for k in dir(settings) if not k.startswith("__")
}
tornado_settings["template_loader"] = jinja2loader
application = tornado.web.Application(
    SOCIAL_AUTH_ROUTES
    + [
        (r"/", MainHandler),
        (r"/done/", DoneHandler),
        (r"/email", EmailRequiredHandler),
        (r"/logout/", LogoutHandler),
    ],
    cookie_secret="adb528da-20bb-4386-8eaf-09f041b569e0",
    **tornado_settings,
)
