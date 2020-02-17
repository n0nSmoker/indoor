import logging
import os
import uuid
from flask import current_app as app


logger = logging.getLogger('indoor')


def save_file(folder, file, ext, prefix=None):
    """
    Saves file with secure name into given folder
    :param folder: str
    :param file: FileStorage | Image
    :param ext: file extension
    :param prefix: prefix for filename
    :return: path to file
    """
    filename = f'{prefix if prefix else ""}{uuid.uuid4()}.{ext}'
    folder = os.path.join(app.config['UPLOAD_DIR'], folder)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    path = os.path.join(folder, filename)
    file.save(path)
    logger.info('Saved file:%s to folder:%s', filename, path)
    return path


def delete_file(path):
    os.remove(path)
