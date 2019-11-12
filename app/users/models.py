from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

from lib.factory import db

from .constants import STATUS_ACTIVE


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-password',)

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), index=True, nullable=False)
    password = db.Column(db.String(1024), index=True, nullable=False)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)

    role = db.Column(db.String(50), index=True, nullable=False)
    status = db.Column(db.String(50), index=True, nullable=False, default=STATUS_ACTIVE)

    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
