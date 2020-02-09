from app.devices.models import Device
from app.users.constants import ROLE_USER, ROLE_ADMIN
from tests.helpers import add_device

endpoint = 'devices.delete_device_view'


def test_default(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    device = add_device()
    resp = client.delete(
        endpoint=endpoint,
        device_id=device.id,
    )
    assert 'id' in resp
    assert resp['id'] == device.id
    assert not Device.query.get(resp['id'])


def test_not_admin_failure(client, add_user):
    _ = add_user(role=ROLE_USER, log_him_in=True)

    device = add_device()
    _ = client.delete(
        endpoint=endpoint,
        device_id=device.id,
        check_status=403
    )


def test_wrong_id_failure(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    device = add_device()
    _ = client.delete(
        endpoint=endpoint,
        device_id=129129129129192,
        check_status=404
    )
    assert Device.query.get(device.id)
