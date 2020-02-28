from datetime import datetime

from app.publishers.models import Publisher
from lib.factory import db

from .constants import STATUS_CREATED


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), index=True)
    comment = db.Column(db.String(1024), index=True)
    src = db.Column(db.String(256))
    status = db.Column(db.String(50), index=True, nullable=False, default=STATUS_CREATED)

    created_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id', ondelete='CASCADE'), nullable=False, index=True)
    publisher = db.relationship(Publisher, foreign_keys=[publisher_id], uselist=False, lazy='joined')

    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
