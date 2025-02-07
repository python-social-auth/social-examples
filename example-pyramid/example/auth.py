from pyramid.events import BeforeRender, subscriber
from social_pyramid.utils import backends
from sqlalchemy import select

from example.models import DBSession, User


def login_user(backend, user, user_social_auth):
    backend.strategy.session_set("user_id", user.id)


def login_required(request):
    return getattr(request, "user", None) is not None


def get_user(request):
    user_id = request.session.get("user_id")
    return DBSession.scalar(select(User).where(User.id == user_id)) if user_id else None


@subscriber(BeforeRender)
def add_social(event):
    request = event["request"]
    event["social"] = backends(request, request.user)
