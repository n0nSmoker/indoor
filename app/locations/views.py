from flask import Blueprint
from sqlalchemy import or_

from lib.factory import db
from lib.utils import success, fail
from lib.webargs import parser

from app.common.decorators import admin_required, auth_required

from .models import Location, City, CityException
from .schemas import (
    FilterCitiesSchema,
    FilterLocationsSchema,
    UpdateLocationSchema,
    UpdateCitySchema,
    LocationSchema,
    CitySchema,
    LocationListSchema,
    CityListSchema,
    AddCitySchema,
    AddLocationSchema,
)
from .utils import save_city, save_location


mod = Blueprint('locations', __name__, url_prefix='/locations')


@mod.route('/')
@auth_required
@parser.use_kwargs(FilterLocationsSchema())
def locations_list_view(page, limit, sort_by, query):
    """Get list of locations.
    ---
    get:
      tags:
        - Locations
      security:
        - cookieAuth: []
      parameters:
      - in: query
        schema: FilterLocationsSchema
      responses:
        200:
          content:
            application/json:
              schema: LocationListSchema
        403:
          description: Forbidden
        400:
          content:
            application/json:
              schema: FailSchema
        5XX:
          description: Unexpected error
    """
    q = Location.query

    if query:
        q = q.filter(
            or_(
                Location.address.ilike(f'%{query}%'),
                Location.city.has(City.name.ilike(f'%{query}%')),
            )
        )

    total = q.count()
    q = q.order_by(sort_by).offset((page - 1) * limit).limit(limit)
    return success(LocationListSchema().dump(dict(
        results=q,
        total=total
    )))


@mod.route('/<int:city_id>/')
@auth_required
def locations_by_city_id_view(city_id):
    """Get list of locations by city_id
    ---
    get:
      tags:
        - Locations
      security:
        - cookieAuth: []
      responses:
        200:
          content:
            application/json:
              schema: LocationListSchema
        403:
          description: Forbidden
        400:
          content:
            application/json:
              schema: FailSchema
        5XX:
          description: Unexpected error
    """
    q = Location.query
    q = q.filter(Location.city.has(City.id == city_id))

    return success(LocationListSchema().dump(dict(
        results=q
    )))


@mod.route('/', methods=['POST'])
@admin_required
@parser.use_kwargs(AddLocationSchema())
def add_location_view(**kwargs):
    """Add new location.
    ---
    post:
      tags:
        - Locations
      security:
        - cookieAuth: []
      requestBody:
        content:
          application/x-www-form-urlencoded:
            schema: AddLocationSchema
      responses:
        200:
          content:
            application/json:
              schema: LocationSchema
        400:
          content:
            application/json:
              schema: FailSchema
        5XX:
          description: Unexpected error
    """
    location = save_location(**kwargs)
    return success(LocationSchema().dump(location))


@mod.route('/<int:location_id>/', methods=['PUT'])
@admin_required
@parser.use_kwargs(UpdateLocationSchema())
def update_location_view(location_id, **kwargs):
    """Update location.
    ---
    put:
      tags:
        - Locations
      security:
        - cookieAuth: []
      requestBody:
        content:
          application/x-www-form-urlencoded:
            schema: UpdateLocationSchema
      responses:
        200:
          content:
            application/json:
              schema: LocationSchema
        400:
          content:
            application/json:
              schema: FailSchema
        403:
          description: Forbidden
        404:
          description: No such item
        5XX:
          description: Unexpected error
    """
    location = save_location(
        instance=Location.query.get_or_404(location_id),
        **kwargs)
    return success(LocationSchema().dump(location))


@mod.route('/<int:location_id>/', methods=['DELETE'])
@admin_required
def delete_location_view(location_id):
    """Delete location.
    ---
    delete:
      tags:
        - Locations
      security:
        - cookieAuth: []
      responses:
        200:
          content:
            application/json:
              schema: LocationSchema
        403:
          description: Forbidden
        404:
          description: No such item
        5XX:
          description: Unexpected error
    """
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    return success(LocationSchema().dump(location))


@mod.route('/cities/')
@auth_required
@parser.use_kwargs(FilterCitiesSchema())
def cities_list_view(page, limit, sort_by, query):
    """Get list of cities.
    ---
    get:
      tags:
        - Cities
      security:
        - cookieAuth: []
      parameters:
      - in: query
        schema: FilterCitiesSchema
      responses:
        200:
          content:
            application/json:
              schema: CityListSchema
        403:
          description: Forbidden
        400:
          content:
            application/json:
              schema: FailSchema
        5XX:
          description: Unexpected error
    """
    q = City.query

    if query:
        q = q.filter(
            City.name.ilike(f'%{query}%')
        )

    total = q.count()
    q = q.order_by(sort_by).offset((page - 1) * limit).limit(limit)
    return success(CityListSchema().dump(dict(
        results=q,
        total=total
    )))


@mod.route('/cities/', methods=['POST'])
@admin_required
@parser.use_kwargs(AddCitySchema())
def add_city_view(**kwargs):
    """Add new city.
    ---
    post:
      tags:
        - Cities
      security:
        - cookieAuth: []
      requestBody:
        content:
          application/x-www-form-urlencoded:
            schema: AddCitySchema
      responses:
        200:
          content:
            application/json:
              schema: CitySchema
        400:
          content:
            application/json:
              schema: FailSchema
        5XX:
          description: Unexpected error
    """
    try:
        city = save_city(**kwargs)
    except CityException as e:
        return fail(str(e))
    return success(CitySchema().dump(city))


@mod.route('/cities/<int:city_id>/', methods=['PUT'])
@admin_required
@parser.use_kwargs(UpdateCitySchema())
def update_city_view(city_id, **kwargs):
    """Update city.
    ---
    put:
      tags:
        - Cities
      security:
        - cookieAuth: []
      requestBody:
        content:
          application/x-www-form-urlencoded:
            schema: UpdateCitySchema
      responses:
        200:
          content:
            application/json:
              schema: CitySchema
        400:
          content:
            application/json:
              schema: FailSchema
        403:
          description: Forbidden
        404:
          description: No such item
        5XX:
          description: Unexpected error
    """
    try:
        city = save_city(
            instance=City.query.get_or_404(city_id),
            **kwargs)
    except CityException as e:
        return fail(str(e))
    return success(CitySchema().dump(city))


@mod.route('/cities/<int:city_id>/', methods=['DELETE'])
@admin_required
def delete_city_view(city_id):
    """Delete city.
    ---
    delete:
      tags:
        - Cities
      security:
        - cookieAuth: []
      responses:
        200:
          content:
            application/json:
              schema: CitySchema
        403:
          description: Forbidden
        404:
          description: No such item
        5XX:
          description: Unexpected error
    """
    city = City.query.get_or_404(city_id)
    db.session.delete(city)
    db.session.commit()
    return success(CitySchema().dump(city))
