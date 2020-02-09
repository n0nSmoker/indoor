from webargs import fields
from webargs.fields import ma
from marshmallow_sqlalchemy import ModelSchema
from marshmallow.validate import Length, Range, OneOf

from app.common.schemas import FilterSchema, SuccessListSchema
from .models import Location, City


# Cities
class FilterCitiesSchema(FilterSchema):
    sort_by = fields.Str(
        validate=OneOf(
            ['id', 'name']),
        missing='name'
    )
    query = fields.Str(validate=Length(min=2, max=100), missing=None)


class CitySchema(ModelSchema):
    class Meta:
        model = City


class CityListSchema(SuccessListSchema):
    results = fields.List(fields.Nested(CitySchema()))


class AddCitySchema(ma.Schema):
    name = fields.Str(validate=Length(min=2, max=255), required=True)


class UpdateCitySchema(AddCitySchema):
    pass


# Locations
class FilterLocationsSchema(FilterSchema):
    sort_by = fields.Str(
        validate=OneOf(
            ['id', 'address', 'city']),
        missing='address'
    )
    query = fields.Str(validate=Length(min=2, max=100), missing=None)


class LocationSchema(ModelSchema):
    city = fields.Nested(CitySchema, many=False)

    class Meta:
        model = Location


class LocationListSchema(SuccessListSchema):
    results = fields.List(fields.Nested(LocationSchema()))


class AddLocationSchema(ma.Schema):
    address = fields.Str(validate=Length(min=2, max=255), required=True)
    city_id = fields.Int(validate=Range(min=1), required=True)


class UpdateLocationSchema(AddLocationSchema):
    pass
