import uuid
from datetime import datetime

from flask import current_app as app
from sqlalchemy.exc import IntegrityError

from lib.factory import db
from lib.utils import hash_password, setattrs

from .constants import ROLE_USER
from .models import User, UserException


def get_user_by_id(user_id):
    return User.query.get(int(user_id))


def save_user(instance=None, **kwargs):
    if instance:
        setattrs(instance, **kwargs, updated_at=datetime.utcnow(), ignore_nulls=True)
    else:
        assert 'email' in kwargs, 'Email is required'
        assert 'name' in kwargs, 'Name is required'
        assert 'password' in kwargs, 'Password is required'

        instance = User(
            password=hash_password(
                salt=app.config['SECRET_KEY'],
                password=kwargs.pop('password')
            ),
            role=kwargs.pop('role', ROLE_USER),
            **kwargs
        )
    db.session.add(instance)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise UserException('Email is already in use')
    return instance


def login_user(email, password):
    password = hash_password(
        salt=app.config['SECRET_KEY'],
        password=password
    )
    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        raise UserException('Password or email is incorrect')
    sid = str(uuid.uuid1())
    app.cache.set_user_id(
        user_id=user.id,
        token=sid
    )
    return user, sid


def logout_user(sid):
    app.cache.invalidate_auth_token(token=sid)
