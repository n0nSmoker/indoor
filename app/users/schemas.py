from webargs import fields, validate, ValidationError
from webargs.fields import ma

from app.common.schemas import FilterSchema
from app.users.constants import ROLES, ROLE_USER


FilterUsersSchema = {
    **FilterSchema,
    'sort_by': fields.Str(
        validate=validate.OneOf(
            ['id', 'name', 'email', 'role', 'created_at', 'updated_at']),
        missing='created_at'
    )

}

AddUserSchema = {
    'name': fields.Str(validate=validate.Length(min=1, max=100), required=True),
    'email': fields.Str(validate=validate.Email(), required=True),
    'password': fields.Str(validate=validate.Length(min=6, max=100), required=True),
    'role': fields.Str(validate=validate.OneOf([r[0] for r in ROLES]), missing=ROLE_USER)
}


class UpdateUserSchema(ma.Schema):
    name = fields.Str(validate=validate.Length(min=1, max=100), missing=None)
    email = fields.Str(validate=validate.Email(), missing=None)
    role = fields.Str(validate=validate.OneOf([r[0] for r in ROLES]), missing=None)

    @ma.validates_schema()
    def check_all(self, data, **_):
        if not any([v for v in data.values()]):
            raise ValidationError('All fields are empty')


LoginUserSchema = {
    'email': fields.Str(validate=validate.Email(), required=True),
    'password': fields.Str(validate=validate.Length(min=6, max=100), required=True),
}
