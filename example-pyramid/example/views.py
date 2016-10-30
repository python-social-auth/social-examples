from pyramid.view import view_config

from common.utils import common_context

from .auth import get_user


@view_config(route_name='home', renderer='common:templates/home.jinja2')
def home(request):
    return common_context(
        request.registry.settings['SOCIAL_AUTH_AUTHENTICATION_BACKENDS'],
        user=get_user(request),
        plus_id=request.registry.settings.get(
            'SOCIAL_AUTH_GOOGLE_PLUS_KEY'
        ),
    )


@view_config(route_name='done', renderer='common:templates/home.jinja2')
def done(request):
    return common_context(
        request.registry.settings['SOCIAL_AUTH_AUTHENTICATION_BACKENDS'],
        user=get_user(request),
        plus_id=request.registry.settings['SOCIAL_AUTH_GOOGLE_PLUS_KEY'],
    )
