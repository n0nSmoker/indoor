from datetime import datetime

from lib.factory import db


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), index=True)
    comment = db.Column(db.String(1024), index=True)
    src = db.Column(db.String(256))

    created_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))

    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
