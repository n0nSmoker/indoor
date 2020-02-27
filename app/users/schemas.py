from webargs import fields, validate, ValidationError
from webargs.fields import ma
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import validates_schema
from marshmallow.validate import Length

from app.common.schemas import FilterSchema, SuccessListSchema, sort_one_of
from app.users.constants import ROLES, ROLE_ADMIN, ROLE_MANAGER, ROLE_USER, STATUSES
from app.users.models import User


class FilterUsersSchema(FilterSchema):
    sort_by = fields.Str(
        validate=sort_one_of([
            'id', 'name', 'email', 'role', 'status', 'created_at', 'updated_at',
        ]),
        missing='-created_at'
    )
    query = fields.Str(validate=Length(min=3, max=100), missing=None)
    role = fields.Str(validate=validate.OneOf([r[0] for r in ROLES]), missing=None)
    status = fields.Str(validate=validate.OneOf([s[0] for s in STATUSES]), missing=None)


class UserSchema(ModelSchema):
    class Meta:
        model = User
        exclude = ['password']


class UserListSchema(SuccessListSchema):
    results = fields.List(fields.Nested(UserSchema()))


class PublisherChecks:
    @validates_schema
    def check_publisher(self, data, **_):  # noqa
        role = data['role']
        publisher_id = data['publisher_id']

        if role == ROLE_MANAGER and not publisher_id:
            raise ValidationError(
                f'Required for role {ROLE_MANAGER}',
                field_name='publisher_id',
            )

        if role == ROLE_ADMIN and publisher_id:
            raise ValidationError(
                f'Shouldn\'t be filled for role {ROLE_ADMIN}',
                field_name='publisher_id',
            )


class AddUserSchema(ma.Schema, PublisherChecks):
    name = fields.Str(validate=validate.Length(min=1, max=100), required=True)
    email = fields.Str(validate=validate.Email(), required=True)
    password = fields.Str(validate=validate.Length(min=6, max=100), required=True)
    role = fields.Str(validate=validate.OneOf([r[0] for r in ROLES]), missing=ROLE_USER)
    publisher_id = fields.Integer(missing=None)


class UpdateUserSchema(ma.Schema, PublisherChecks):
    name = fields.Str(validate=validate.Length(min=1, max=100), missing=None)
    email = fields.Str(validate=validate.Email(), missing=None)
    role = fields.Str(validate=validate.OneOf([r[0] for r in ROLES]), missing=None)
    publisher_id = fields.Integer(missing=None)

    @validates_schema
    def check_all(self, data, **_):  # noqa
        if not any([v for v in data.values()]):
            raise ValidationError('All fields are empty')


class LoginUserSchema(ma.Schema):
    email = fields.Str(validate=validate.Email(), required=True)
    password = fields.Str(validate=validate.Length(max=100), required=True)
