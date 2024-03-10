from common.utils import common_context
from pyramid.view import view_config
from social_pyramid.utils import load_strategy

from .auth import get_user


@view_config(route_name="home", renderer="common:templates/home.jinja2")
def home(request):
    return common_context(
        request.registry.settings["SOCIAL_AUTH_AUTHENTICATION_BACKENDS"],
        load_strategy(request),
        user=get_user(request),
        plus_id=request.registry.settings.get("SOCIAL_AUTH_GOOGLE_PLUS_KEY"),
    )


@view_config(route_name="done", renderer="common:templates/home.jinja2")
def done(request):
    return common_context(
        request.registry.settings["SOCIAL_AUTH_AUTHENTICATION_BACKENDS"],
        load_strategy(request),
        user=get_user(request),
    )


@view_config(  # fix: skip
    route_name="email_required",  # fix: skip
    renderer="common:templates/home.jinja2"  # fix: skip
)
def email_required(request):
    strategy = load_strategy(request)
    partial_token = request.GET.get("partial_token")
    partial = strategy.partial_load(partial_token)
    return common_context(
        request.registry.settings["SOCIAL_AUTH_AUTHENTICATION_BACKENDS"],
        strategy,
        user=get_user(request),
        plus_id=request.registry.settings["SOCIAL_AUTH_GOOGLE_PLUS_KEY"],
        email_required=True,
        partial_backend_name=partial.backend,
        partial_token=partial_token,
    )
