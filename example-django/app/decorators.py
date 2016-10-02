from functools import wraps

from django.shortcuts import render


def render_to(tpl):
    """Simple render_to decorator"""
    def decorator(func):
        """Decorator"""
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            """Rendering method"""
            out = func(request, *args, **kwargs)
            if isinstance(out, dict):
                out = render(request, tpl, out)
            return out
        return wrapper
    return decorator
