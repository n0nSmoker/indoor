from webargs import fields, validate
from webargs.fields import ma


class FilterSchema(ma.Schema):
    page = fields.Int(missing=1, validate=validate.Range(min=1, max=100))
    limit = fields.Int(missing=10, validate=validate.Range(min=1, max=1000))
    sort_by = fields.Str(validate=validate.OneOf(['id', 'created_at', 'updated_at']), missing='created_at')


class FailSchema(ma.Schema):
    errors = fields.List(fields.Str())


class SuccessListSchema(ma.Schema):
    results = fields.List(fields.Raw())
    total = fields.Number()
