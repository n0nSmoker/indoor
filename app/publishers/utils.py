from datetime import datetime

from sqlalchemy.exc import IntegrityError

from lib.factory import db
from lib.utils import setattrs

from .models import Publisher, PublisherException


def save_publisher(instance=None, **kwargs):
    if instance:
        setattrs(instance, **kwargs, updated_at=datetime.utcnow(), ignore_nulls=True)
    else:
        instance = Publisher(**kwargs)

    db.session.add(instance)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise PublisherException('This name is already in use')
    return instance
