import contextlib
import re

from django import template
from social_core.backends.oauth import OAuthAuth

register = template.Library()

name_re = re.compile(r"([^O])Auth")


@register.filter
def backend_name(backend):
    name = backend.__class__.__name__
    name = name.replace("OAuth", " OAuth")
    name = name.replace("OpenId", " OpenId")
    name = name.replace("Sandbox", "")
    return name_re.sub(r"\1 Auth", name)


@register.filter
def backend_class(backend):
    return backend.name.replace("-", " ")


@register.filter
def icon_name(name):
    return {
        "stackoverflow": "stack-overflow",
        "google-oauth": "google",
        "google-oauth2": "google",
        "google-openidconnect": "google",
        "yahoo-oauth": "yahoo",
        "facebook-app": "facebook",
        "email": "envelope",
        "vimeo": "vimeo-square",
        "linkedin-oauth2": "linkedin",
        "vk-oauth2": "vk",
        "live": "windows",
        "username": "user",
    }.get(name, name)


@register.filter
def social_backends(backends):
    backends = [
        (name, backend)
        for name, backend in backends.items()
        if name not in ["username", "email"]
    ]
    backends.sort(key=lambda b: b[0])
    return [
        backends[n : n + 10]  # fix: skip
        for n in range(0, len(backends), 10)
    ]


@register.filter
def legacy_backends(backends):
    backends = [
        (name, backend)
        for name, backend in backends.items()
        if name in ["username", "email"]
    ]
    backends.sort(key=lambda b: b[0])
    return backends


@register.filter
def oauth_backends(backends):
    backends = [
        (name, backend)
        for name, backend in backends.items()
        if issubclass(backend, OAuthAuth)
    ]
    backends.sort(key=lambda b: b[0])
    return backends


@register.simple_tag(takes_context=True)
def associated(context, backend):
    user = context.get("user")
    context["association"] = None
    if user and user.is_authenticated():
        associations = user.social_auth.filter(provider=backend.name)
        with contextlib.suppress(IndexError):
            context["association"] = associations[0]
    return ""
