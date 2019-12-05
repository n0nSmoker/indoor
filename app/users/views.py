from datetime import datetime

from flask import Blueprint, current_app as app, request
from sqlalchemy.exc import IntegrityError

from lib.factory import db
from lib.utils import setattrs, success, fail
from lib.webargs import parser

from app.common.decorators import admin_required, auth_required

from .models import User, UserException
from .utils import create_user, login_user, logout_user
from .schemas import (FilterUsersSchema, UpdateUserSchema, UserListSchema,
                      UserSchema, AddUserSchema, LoginUserSchema)


mod = Blueprint('users', __name__, url_prefix='/users')


@mod.route('/')
@admin_required
@parser.use_kwargs(FilterUsersSchema())
def users_list_view(page, limit, sort_by):
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
        403:
          description: Forbidden
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
    return success(UserListSchema().dump(dict(
        results=q,
        total=total
    )))


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
        403:
          description: Forbidden
        404:
          description: No such item
        5XX:
          description: Unexpected error
    """
    user = User.query.get_or_404(user_id)
    return success(UserSchema().dump(user))


@mod.route('/', methods=['POST'])
@admin_required
@parser.use_kwargs(AddUserSchema())
def add_user_view(**kwargs):
    """Add user.
    ---
    post:
      tags:
        - Users
      security:
        - cookieAuth: []
      requestBody:
        content:
          application/x-www-form-urlencoded:
            schema: AddUserSchema
      responses:
        200:
          content:
            application/json:
              schema: UserSchema
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
        user = create_user(**kwargs)
    except UserException as e:
        return fail(str(e))

    return success(UserSchema().dump(user))


@mod.route('/<int:user_id>/', methods=['PUT'])
@admin_required
@parser.use_kwargs(UpdateUserSchema())
def update_user_view(user_id, **kwargs):
    """Update user.
    ---
    put:
      tags:
        - Users
      security:
        - cookieAuth: []
      requestBody:
        content:
          application/x-www-form-urlencoded:
            schema: UpdateUserSchema
      responses:
        200:
          content:
            application/json:
              schema: UserSchema
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
    user = User.query.get_or_404(user_id)
    setattrs(user, **kwargs, updated_at=datetime.utcnow(), ignore_nulls=True)

    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return fail('Email is already in use')

    return success(UserSchema().dump(user))


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
        403:
          description: Forbidden
        404:
          description: No such item
        5XX:
          description: Unexpected error
    """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return success(UserSchema().dump(user))


@mod.route('/login', methods=['POST'])
@parser.use_kwargs(LoginUserSchema())
def login_user_view(email, password):
    """Login user.
    ---
    post:
      tags:
        - Auth
      requestBody:
        content:
          application/x-www-form-urlencoded:
            schema: LoginUserSchema
      responses:
        200:
          content:
            application/json:
              schema: UserSchema
          headers:
            Set-Cookie:
              description:
                Contains the session cookie named from env var `AUTH_COOKIE_NAME`.
                Pass this cookie back in subsequent requests.
              schema:
                type: string
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
        data=UserSchema().dump(user),
        cookies={app.config.get('AUTH_COOKIE_NAME'): sid}
    )


@mod.route('/logout', methods=['POST'])
@auth_required
def logout_user_view():
    """Logout user.
    ---
    post:
      tags:
        - Auth
      responses:
        200:
          content:
            text/plain:
                schema:
                    type: string
                    example: ok
          headers:
            Set-Cookie:
              description:
                Contains the session cookie named from env var `AUTH_COOKIE_NAME`
                with empty value
              schema:
                type: string
        403:
          description: Forbidden
        5XX:
          description: Unexpected error
    """
    sid = request.cookies.get(app.config['AUTH_COOKIE_NAME'])
    logout_user(sid)
    return success('ok')
