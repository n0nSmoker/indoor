import os
from werkzeug.datastructures import FileStorage

import pytest

from app.common.utils import save_file
from lib.utils import fail
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


@pytest.mark.parametrize("ext", ['.', '|Ё|', 'exe', 'bat'])
def test_conflict_ext_failure(add_user, ext):
    """
    Check error with "ext" parameter conflict
    """
    file = open('tests/data/FaceImage.jpg', 'rb')
    ext_correct = file.name.split('.')[-1]

    file = FileStorage(file)
    folder = 'tests'

    result = save_file(
        folder=folder,
        ext=ext,
        file=file,
    )

    if ext_correct != result.split('.')[-1]:
        os.remove(result)
        return fail('The extension of the source file '
                    'is different from the one passed '
                    'to the "save_file" function', 501)


@pytest.mark.parametrize("prefix", [get_random_str(), 'User_'])
def test_conflict_prefix_failure(add_user, prefix):
    """
    Check error with "prefix" parameter conflict
    """
    file = open('tests/data/FaceImage.jpg', 'rb')
    ext = file.name.split('.')[-1]

    file = FileStorage(file)
    folder = 'tests'
    prefix_incorrect = get_random_str()

    result = save_file(
        folder=folder,
        ext=ext,
        file=file,
        prefix=prefix_incorrect,
    )
    if prefix_incorrect in result:
        if prefix != prefix_incorrect:
            os.remove(result)
            return fail('The "save_file" function worked incorrectly.'
                        'The final prefix is different from the specified one', 501)
