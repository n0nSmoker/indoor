from datetime import datetime

from flask import Blueprint, current_app as app
from sqlalchemy.exc import IntegrityError

from lib.factory import db
from lib.utils import setattrs, success, fail
from lib.webargs import parser

from app.common.decorators import admin_required

from .models import User, UserException
from .utils import create_user, login_user
from . import schemas


mod = Blueprint('users', __name__, url_prefix='/users')


@mod.route('/')
@admin_required
@parser.use_kwargs(schemas.FilterUsersSchema())
def list_view(page, limit, sort_by):
    """Get list of users.
    ---
    get:
      tags:
        - Users
      security:
        - cookieAuth: []
      parameters:
      - in: query
        schema: FilterUsersSchema
      responses:
        200:
          content:
            application/json:
              schema: UserListSchema
        401:
          description: Not authorised
        400:
          content:
            application/json:
              schema: FailSchema
        5XX:
          description: Unexpected error
    """
    q = User.query
    total = q.count()

    q = q.order_by(sort_by).offset((page - 1) * limit).limit(limit)
    return success(dict(
        results=[user.to_dict() for user in q],
        total=total
    ))


@mod.route('/<int:user_id>/')
@admin_required
def user_by_id_view(user_id):
    """Get user by id.
    ---
    get:
      tags:
        - Users
      security:
        - cookieAuth: []
      responses:
        200:
          content:
            application/json:
              schema: UserSchema
        401:
          description: Not authorised
        404:
          description: No such item
        5XX:
          description: Unexpected error
    """
    user = User.query.get_or_404(user_id)
    return success(user.to_dict())


@mod.route('/', methods=['POST'])
@admin_required
@parser.use_kwargs(schemas.AddUserSchema())
def add_user_view(**kwargs):
    """Add user.
    ---
    post:
      tags:
        - Users
      security:
        - cookieAuth: []
      content:
        schema: AddUserSchema
      responses:
        200:
          content:
            application/json:
              schema: UserSchema
        401:
          description: Not authorised
        400:
          content:
            application/json:
              schema: FailSchema
        5XX:
          description: Unexpected error
    """
    try:
        user = create_user(**kwargs)
    except UserException as e:
        return fail(str(e))

    return success(user.to_dict())


@mod.route('/<int:user_id>/', methods=['PUT'])
@admin_required
@parser.use_kwargs(schemas.UpdateUserSchema())
def update_user_view(user_id, **kwargs):
    """Update user.
    ---
    put:
      tags:
        - Users
      security:
        - cookieAuth: []
      content:
        schema: UpdateUserSchema
      responses:
        200:
          content:
            application/json:
              schema: UserSchema
        401:
          description: Not authorised
        400:
          content:
            application/json:
              schema: FailSchema
        404:
          description: No such item
        5XX:
          description: Unexpected error
    """
    user = User.query.get_or_404(user_id)
    setattrs(user, **kwargs, updated_at=datetime.utcnow(), ignore_nulls=True)

    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return fail('Email is already in use')

    return success(user.to_dict())


@mod.route('/<int:user_id>/', methods=['DELETE'])
@admin_required
def delete_user_view(user_id):
    """Delete user.
    ---
    delete:
      tags:
        - Users
      security:
        - cookieAuth: []
      responses:
        200:
          content:
            application/json:
              schema: UserSchema
        401:
          description: Not authorised
        404:
          description: No such item
        5XX:
          description: Unexpected error
    """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return success(user.to_dict())


@mod.route('/login', methods=['POST'])
@parser.use_kwargs(schemas.LoginUserSchema())
def login_user_view(email, password):
    """Update user.
    ---
    put:
      tags:
        - Users
      content:
        schema: LoginUserSchema
      responses:
        200:
          content:
            application/json:
              schema: UserSchema
        400:
          content:
            application/json:
              schema: FailSchema
        5XX:
          description: Unexpected error
    """
    try:
        user, sid = login_user(email=email, password=password)
    except UserException as e:
        return fail(str(e))
    return success(
        data=user.to_dict(),
        cookies={app.config.get('AUTH_COOKIE_NAME'): sid}
    )
