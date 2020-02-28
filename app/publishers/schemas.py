from webargs import fields, validate
from webargs.fields import ma
from marshmallow_sqlalchemy import ModelSchema

from app.common.schemas import FilterSchema, SuccessListSchema, sort_one_of
from app.publishers.models import Publisher


class FilterPublishersSchema(FilterSchema):
    sort_by = fields.Str(
        validate=sort_one_of(['id', 'name', 'airtime', 'comment', 'created_at', 'updated_at']),
        missing='created_at'
    )
    query = fields.Str(validate=validate.Length(min=3, max=100), missing=None)
    query_fields = fields.List(
        fields.Str(),
        validate=validate.ContainsOnly(
            ['name', 'comment']),
        missing=['name', 'comment']
    )


class PublisherSchema(ModelSchema):
    class Meta:
        model = Publisher
        exclude = ['created_by']


class PublisherListSchema(SuccessListSchema):
    results = fields.List(fields.Nested(PublisherSchema()))


class AddPublisherSchema(ma.Schema):
    name = fields.Str(validate=validate.Length(min=1, max=100), required=True)
    comment = fields.Str(validate=validate.Length(min=1, max=1024), missing=None)
    airtime = fields.Number(validate=validate.Range(min=.1, max=100), missing=None)


class UpdatePublisherSchema(AddPublisherSchema):
    pass
