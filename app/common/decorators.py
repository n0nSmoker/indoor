from functools import wraps

from lib.auth import current_user
from lib.utils import fail

from app.users.constants import ROLE_ADMIN


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


def admin_required(fn):
    """
    Shortcut decorator checks that user is logged in and his role is admin
    :param fn:
    :return:
    """
    wrapper = check_auth(roles=[ROLE_ADMIN])
    return wrapper(fn)


def auth_required(fn):
    """
    Shortcut function to check if user is logged in
    :param fn:
    :return:
    """
    wrapper = check_auth()
    return wrapper(fn)
