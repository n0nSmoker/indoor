from webargs import fields
from webargs.fields import ma
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import validates_schema
from marshmallow.validate import Length, OneOf, ValidationError

from app.common.schemas import FilterSchema, SuccessListSchema, sort_one_of
from app.publishers.schemas import PublisherSchema
from lib.auth.manager import current_user

from .constants import STATUSES, STATUS_CREATED, STATUS_MODERATION
from .models import File


class FilterFilesSchema(FilterSchema):
    sort_by = fields.Str(
        validate=sort_one_of(['id', 'name', 'created_at', 'comment']),
        missing='created_at'
    )
    query = fields.Str(validate=Length(min=2, max=100), missing=None)


class AddFileSchema(ma.Schema):
    file = fields.Field(location='files', type='file', required=True)
    comment = fields.Str(validate=Length(max=1024), missing=None)
    publisher_id = fields.Integer(missing=None)

    @validates_schema
    def check_publisher(self, data, **_):  # noqa
        if data['publisher_id']:
            if not current_user.is_admin:
                raise ValidationError('Shouldn\'t be filled', field_name='publisher_id')
        else:
            if current_user.is_admin:
                raise ValidationError('Required', field_name='publisher_id')


class UpdateFileSchema(ma.Schema):
    file = fields.Field(location='files', type='file', missing=None)
    comment = fields.Str(validate=Length(max=1024), missing=None)
    status = fields.Str(validate=OneOf([r[0] for r in STATUSES]), missing=None)

    @validates_schema
    def check_schema(self, data, **_):  # noqa
        if not any([v for v in data.values()]):
            raise ValidationError('All fields are empty')

        status = data['status']
        if status and not current_user.is_admin:
            if status not in [STATUS_CREATED, STATUS_MODERATION]:
                raise ValidationError(f'Status {status} not allowed', field_name='status')


class FileSchema(ModelSchema):
    publisher = fields.Nested(PublisherSchema, many=False)

    class Meta:
        model = File


class FileListSchema(SuccessListSchema):
    results = fields.List(fields.Nested(FileSchema()))
