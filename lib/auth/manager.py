import logging

from flask import _request_ctx_stack, current_app, request
from werkzeug.local import LocalProxy


logger = logging.getLogger('auth')


class AuthManager:
    def __init__(self, app, get_user_func, get_device_func):
        """
        Init auth manager
        :param app:
        :param get_user_func: function which returns user instance by id
        :param get_device_func: function which returns device instance by token
        """
        app.auth_manager = self
        self.get_user_func = get_user_func
        self.get_device_func = get_device_func
        self.cache = app.cache
        self.cookie_name = app.config['AUTH_COOKIE_NAME']
        self.token_header_name = app.config['AUTH_TOKEN_HEADER_NAME']

    def get_user(self):
        if not hasattr(_request_ctx_stack.top, 'user'):
            user = None
            token = None
            if self.cookie_name in request.cookies:
                token = request.cookies.get(self.cookie_name)

            if token:
                user_id = self.cache.get_user_id(token)
                if user_id:
                    user = self.get_user_func(user_id)

            _request_ctx_stack.top.user = user

        return _request_ctx_stack.top.user

    def get_device(self):
        if not hasattr(_request_ctx_stack.top, 'device'):
            device = None
            token = request.headers.get(self.token_header_name)

            if token:
                device = self.get_device_func(token)

            _request_ctx_stack.top.device = device

        return _request_ctx_stack.top.device


class AuthException(Exception):
    pass


current_user = LocalProxy(lambda: current_app.auth_manager.get_user())  # pylint: disable=unnecessary-lambda
current_device = LocalProxy(lambda: current_app.auth_manager.get_device())  # pylint: disable=unnecessary-lambda
