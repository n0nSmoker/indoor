from datetime import datetime

from lib.factory import db
from sqlalchemy_serializer import SerializerMixin


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), index=True, nullable=False)
    password = db.Column(db.String(50), index=True, nullable=False)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)

    role = db.Column(db.String(50), index=True, nullable=False)
    status = db.Column(db.String(50), index=True, nullable=False)

    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
