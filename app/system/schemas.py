from webargs import fields, validate
from webargs.fields import ma
from marshmallow_sqlalchemy import ModelSchema

from app.common.schemas import FilterSchema, SuccessListSchema
from app.devices.schemas import DeviceSchema
from app.system.models import DeviceHealth
from app.system.constants import OS


class OSVersionSchema(ma.Schema):
    os_name = fields.Str(validate=validate.OneOf([os for os in OS]), required=True)


class SoftwareVersionSchema(ma.Schema):
    software_version = fields.Str(validate=validate.Length(min=1, max=255), required=True)
    os_name = fields.Str(validate=validate.Length(min=1, max=255), required=True)
    download_url = fields.Str(validate=validate.Length(min=1, max=1024), required=True)


class FilterDeviceHealthSchema(FilterSchema):
    sort_by = fields.Str(
        validate=validate.OneOf(
            ['device_id', 'software_version', 'created_at']),
        missing='created_at'
    )
    device_id = fields.Integer(missing=None)
    start_date_time = fields.DateTime(missing=None)
    end_date_time = fields.DateTime(missing=None)


class DeviceHealthSchema(ModelSchema):
    device = fields.Nested(DeviceSchema, many=False)

    class Meta:
        model = DeviceHealth


class DeviceHealthListSchema(SuccessListSchema):
    results = fields.List(fields.Nested(DeviceHealthSchema()))


class AddDeviceHealthSchema(ma.Schema):
    software_version = fields.Str(validate=validate.Length(min=0, max=255), missing=None)
