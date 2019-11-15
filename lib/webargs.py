"""Redefined FlaskParser handle_error here
because I suddenly realized that it works
weired in the last versions:
  - Doesn't return detailed error messages
  - Returns code 422 on missing field error instead 400

"""

from flask import abort
from webargs.flaskparser import FlaskParser

from lib.utils import fail


class Parser(FlaskParser):
    def handle_error(self, error, req, schema,
                     error_status_code, error_headers):
        response = fail(
            [f"Field:{k}. {' '.join(v)}" for k, v in error.messages.items()]
        )
        abort(response)


parser = Parser()
