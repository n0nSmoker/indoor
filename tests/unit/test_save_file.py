import os
from werkzeug.datastructures import FileStorage

import pytest

from app.common.utils import save_file


@pytest.mark.parametrize("prefix", ['', None, 'Img_',])
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
