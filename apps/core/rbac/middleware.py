from django.contrib.auth import get_user_model, logout
from apps.core.rbac.models import User
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import redirect
from re import compile
from django.conf import settings
from apps.core.rbac import models


EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]

if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]
    
class LoginRequiredMiddleware(MiddlewareMixin):
    """ Checking User authentication before serving response """
    def process_request(self, request):
        if request.user.is_anonymous:
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                return redirect(settings.LOGIN_URL)
        else:
            if not request.user.is_active:
                logout(request)
                path = request.path_info.lstrip('/')
                if not any(m.match(path) for m in EXEMPT_URLS):
                    return redirect(settings.LOGIN_URL)


def RequestExposerMiddleware(get_response):
    """ Pass request object to rbac.models """
    def middleware(request):
        models.exposed_request = request
        response = get_response(request)
        return response

    return middleware