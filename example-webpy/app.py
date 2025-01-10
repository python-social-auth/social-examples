import os

import web
from common import filters
from common.utils import common_context, url_for
from example import local_settings, settings
from social_core.utils import setting_name
from social_webpy import app as social_app
from social_webpy.utils import load_strategy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from web.contrib.template import render_jinja

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

web.config.debug = False
web.config[setting_name("USER_MODEL")] = "models.User"
web.config[setting_name("AUTHENTICATION_BACKENDS")] = (
    settings.SOCIAL_AUTH_AUTHENTICATION_BACKENDS
)
web.config[setting_name("PIPELINE")] = settings.SOCIAL_AUTH_PIPELINE

for name, value in local_settings.__dict__.items():
    if name.startswith("SOCIAL_AUTH"):
        web.config[name] = value

web.config[setting_name("LOGIN_REDIRECT_URL")] = "/done/"

urls = (
    "^/$",
    "main",
    "^/done/?$",
    "done",
    "^/email/?$",
    "email",
    "",
    social_app.app_social,
)

render = render_jinja(os.path.join(BASE_DIR, "common", "templates"))
render._lookup.filters.update(
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
render._lookup.globals.update({"url": url_for})


class AppBaseView(social_app.BaseViewClass):
    def render_home(self, **extra):
        context = common_context(
            web.config[setting_name("AUTHENTICATION_BACKENDS")],
            load_strategy(),
            user=self.get_current_user(),
            **extra,
        )
        return render.home(**context)


class main(AppBaseView):
    def GET(self):
        return self.render_home()


class done(AppBaseView):
    def GET(self):
        return self.render_home()


class email(AppBaseView):
    def GET(self):
        strategy = load_strategy()
        partial_token = web.input(_method="get").get("partial_token")
        partial = strategy.partial_load(partial_token)
        return self.render_home(
            email_required=True,
            partial_backend_name=partial.backend,
            partial_token=partial_token,
        )


engine = create_engine("sqlite:///db.sqlite3")


def load_sqla(handler):
    web.ctx.orm = Session(engine)
    try:
        return handler()
    except web.HTTPError:
        web.ctx.orm.commit()
        raise
    except Exception:
        web.ctx.orm.rollback()
        raise
    finally:
        web.ctx.orm.commit()


app = web.application(urls, locals())
app.add_processor(load_sqla)
session = web.session.Session(
    app, web.session.DiskStore(os.path.join(BASE_DIR, "sessions"))
)

web.db_session = Session(engine)
web.web_session = session
