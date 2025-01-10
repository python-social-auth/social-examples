from common import filters, utils
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from social_pyramid.models import init_social
from sqlalchemy import engine_from_config

import example.local_settings as app_local_settings
import example.settings as app_settings

from .models import Base, DBSession


def get_settings(module):
    not_in_filters = ["__builtins__", "__file__"]
    return {
        key: value
        for key, value in module.__dict__.items()
        if key not in module.__builtins__ and key not in not_in_filters
    }


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    engine = engine_from_config(settings, "sqlalchemy.")
    DBSession.bind = engine
    Base.metadata.bind = engine
    session_factory = SignedCookieSessionFactory("thisisasecret")
    settings["jinja2.globals"] = {"url": utils.url_for}
    settings["jinja2.filters"] = {
        "backend_name": filters.backend_name,
        "backend_class": filters.backend_class,
        "icon_name": filters.icon_name,
        "social_backends": filters.social_backends,
        "legacy_backends": filters.legacy_backends,
        "oauth_backends": filters.oauth_backends,
        "filter_backends": filters.filter_backends,
        "slice_by": filters.slice_by,
    }
    config = Configurator(
        settings=settings, session_factory=session_factory, autocommit=True
    )
    config.include("pyramid_chameleon")
    config.include("pyramid_jinja2")

    config.add_static_view("static", "static", cache_max_age=3600)
    config.add_request_method("example.auth.get_user", "user", reify=True)
    config.add_route("home", "/")
    config.add_route("done", "/done")
    config.add_route("email_required", "/email")

    config.registry.settings.update(get_settings(app_settings))
    config.registry.settings.update(get_settings(app_local_settings))

    config.include("social_pyramid")

    init_social(config, Base, DBSession)

    config.scan()
    config.scan("social_pyramid")
    return config.make_wsgi_app()
