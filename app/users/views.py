import uuid
from datetime import datetime

from flask import Blueprint, current_app as app
from sqlalchemy.exc import IntegrityError

from app.common.decorators import auth_required
from lib.factory import db

from lib.swagger import use_kwargs
from lib.utils import setattrs, success, fail

from .models import User
from . import schemas


mod = Blueprint('users', __name__, url_prefix='/users')


@mod.route('/')
@auth_required
@use_kwargs(schemas.FILTER_USERS_SCHEMA)
def list_view(page, limit, sort_by):
    q = User.query
    total = q.count()

    q = q.order_by(sort_by).offset((page - 1) * limit).limit(limit)
    return success(dict(
        results=[user.to_dict() for user in q],
        total=total
    ))


@mod.route('/<int:user_id>/')
def user_by_id_view(user_id):
    user = User.query.filter_by(id=user_id).one()
    return success(user.to_dict())


@mod.route('/', methods=['POST'])
@use_kwargs(schemas.ADD_USER_SCHEMA)
def add_user_view(**kwargs):
    user = User(**kwargs)
    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return fail(title='Email is already in use')

    return success(user.to_dict())


@mod.route('/<int:user_id>/', methods=['PUT'])
@use_kwargs(schemas.UPDATE_USER_SCHEMA)
def update_user_view(user_id, **kwargs):
    user = User.query.filter_by(id=user_id).one()
    setattrs(user, **kwargs, updated_at=datetime.utcnow(), ignore_nulls=True)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return fail(title='Email is already in use')

    return success(user.to_dict())


@mod.route('/<int:user_id>/', methods=['DELETE'])
def delete_user_view(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return success(user.to_dict())


@mod.route('/login', methods=['POST'])
@use_kwargs(schemas.LOGIN_USER_SCHEMA)
def login_user_view(email, password):
    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        return fail(title='Password or email is incorrect')
    sid = str(uuid.uuid1())
    app.cache.set_user_id(
        user_id=user.id,
        token=sid
    )
    return success(
        data=user.to_dict(),
        cookies={app.config.get('AUTH_COOKIE_NAME'): sid}
    )
