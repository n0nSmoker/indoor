from app.users.constants import ROLE_USER
from tests.helpers import add_device

endpoint = 'devices.device_by_id_view'


def test_default(client, add_user):
    _ = add_user(role=ROLE_USER, log_him_in=True)

    device = add_device()
    resp = client.get(
        endpoint=endpoint,
        device_id=device.id,
    )
    assert 'id' in resp
    assert resp['id'] == device.id
    assert 'access_token' not in resp
    assert 'uid_token' not in resp


def test_not_auth_failure(client):
    device = add_device()
    _ = client.get(
        endpoint=endpoint,
        device_id=device.id,
        check_status=403
    )


def test_wrong_id_failure(client, add_user):
    _ = add_user(role=ROLE_USER, log_him_in=True)

    device = add_device()
    _ = client.get(
        endpoint=endpoint,
        device_id=device.id + 100,
        check_status=404
    )
