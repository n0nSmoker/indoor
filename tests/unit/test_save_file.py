import os
from werkzeug.datastructures import FileStorage

import pytest

from app.common.utils import save_file
from lib.utils import get_random_str


@pytest.mark.parametrize("prefix", ['', None, 'Img_', ])
def test_save_file(add_user, prefix):
    file = open('tests/data/FaceImage.jpg', 'rb')
    ext = file.name.split('.')[-1]

    file = FileStorage(file)
    folder = 'tests'

    result = save_file(
        folder=folder,
        ext=ext,
        file=file,
        prefix=prefix
    )
    assert os.path.exists(result)
    assert result.split('.')[-1] == ext
    assert open(result, 'rb').read() == open('tests/data/FaceImage.jpg', 'rb').read()


@pytest.mark.parametrize("ext", ['txt', 'ext'])
def test_ext_failure(add_user, ext):
    file = open('tests/data/FaceImage.jpg', 'rb')

    file = FileStorage(file)
    folder = 'tests'

    result = save_file(
        folder=folder,
        ext=ext,
        file=file,
    )
    assert result.split('.')[-1] == ext


@pytest.mark.parametrize("prefix", [get_random_str()])
def test_prefix_failure(add_user, prefix):
    file = open('tests/data/FaceImage.jpg', 'rb')
    ext = file.name.split('.')[-1]

    file = FileStorage(file)
    folder = 'tests'

    result = save_file(
        folder=folder,
        ext=ext,
        file=file,
        prefix=prefix,
    )
    assert prefix in result
