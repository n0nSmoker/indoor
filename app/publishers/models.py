from datetime import datetime

from lib.factory import db


class Publisher(db.Model):
    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), unique=True, index=True, nullable=False)
    comment = db.Column(db.String(1024), nullable=True)
    airtime = db.Column(db.DECIMAL(precision=4, scale=1), index=True, nullable=True)

    created_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))

    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class PublisherException(Exception):
    pass
