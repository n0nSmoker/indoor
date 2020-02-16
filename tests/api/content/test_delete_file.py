import os

from app.content.models import File
from app.users.constants import ROLE_USER, ROLE_ADMIN
from tests.helpers import add_content


endpoint = 'content.delete_file_view'


def test_default(client, add_user):
    """
    Checks that ordinary user can delete its own files
    """
    user = add_user(role=ROLE_USER, log_him_in=True)

    file = add_content(created_by=user.id)
    resp = client.delete(
        endpoint=endpoint,
        file_id=file.id,
    )
    assert 'id' in resp
    assert resp['id'] == file.id
    assert not File.query.get(resp['id'])
    assert not os.path.isfile(file.src)


def test_admin_default(client, add_user):
    """
    Checks that admin can delete other user's files
    """
    user = add_user(role=ROLE_USER, log_him_in=False)
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    file = add_content(created_by=user.id)
    resp = client.delete(
        endpoint=endpoint,
        file_id=file.id,
    )
    assert 'id' in resp
    assert resp['id'] == file.id
    assert not File.query.get(resp['id'])
    assert not os.path.isfile(file.src)


def test_not_auth_failure(client, add_user):
    """
    Checks that anonymous user can not delete files
    """
    user = add_user(role=ROLE_USER, log_him_in=False)

    file = add_content(created_by=user.id)
    _ = client.delete(
        endpoint=endpoint,
        file_id=file.id,
        check_status=403
    )


def test_not_admin_failure(client, add_user):
    """
    Checks that ordinary user can not delete other user's files
    """
    user = add_user(role=ROLE_USER, log_him_in=False)
    _ = add_user(role=ROLE_USER, log_him_in=True)

    file = add_content(created_by=user.id)
    _ = client.delete(
        endpoint=endpoint,
        file_id=file.id,
        check_status=403
    )


def test_wrong_id_failure(client, add_user):
    """
    Checks that we get 404 response if the file_id is wrong
    """
    user = add_user(role=ROLE_ADMIN, log_him_in=True)

    file = add_content(created_by=user.id)
    _ = client.delete(
        endpoint=endpoint,
        file_id=129129129129192,
        check_status=404
    )
    assert File.query.get(file.id)
