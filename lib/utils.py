import hashlib
import inspect
import random
import re
import string

import simplejson as json

from flask import make_response, current_app
from flask_sqlalchemy import Model
from sqlalchemy.sql.schema import Table
from werkzeug.utils import find_modules, import_string


def get_url_map(app):
    url_map = dict()
    p = re.compile(r'(<[\w]+)|(>)')

    for u in app.url_map.iter_rules():
        route = p.sub('', u.rule)

        if '.' not in u.endpoint:
            url_map[u.endpoint] = route
            continue

        mod, name = u.endpoint.split('.')
        if not url_map.get(mod):
            url_map[mod] = {}
        url_map[mod][name] = route

    return url_map


class ApiException(Exception):
    def __init__(self, message, status=400):
        super().__init__()
        self.message = message
        self.status = status

    def to_result(self):
        return fail(self.message, status=self.status)


def find_models_and_tables():
    models_dict = {}
    for module_name in find_modules('app', include_packages=True):
        models_module = import_string('%s.models' % module_name, silent=True)
        if models_module:
            for name, item in models_module.__dict__.items():
                if (inspect.isclass(item) and Model in inspect.getmro(item)) \
                   or item.__class__ is Table:
                    models_dict[name] = item
    return models_dict


def setattrs(obj, ignore_nulls=False, **kwargs):
    """ Setting multiple object attributes at once """

    attrs = (a for a in dir(obj) if not a.startswith('_'))
    for attr in attrs:
        if attr in kwargs and (kwargs[attr] is not None and ignore_nulls or not ignore_nulls):
            setattr(obj, attr, kwargs[attr])


def jsonify(data):
    """
    Returns data wrapped in response class
    with corresponding mimetype (Uses default JSONIFY_MIMETYPE)
    :param any data:
    :return:
    """
    return current_app.response_class(
        json.dumps(data),
        mimetype=current_app.config["JSONIFY_MIMETYPE"],
    )


def success(data, headers=None, cookies=None):
    """
    Generates successful response
    :param data:
    :param headers:
    :param cookies:
    :return:
    """
    status = 200
    resp = make_response(jsonify(data), status)
    if cookies:
        assert isinstance(cookies, dict), 'Cookies should be a dict'
        for n, v in cookies.items():
            resp.set_cookie(key=n, value=v)

    if headers:
        assert isinstance(cookies, dict), 'Headers should be a dict'
        for h, v in headers.items():
            resp.headers[h] = v

    return resp


def fail(msg, status=400):
    """
    Generates json error msg
    :param msg: Error message(s)
    :param status: Status code
    :return:
    """
    if not isinstance(msg, list):
        msg = [msg]
    return make_response(jsonify({'errors': msg}), status)


def add_or_update_attr(func, param, value):
    assert 'dict' in str(type(value))
    try:
        param = getattr(func, param)
        param.update(value)
    except AttributeError:
        setattr(func, param, value)


def get_random_str(length=10, punctuation=False):
    """
    Generates random string of given length
    :param length:
    :param punctuation:
    :return:
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits + (string.punctuation if punctuation else ''), k=length))


def hash_password(salt, password):
    salted = (salt + password).encode()
    return hashlib.sha512(salted).hexdigest()
