from datetime import datetime

from flask import Blueprint
from lib.factory import db

from lib.swagger import use_kwargs
from lib.utils import setattrs, success

from .models import User
import app.users.schemas as schemas

mod = Blueprint('users', __name__, url_prefix='/users')


@mod.route('/')
@use_kwargs(schemas.FILTER_USERS_SCHEMA)
def list_view(page, limit, sort_by):
    q = User.query
    total = q.count()

    q = q.order_by(sort_by).offset((page - 1) * limit).limit(limit)
    return success(
        results=[user.to_dict() for user in q],
        total=total
    )


@mod.route('/<int:user_id>/')
def user_by_id_view(user_id):
    user = User.query.filter_by(id=user_id).one()
    return success(**user.to_dict())


@mod.route('/', methods=['POST'])
@use_kwargs(schemas.ADD_USER_SCHEMA)
def add_user_view(user_id=None, **kwargs):
    if user_id:
        user = User.query.filter_by(id=user_id).one()
        setattrs(user, **kwargs, updated_at=datetime.utcnow())
    else:
        user = User(**kwargs)
        db.session.add(user)

    db.session.commit()

    return success(**user.to_dict())


@mod.route('/<int:user_id>/', methods=['PUT'])
@use_kwargs(schemas.UPDATE_USER_SCHEMA)
def update_user_view(user_id, **kwargs):
    return add_user_view(user_id, **kwargs)


@mod.route('/<int:user_id>/', methods=['DELETE'])
def delete_user_view(user_id):
    user = User.query.filter_by(id=user_id).one()
    db.session.delete(user)
    db.session.commit()
    return success(**user.to_dict())
