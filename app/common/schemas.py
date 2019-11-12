from marshmallow.fields import String
from webargs import fields, validate
from flask import current_app as app

from lib.utils import hash_password


FILTER_SCHEMA = {
    'page': fields.Int(missing=1),
    'limit': fields.Int(missing=10),
    'sort_by': fields.Str(validate=validate.OneOf(['id', 'created_at', 'updated_at']), missing='created_at')
}


class PasswordField(String):
    def deserialize(self, value, attr=None, data=None):
        value = super().deserialize(value=value, attr=attr, data=data)
        if value:
            value = hash_password(
                salt=app.config['SECRET_KEY'],
                password=value
            )
        return value
