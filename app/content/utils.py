from datetime import datetime

from app.common.utils import save_file
from app.content.models import File
from lib.factory import db
from lib.utils import setattrs


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
        setattrs(instance, **kwargs, updated_at=datetime.utcnow(), ignore_nulls=True)
    else:
        instance = File(**kwargs)

    db.session.add(instance)
    db.session.commit()
    return instance
