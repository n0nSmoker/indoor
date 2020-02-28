from datetime import datetime

from app.common.utils import save_file
from app.content.models import File
from lib.auth.manager import current_user
from lib.factory import db
from lib.utils import setattrs

from .constants import STATUS_CREATED


def save_content(instance=None, file=None, **kwargs):
    """
    Saves new or updates existing file
    :param instance: instance of File to update
    :param file: file or FileStorage instance
    :param kwargs:
    :return:
    """
    if file:
        kwargs['name'] = file.filename.split('.')[0]
        kwargs['src'] = save_file(
            folder='content',
            file=file,
            ext=file.filename.split('.')[-1])

    if instance:
        status = kwargs.pop('status', None)
        if file:
            status = STATUS_CREATED
        setattrs(
            instance,
            **kwargs,
            status=status,
            updated_at=datetime.utcnow(),
            ignore_nulls=True,
        )
    else:
        publisher_id = kwargs.pop('publisher_id', None)
        if not publisher_id:
            publisher_id = current_user.publisher_id
        instance = File(**kwargs, publisher_id=publisher_id)

    db.session.add(instance)
    db.session.commit()
    return instance
