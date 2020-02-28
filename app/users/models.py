from datetime import datetime

from app.publishers.models import Publisher
from lib.factory import db

from .constants import ROLE_ADMIN, STATUS_ACTIVE


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), index=True, nullable=False)
    password = db.Column(db.String(1024), index=True, nullable=False)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)

    role = db.Column(db.String(50), index=True, nullable=False)
    status = db.Column(db.String(50), index=True, nullable=False, default=STATUS_ACTIVE)

    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id', ondelete='CASCADE'), index=True)
    publisher = db.relationship(Publisher, foreign_keys=[publisher_id], uselist=False, lazy='joined')

    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN


class UserException(Exception):
    pass
