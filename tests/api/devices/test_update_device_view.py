import pytest
from lib.utils import get_random_str

from tests.helpers import add_contact, add_location, add_device

from app.users.constants import ROLE_ADMIN, ROLE_USER
from app.devices.models import Device
from app.devices.constants import STATUSES, ACTIVE, INACTIVE, UNAPPROVED


endpoint = 'devices.update_device_view'


@pytest.mark.parametrize("contact,location,comment,status", [
    (True, None, None, None),
    (None, True, None, None),
    (None, None, get_random_str(), None),
    (None, None, None, INACTIVE),

    (True, True, None, None),
    (True, True, get_random_str(), None),
    (None, None, get_random_str(), ACTIVE),
    (None, True, get_random_str(), ACTIVE),
    (True, True, get_random_str(), ACTIVE),
])
def test_default(client, add_user, contact, location, comment, status):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)
    device = add_device()

    contact_id = add_contact().id if contact else None
    location_id = add_location().id if location else None
    resp = client.put(
        endpoint=endpoint,
        device_id=device.id,
        data=dict(
            status=status,
            comment=comment,
            contact_id=contact_id,
            location_id=location_id,
        )
    )
    assert 'id' in resp
    assert resp['id'] == device.id
    updated_device = Device.query.get(resp['id'])
    assert updated_device

    assert 'comment' in resp
    assert updated_device.comment == comment == resp['comment']

    assert 'status' in resp
    if status:
        assert updated_device.status == status == resp['status']
    else:
        assert updated_device.status == resp['status'] == UNAPPROVED

    assert 'location' in resp
    assert updated_device.location_id == location_id
    if location:
        assert 'id' in resp['location']
        assert resp['location']['id'] == location_id

    assert 'contact' in resp
    assert updated_device.contact_id == contact_id
    if contact:
        assert 'id' in resp['contact']
        assert resp['contact']['id'] == contact_id


def test_not_auth_failure(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=False)

    device = add_device()
    _ = client.put(
        endpoint=endpoint,
        device_id=device.id,
        check_status=403,
        data=dict(
            status=ACTIVE,
            comment=get_random_str(),
        )
    )


def test_not_admin_failure(client, add_user):
    _ = add_user(role=ROLE_USER, log_him_in=True)

    device = add_device()
    _ = client.put(
        endpoint=endpoint,
        device_id=device.id,
        check_status=403,
        data=dict(
            status=ACTIVE,
            comment=get_random_str(),
        )
    )


@pytest.mark.parametrize("contact_id,location_id,comment,status", [
    (0, None, None, None),
    (None, 0, None, None),
    (-1, None, None, None),
    (None, -2, None, None),

    (None, None, get_random_str(256), None),
    (None, None, None, get_random_str()),
])
def test_malformed_params_failure(client, add_user, contact_id, location_id, comment, status):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    device = add_device()
    resp = client.put(
        endpoint=endpoint,
        device_id=device.id,
        check_status=400,
        data=dict(
            status=status,
            comment=comment,
            contact_id=contact_id,
            location_id=location_id,
        )
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
