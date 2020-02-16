import os

import pytest

from lib.utils import get_random_str

from app.users.constants import ROLE_ADMIN, ROLE_USER
from app.content.models import File


endpoint = 'content.add_file_view'


@pytest.mark.parametrize("comment", [
    '12345',
    '     ',
    '\n\n\n\n\n',
    '!@#$%^&*',
    get_random_str(1024),
    '',
])
def test_default(client, add_user, comment):
    """
    Checks that regular user can add files
    """
    _ = add_user(role=ROLE_USER, log_him_in=True)

    resp = client.post(
        endpoint=endpoint,
        content_type='multipart/form-data',
        data=dict(
            file=open('tests/data/FaceImage.jpg', 'rb'),
            comment=comment,
        )
    )
    assert 'id' in resp
    f = File.query.get(resp['id'])
    assert f and os.path.isfile(f.src)

    assert 'comment' in resp
    assert resp['comment'] == f.comment == comment


def test_not_auth_failure(client):
    """
    Checks that anonymous user can not add files
    """
    resp = client.post(
        endpoint=endpoint,
        content_type='multipart/form-data',
        data=dict(
            comment=get_random_str(),
        ),
        check_status=403
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1


@pytest.mark.parametrize("file,comment", [
    (open('tests/data/FaceImage.jpg', 'rb'), get_random_str(1025)),
    (None, get_random_str(100)),
])
def test_malformed_params_failure(client, add_user, file, comment):
    """
    Checks that user can not add files with malformed properties
    """
    _ = add_user(log_him_in=True)

    resp = client.post(
        endpoint=endpoint,
        content_type='multipart/form-data',
        data=dict(
            comment=comment,
            file=file
        ),
        check_status=400
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
