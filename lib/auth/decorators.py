from functools import wraps
from flask import request
from lib.auth.manager import current_device, current_user
from lib.utils import fail


def check_basic_auth(username, password):
    """
    Checks credentials for basic auth
    :param username:
    :param password:
    :return:
    """
    auth = request.authorization
    return bool(
        auth and
        auth.username == username and
        auth.password == password
    )


def basic_auth_decorator(username, password):
    """
    Returns decorator for basic auth
    :param str username: No basic auth if None
    :param str password:
    :return:
    """
    def decorator(f):
        """
        Checks if user is authenticated (Basic Auth)
        :param function f:
        :return:
        """
        @wraps(f)
        def wrapped_view(**kwargs):
            if username and not check_basic_auth(username, password):
                return ('Unauthorized', 401, {
                    'WWW-Authenticate': 'Basic realm="Login Required"'
                })

            return f(**kwargs)

        return wrapped_view
    return decorator


def check_auth(roles=None):
    """
    Adds auth check to view function
    :param roles: list of roles | None
    :return: wrapped function
    """
    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if not current_user or roles and current_user.role not in roles:
                return fail('Доступ запрещен', status=403)
            return fn(*args, **kwargs)
        return wrapped
    return wrapper


def check_device_auth():
    """
    Adds device auth check to view function
    :return: wrapped function
    """
    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if not current_device:
                return fail('Доступ запрещен', status=403)
            return fn(*args, **kwargs)
        return wrapped
    return wrapper
