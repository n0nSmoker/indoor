from flask import Blueprint
from sqlalchemy import or_

from app.common.decorators import auth_required
from app.common.utils import delete_file
from lib.auth.manager import current_user
from lib.factory import db
from lib.utils import success, fail
from lib.webargs import parser

from .models import File
from .schemas import (
    FilterFilesSchema,
    FileListSchema,
    AddFileSchema,
    UpdateFileSchema,
    FileSchema,
)
from .utils import save_content


mod = Blueprint('content', __name__, url_prefix='/content')


@mod.route('/')
@auth_required
@parser.use_kwargs(FilterFilesSchema())
def files_list_view(page, limit, sort_by, query):
    """Get list of files.
    ---
    get:
      tags:
        - Content
      security:
        - cookieAuth: []
      parameters:
      - in: query
        schema: FilterFilesSchema
      responses:
        200:
          content:
            application/json:
              schema: FileListSchema
        403:
          description: Forbidden
        400:
          content:
            application/json:
              schema: FailSchema
        5XX:
          description: Unexpected error
    """
    q = File.query

    if not current_user.is_admin:
        q = q.filter_by(publisher_id=current_user.publisher_id)

    if query:
        q = q.filter(
            or_(
                File.name.ilike(f'%{query}%'),
                File.comment.ilike(f'%{query}%'),
            )
        )

    total = q.count()
    q = q.order_by(sort_by).offset((page - 1) * limit).limit(limit)
    return success(FileListSchema().dump(dict(
        results=q,
        total=total
    )))


@mod.route('/', methods=['POST'])
@auth_required
@parser.use_kwargs(AddFileSchema())
def add_file_view(**kwargs):
    """Add new file.
    ---
    post:
      tags:
        - Content
      security:
        - cookieAuth: []
      requestBody:
        content:
          multipart/form-data:
            schema: AddFileSchema
      responses:
        200:
          content:
            application/json:
              schema: FileSchema
        400:
          content:
            application/json:
              schema: FailSchema
        5XX:
          description: Unexpected error
    """
    content = save_content(created_by=current_user.id, **kwargs)
    return success(FileSchema().dump(content))


@mod.route('/<int:file_id>/', methods=['DELETE'])
@auth_required
def delete_file_view(file_id):
    """Delete file.
    ---
    delete:
      tags:
        - Content
      security:
        - cookieAuth: []
      responses:
        200:
          content:
            application/json:
              schema: FileSchema
        403:
          description: Forbidden
        404:
          description: No such item
        5XX:
          description: Unexpected error
    """
    file = File.query.get_or_404(file_id)
    if file.created_by != current_user.id and not current_user.is_admin:
        return fail('You can not delete this item', 403)
    response = FileSchema().dump(file)
    db.session.delete(file)
    db.session.commit()
    delete_file(file.src)
    return success(response)


@mod.route('/<int:file_id>/', methods=['PUT'])
@auth_required
@parser.use_kwargs(UpdateFileSchema())
def update_file_view(file_id, **kwargs):
    """Update file.
    ---
    put:
      tags:
        - Content
      security:
        - cookieAuth: []
      requestBody:
        content:
          multipart/form-data:
            schema: UpdateFileSchema
      responses:
        200:
          content:
            application/json:
              schema: FileSchema
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
    file = File.query.get_or_404(file_id)
    if file.created_by != current_user.id and not current_user.is_admin:
        return fail('You can not edit this item', 403)
    file = save_content(instance=file, **kwargs)
    return success(FileSchema().dump(file))

#
# @mod.route('/<int:location_id>/', methods=['DELETE'])
# @admin_required
# def delete_location_view(location_id):
#     """Delete location.
#     ---
#     delete:
#       tags:
#         - Locations
#       security:
#         - cookieAuth: []
#       responses:
#         200:
#           content:
#             application/json:
#               schema: LocationSchema
#         403:
#           description: Forbidden
#         404:
#           description: No such item
#         5XX:
#           description: Unexpected error
#     """
#     location = Location.query.get_or_404(location_id)
#     db.session.delete(location)
#     db.session.commit()
#     return success(LocationSchema().dump(location))
#
#
# @mod.route('/cities/')
# @auth_required
# @parser.use_kwargs(FilterCitiesSchema())
# def cities_list_view(page, limit, sort_by, query):
#     """Get list of cities.
#     ---
#     get:
#       tags:
#         - Cities
#       security:
#         - cookieAuth: []
#       parameters:
#       - in: query
#         schema: FilterCitiesSchema
#       responses:
#         200:
#           content:
#             application/json:
#               schema: CityListSchema
#         403:
#           description: Forbidden
#         400:
#           content:
#             application/json:
#               schema: FailSchema
#         5XX:
#           description: Unexpected error
#     """
#     q = City.query
#
#     if query:
#         q = q.filter(
#             City.name.ilike(f'%{query}%')
#         )
#
#     total = q.count()
#     q = q.order_by(sort_by).offset((page - 1) * limit).limit(limit)
#     return success(CityListSchema().dump(dict(
#         results=q,
#         total=total
#     )))
#
#
# @mod.route('/cities/', methods=['POST'])
# @admin_required
# @parser.use_kwargs(AddCitySchema())
# def add_city_view(**kwargs):
#     """Add new city.
#     ---
#     post:
#       tags:
#         - Cities
#       security:
#         - cookieAuth: []
#       requestBody:
#         content:
#           schema: AddCitySchema
#       responses:
#         200:
#           content:
#             application/json:
#               schema: CitySchema
#         400:
#           content:
#             application/json:
#               schema: FailSchema
#         5XX:
#           description: Unexpected error
#     """
#     try:
#         city = save_city(**kwargs)
#     except CityException as e:
#         return fail(str(e))
#     return success(CitySchema().dump(city))
#
#
# @mod.route('/cities/<int:city_id>/', methods=['PUT'])
# @admin_required
# @parser.use_kwargs(UpdateCitySchema())
# def update_city_view(city_id, **kwargs):
#     """Update city.
#     ---
#     put:
#       tags:
#         - Cities
#       security:
#         - cookieAuth: []
#       requestBody:
#         content:
#           schema: UpdateCitySchema
#       responses:
#         200:
#           content:
#             application/json:
#               schema: CitySchema
#         400:
#           content:
#             application/json:
#               schema: FailSchema
#         403:
#           description: Forbidden
#         404:
#           description: No such item
#         5XX:
#           description: Unexpected error
#     """
#     try:
#         city = save_city(
#             instance=City.query.get_or_404(city_id),
#             **kwargs)
#     except CityException as e:
#         return fail(str(e))
#     return success(CitySchema().dump(city))
#
#
