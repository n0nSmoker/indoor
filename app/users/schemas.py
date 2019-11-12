from webargs import fields, validate

from app.common.schemas import FILTER_SCHEMA
from app.users.constants import ROLES, ROLE_USER


FILTER_USERS_SCHEMA = {
    **FILTER_SCHEMA,
    'sort_by': fields.Str(
        validate=validate.OneOf(
            ['id', 'name', 'email', 'role', 'created_at', 'updated_at']),
        missing='created_at'
    )

}

ADD_USER_SCHEMA = {
    'name': fields.Str(validate=validate.Length(min=1, max=100), required=True),
    'email': fields.Str(validate=validate.Email(), required=True),
    'password': fields.Str(validate=validate.Length(min=6, max=100), required=True),
    'role': fields.Str(validate=validate.OneOf([r[0] for r in ROLES]), missing=ROLE_USER)
}

UPDATE_USER_SCHEMA = {
    'name': fields.Str(validate=validate.Length(min=1, max=100), missing=None),
    'email': fields.Str(validate=validate.Email(), missing=None),
    'role': fields.Str(validate=validate.OneOf([r[0] for r in ROLES]), missing=None)
}

LOGIN_USER_SCHEMA = {
    'email': fields.Str(validate=validate.Email(), required=True),
    'password': fields.Str(validate=validate.Length(min=6, max=100), required=True),
}
