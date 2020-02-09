from datetime import datetime
from functools import partial

from sqlalchemy import UniqueConstraint

from lib.factory import db
from lib.utils import get_random_str
from .constants import UNAPPROVED


class Device(db.Model):
    __tablename__ = 'devices'

    id = db.Column(db.Integer, primary_key=True)

    comment = db.Column(db.String(1024), index=True)
    status = db.Column(db.String(50), index=True, default=UNAPPROVED)

    location_id = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete='CASCADE'))
    location = db.relationship('Location', foreign_keys=[location_id], uselist=False, lazy='joined')

    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id', ondelete='SET NULL'))
    contact = db.relationship('Contact', foreign_keys=[contact_id], uselist=False, lazy='joined')

    # Health info multiple ref
    # Status history multiple ref

    access_token = db.Column(
        db.String(255),
        index=True,
        default=partial(get_random_str, 200),
        nullable=False)
    uid_token = db.Column(db.String(255), unique=True, index=True, nullable=False)

    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class Contact(db.Model):
    __tablename__ = 'contacts'
    __table_args__ = (
        UniqueConstraint('name', 'tel'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    tel = db.Column(db.String(255), index=True)
    comment = db.Column(db.String(1024))


class DeviceException(Exception):
    pass


class ContactException(Exception):
    pass
