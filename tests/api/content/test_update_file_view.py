import os

import pytest

from lib.utils import get_random_str

from tests.helpers import add_content

from app.users.constants import ROLE_ADMIN, ROLE_MANAGER
from app.content.constants import STATUS_CREATED, STATUS_MODERATION, STATUS_APPROVED, STATUS_REJECTED
from app.content.models import File


endpoint = 'content.update_file_view'


@pytest.mark.parametrize("file,comment", [
    (open('tests/data/FaceImage.jpg', 'rb'), '12345'),
    (open('tests/data/FaceImage.jpg', 'rb'), ''),
    (None, '12345'),
    (None, '     '),
    (None, '\n\n\n\n\n'),
    (None, '!@#$%^&*'),
    (None, get_random_str(1024)),
])
def test_default(client, add_user, file, comment):
    """
    Checks that regular user can update its own files
    """
    user = add_user(role=ROLE_MANAGER, log_him_in=True)
    content = add_content(created_by=user.id, publisher_id=user.publisher_id)
    previous_src = content.src

    resp = client.put(
        endpoint=endpoint,
        content_type='multipart/form-data',
        file_id=content.id,
        data=dict(
            file=file,
            comment=comment,
        )
    )
    assert 'id' in resp
    f = File.query.get(resp['id'])
    assert f
    if file:
        assert os.path.isfile(f.src)
        assert f.src != previous_src

    assert 'comment' in resp
    assert resp['comment'] == f.comment == comment


def test_admin_default(client, add_user):
    """
    Checks that admin can update other user's files
    """
    user = add_user(role=ROLE_MANAGER)
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    file = add_content(created_by=user.id, publisher_id=user.publisher_id)
    previous_src = file.src
    comment = get_random_str()

    resp = client.put(
        endpoint=endpoint,
        content_type='multipart/form-data',
        file_id=file.id,
        data=dict(
            file=open('tests/data/FaceImage.jpg', 'rb'),
            comment=comment,
        )
    )
    assert 'id' in resp
    file = File.query.get(resp['id'])
    assert file and os.path.isfile(file.src)
    assert file.src != previous_src
    assert file.status == STATUS_CREATED

    assert 'comment' in resp
    assert resp['comment'] == file.comment == comment


def test_not_admin_failure(client, add_user):
    """
    Checks that ordinary user can not update other user's files
    """
    user = add_user(role=ROLE_MANAGER)
    _ = add_user(role=ROLE_MANAGER, log_him_in=True)

    file = add_content(created_by=user.id, publisher_id=user.publisher_id)
    comment = get_random_str()

    resp = client.put(
        endpoint=endpoint,
        content_type='multipart/form-data',
        file_id=file.id,
        check_status=403,
        data=dict(
            file=open('tests/data/FaceImage.jpg', 'rb'),
            comment=comment,
        )
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1


def test_not_auth_failure(client, add_user):
    """
    Checks that anonymous user can not update files
    """
    user = add_user(role=ROLE_MANAGER)
    file = add_content(created_by=user.id, publisher_id=user.publisher_id)

    resp = client.put(
        endpoint=endpoint,
        content_type='multipart/form-data',
        file_id=file.id,
        data=dict(
            comment=get_random_str(),
        ),
        check_status=403
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1


@pytest.mark.parametrize("file,comment", [
    (open('tests/data/FaceImage.jpg', 'rb'), get_random_str(1025)),
    (None, ''),
])
def test_malformed_params_failure(client, add_user, file, comment):
    """
    Checks that user can not update files with malformed params
    """
    user = add_user(role=ROLE_MANAGER, log_him_in=True)
    file = add_content(created_by=user.id, publisher_id=user.publisher_id)

    resp = client.put(
        endpoint=endpoint,
        content_type='multipart/form-data',
        file_id=file.id,
        data=dict(
            comment=comment,
            file=file
        ),
        check_status=400
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1


@pytest.mark.parametrize("role,status", [
    (ROLE_MANAGER, STATUS_CREATED),
    (ROLE_MANAGER, STATUS_MODERATION),
    (ROLE_ADMIN, STATUS_CREATED),
    (ROLE_ADMIN, STATUS_MODERATION),
    (ROLE_ADMIN, STATUS_REJECTED),
    (ROLE_ADMIN, STATUS_APPROVED),
])
def test_status_change(client, add_user, role, status):
    """
    Checks that status changed correctly
    """
    if role == ROLE_MANAGER:
        user = add_user(role=role, log_him_in=True)
    else:
        user = add_user(role=ROLE_MANAGER)
        _ = add_user(role=role, log_him_in=True)

    file = add_content(created_by=user.id, publisher_id=user.publisher_id)

    resp = client.put(
        endpoint=endpoint,
        file_id=file.id,
        data=dict(
            status=status,
        )
    )

    assert 'status' in resp
    assert resp['status'] == status


@pytest.mark.parametrize("role,status", [
    (ROLE_MANAGER, STATUS_REJECTED),
    (ROLE_MANAGER, STATUS_APPROVED),
])
def test_malformed_status_change(client, add_user, role, status):
    """
    Checks that user can not change status to not allowed
    """
    user = add_user(role=role, log_him_in=True)
    file = add_content(created_by=user.id, publisher_id=user.publisher_id, status=STATUS_MODERATION)

    resp = client.put(
        endpoint=endpoint,
        file_id=file.id,
        data=dict(
            status=status,
        ),
        check_status=400
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
    assert 'status' in resp['errors'][0]
