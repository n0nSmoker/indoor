from datetime import datetime

from lib.factory import db


class DeviceHealth(db.Model):
    __tablename__ = 'devices_health'

    id = db.Column(db.Integer, primary_key=True)

    device_id = db.Column(db.String(255), index=True, nullable=False)
    software_version = db.Column(db.String(255), index=True, nullable=True)

    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class DeviceHealthException(Exception):
    pass
