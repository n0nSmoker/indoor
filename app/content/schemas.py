from webargs import fields
from webargs.fields import ma
from marshmallow_sqlalchemy import ModelSchema
from marshmallow.validate import Length

from app.common.schemas import FilterSchema, SuccessListSchema, sort_one_of
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


class UpdateFileSchema(ma.Schema):
    file = fields.Field(location='files', type='file', missing=None)
    comment = fields.Str(validate=Length(max=1024), missing=None)


class FileSchema(ModelSchema):
    class Meta:
        model = File


class FileListSchema(SuccessListSchema):
    results = fields.List(fields.Nested(FileSchema()))
