from social_core.backends.google import GooglePlusAuth
from social_core.backends.utils import load_backends


def is_authenticated(user):
    if callable(user.is_authenticated):
        return user.is_authenticated()
    else:
        return user.is_authenticated


def associations(user):
    return list(user.social_auth)


def common_context(authentication_backends, user=None, plus_id=None, **extra):
    """Common view context"""
    context = {
        'user': user,
        'available_backends': load_backends(authentication_backends),
        'associated': {}
    }

    if user and is_authenticated(user):
        context['associated'] = dict((association.provider, association)
                                     for association in associations(user))

    if plus_id:
        context['plus_id'] = plus_id
        context['plus_scope'] = ' '.join(GooglePlusAuth.DEFAULT_SCOPE)

    return dict(context, **extra)
