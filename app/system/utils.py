from sqlalchemy.exc import IntegrityError

from lib.factory import db

from .models import DeviceHealth, DeviceHealthException


def save_device_health(**kwargs):
    instance = DeviceHealth(**kwargs)

    db.session.add(instance)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise DeviceHealthException()
    return instance
