import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login

from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_core.backends.google import GooglePlusAuth
from social_core.backends.utils import load_backends
from social_django.utils import psa

from .decorators import render_to


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')


@render_to('home.html')
def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return redirect('done')


@login_required
@render_to('home.html')
def done(request):
    """Login complete view, displays user data"""
    pass


@render_to('home.html')
def validation_sent(request):
    """Email validation sent confirmation page"""
    return {
        'validation_sent': True,
        'email': request.session.get('email_validation_address')
    }


@render_to('home.html')
def require_email(request):
    """Email required page"""
    backend = request.session['partial_pipeline']['backend']
    return {
        'email_required': True,
        'backend': backend
    }


@psa('social:complete')
def ajax_auth(request, backend):
    """AJAX authentication endpoint"""
    if isinstance(request.backend, BaseOAuth1):
        token = {
            'oauth_token': request.REQUEST.get('access_token'),
            'oauth_token_secret': request.REQUEST.get('access_token_secret'),
        }
    elif isinstance(request.backend, BaseOAuth2):
        token = request.REQUEST.get('access_token')
    else:
        raise HttpResponseBadRequest('Wrong backend type')
    user = request.backend.do_auth(token, ajax=True)
    login(request, user)
    data = {'id': user.id, 'username': user.username}
    return HttpResponse(json.dumps(data), mimetype='application/json')
