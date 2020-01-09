from webargs import fields, validate
from webargs.fields import ma


class OSVersionSchema(ma.Schema):
    os_version = fields.Str(validate=validate.Length(min=1, max=1024), required=True)


class SoftwareVersionSchema(ma.Schema):
    software_version = fields.Str(validate=validate.Length(min=1, max=100), missing=None)
    download_url = fields.Str(validate=validate.Length(min=1, max=1024), missing=None)
