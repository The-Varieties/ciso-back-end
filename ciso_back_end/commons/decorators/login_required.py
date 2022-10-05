import functools

from rest_framework.exceptions import NotAuthenticated


def login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if "Authorization" in request.headers:
            return view_func(request, *args, **kwargs)
        raise NotAuthenticated(detail="Need to login")

    return wrapper
