import os
import pytest

from lib.utils import get_random_str

from app.users.constants import ROLE_USER
from app.content.models import File

endpoint = 'content.add_file_view'
test_file_path = 'tests/data/FaceImage.jpg'


@pytest.mark.parametrize("comment", [
    # Valid parameters
    '123',
    'Text',
    '_',
    '\t',
    '|Ё|',
    '   ',
])
def test_default(client, add_user, comment):
    _ = add_user(role=ROLE_USER, log_him_in=True)
    resp = client.post(
        endpoint=endpoint,
        content_type='multipart/form-data',
        data=dict(
            comment=comment,
            file=open(test_file_path, 'rb'),
        )
    )
    assert 'id' in resp
    content = File.query.filter_by(id=resp['id']).one_or_none()
    assert content

    assert content.comment == comment
    assert content.name and os.path.isfile(content.src)


def test_not_auth_failure(client, add_user, add_content):
    _ = add_user(role=ROLE_USER, log_him_in=False)
    client.post(
        endpoint=endpoint,
        content_type='multipart/form-data',
        data=dict(
            comment=get_random_str(),
            file=open(test_file_path, 'rb'),
        ),
        check_status=403
    )


@pytest.mark.parametrize("comment,file", [
    (get_random_str(), None),
    (get_random_str(), ''),
])
def test_not_file_failure(client, add_user, comment, file):
    _ = add_user(role=ROLE_USER, log_him_in=True)
    resp = client.post(
        endpoint=endpoint,
        content_type='multipart/form-data',
        data=dict(
            comment=comment,
            file=file,
        ),
        check_status=400
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
    assert 'file' in resp['errors'][0].lower()
