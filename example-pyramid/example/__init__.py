import sys

from sqlalchemy import engine_from_config

from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from social_pyramid.models import init_social

from common import filters

from .models import DBSession, Base

import settings as app_settings
import local_settings as app_local_settings


def url_for(name, **kwargs):
    if name == 'social:begin':
        url = '/login/{backend}/'
    elif name == 'social:complete':
        url = '/complete/{backend}/'
    elif name == 'social:disconnect':
        url = '/disconnect/{backend}/'
    elif name == 'social:disconnect_individual':
        url = '/disconnect/{backend}/{association_id}/'
    else:
        url = name
    return url.format(**kwargs)


def get_settings(module):
    return { key: value for key, value in module.__dict__.items()
              if key not in module.__builtins__ and
                 key not in ['__builtins__', '__file__'] }


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    session_factory = UnencryptedCookieSessionFactoryConfig('thisisasecret')
    settings['jinja2.globals'] = {
        'url': url_for
    }
    settings['jinja2.filters'] = {
        'backend_name': filters.backend_name,
        'backend_class': filters.backend_class,
        'icon_name': filters.icon_name,
        'social_backends': filters.social_backends,
        'legacy_backends': filters.legacy_backends,
        'oauth_backends': filters.oauth_backends,
        'filter_backends': filters.filter_backends,
        'slice_by': filters.slice_by
    }
    config = Configurator(settings=settings,
                          session_factory=session_factory,
                          autocommit=True)
    config.include('pyramid_chameleon')
    config.include('pyramid_jinja2')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_request_method('example.auth.get_user', 'user', reify=True)
    config.add_route('home', '/')
    config.add_route('done', '/done')

    config.registry.settings.update(get_settings(app_settings))
    config.registry.settings.update(get_settings(app_local_settings))

    config.include('social_pyramid')

    init_social(config, Base, DBSession)

    config.scan()
    config.scan('social_pyramid')
    return config.make_wsgi_app()
