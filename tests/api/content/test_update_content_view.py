import os
import pytest

from lib.utils import get_random_str

from app.users.constants import ROLE_USER, ROLE_ADMIN
from app.content.models import File


endpoint = 'content.update_file_view'
test_file_path = 'tests/data/FaceImage.jpg'


@pytest.mark.parametrize("comment,file", [
    # Valid parameters
    ('', open(test_file_path, 'rb')),
    ('123', open(test_file_path, 'rb')),
    ('Text', open(test_file_path, 'rb')),
    ('_', open(test_file_path, 'rb')),
    ('\t', open(test_file_path, 'rb')),
    ('|Ё|', open(test_file_path, 'rb')),
    ('   ', open(test_file_path, 'rb')),

    ('', None),
    ('123', None),
    ('Text', None),
    ('_', None),
    ('\t', None),
    ('|Ё|', None),
    ('   ', None),
])
def test_default(client, add_user, add_content, comment, file):
    user = add_user(role=ROLE_USER, log_him_in=True)
    content = add_content(created_by=user.id)
    resp = client.put(
        endpoint=endpoint,
        file_id=content.id,
        content_type='multipart/form-data',
        data=dict(
            comment=comment,
            file=file,
        )
    )
    assert 'id' in resp
    updated = File.query.filter_by(id=resp['id']).one_or_none()
    assert updated

    assert updated.comment == comment
    assert updated.name and os.path.isfile(updated.src)


def test_not_auth_failure(client, add_user, add_content):
    user = add_user(role=ROLE_USER, log_him_in=False)
    content = add_content(created_by=user.id)
    client.put(
        endpoint=endpoint,
        file_id=content.id,
        content_type='multipart/form-data',
        data=dict(
            comment=get_random_str(),
            file=open(test_file_path, 'rb'),
        ),
        check_status=403
    )


def test_fake_file_id_failure(client, add_user, add_content):
    _ = add_user(role=ROLE_USER, log_him_in=True)
    client.put(
        endpoint=endpoint,
        file_id=131546543213513,
        content_type='multipart/form-data',
        data=dict(
            comment=get_random_str(),
            file=None,
        ),
        check_status=404
    )
