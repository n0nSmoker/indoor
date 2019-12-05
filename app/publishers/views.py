from flask import Blueprint

from lib.auth.manager import current_user
from lib.factory import db
from lib.utils import success, fail
from lib.webargs import parser

from app.common.decorators import admin_required

from .models import Publisher, PublisherException
from .schemas import (FilterPublishersSchema, UpdatePublisherSchema, PublisherListSchema,
                      PublisherSchema, AddPublisherSchema)
from .utils import save_publisher


mod = Blueprint('publishers', __name__, url_prefix='/publishers')


@mod.route('/')
@admin_required
@parser.use_kwargs(FilterPublishersSchema())
def publishers_list_view(page, limit, sort_by):
    """Get list of publishers.
    ---
    get:
      tags:
        - Publishers
      security:
        - cookieAuth: []
      parameters:
      - in: query
        schema: FilterPublishersSchema
      responses:
        200:
          content:
            application/json:
              schema: PublisherListSchema
        403:
          description: Forbidden
        400:
          content:
            application/json:
              schema: FailSchema
        5XX:
          description: Unexpected error
    """
    q = Publisher.query
    total = q.count()

    q = q.order_by(sort_by).offset((page - 1) * limit).limit(limit)
    return success(PublisherListSchema().dump(dict(
        results=q,
        total=total
    )))


@mod.route('/<int:publisher_id>/')
@admin_required
def publisher_by_id_view(publisher_id):
    """Get publisher by id.
    ---
    get:
      tags:
        - Publishers
      security:
        - cookieAuth: []
      responses:
        200:
          content:
            application/json:
              schema: PublisherSchema
        403:
          description: Forbidden
        404:
          description: No such item
        5XX:
          description: Unexpected error
    """
    user = Publisher.query.get_or_404(publisher_id)
    return success(PublisherSchema().dump(user))


@mod.route('/', methods=['POST'])
@admin_required
@parser.use_kwargs(AddPublisherSchema())
def add_publisher_view(**kwargs):
    """Add publisher.
    ---
    post:
      tags:
        - Publishers
      security:
        - cookieAuth: []
      requestBody:
        content:
          application/x-www-form-urlencoded:
            schema: AddPublisherSchema
      responses:
        200:
          content:
            application/json:
              schema: PublisherSchema
        400:
          content:
            application/json:
              schema: FailSchema
        403:
          description: Forbidden
        5XX:
          description: Unexpected error
    """
    try:
        publisher = save_publisher(
            created_by=current_user.id,
            **kwargs)
    except PublisherException as e:
        return fail(str(e))

    return success(PublisherSchema().dump(publisher))


@mod.route('/<int:publisher_id>/', methods=['PUT'])
@admin_required
@parser.use_kwargs(UpdatePublisherSchema())
def update_publisher_view(publisher_id, **kwargs):
    """Update publisher.
    ---
    put:
      tags:
        - Publishers
      security:
        - cookieAuth: []
      requestBody:
        content:
          application/x-www-form-urlencoded:
            schema: UpdatePublisherSchema
      responses:
        200:
          content:
            application/json:
              schema: PublisherSchema
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
    publisher = Publisher.query.get_or_404(publisher_id)
    try:
        publisher = save_publisher(publisher, **kwargs)
    except PublisherException as e:
        return fail(str(e))

    return success(PublisherSchema().dump(publisher))


@mod.route('/<int:publisher_id>/', methods=['DELETE'])
@admin_required
def delete_publisher_view(publisher_id):
    """Delete publisher.
    ---
    delete:
      tags:
        - Publishers
      security:
        - cookieAuth: []
      responses:
        200:
          content:
            application/json:
              schema: PublisherSchema
        403:
          description: Forbidden
        404:
          description: No such item
        5XX:
          description: Unexpected error
    """
    publisher = Publisher.query.get_or_404(publisher_id)
    db.session.delete(publisher)
    db.session.commit()
    return success(PublisherSchema().dump(publisher))
