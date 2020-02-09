import pytest

from lib.utils import get_random_str

from app.users.constants import ROLE_ADMIN, ROLE_USER
from app.locations.models import Location
from tests.helpers import add_location

endpoint = 'locations.update_location_view'


@pytest.mark.parametrize("address", [
    '15',
    '     ',
    '\n\n\n\n\n',
    '!@#$%^&*',
    get_random_str(255),
    get_random_str(2),
])
def test_default(client, add_user, address):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    location = add_location()

    resp = client.put(
        endpoint=endpoint,
        location_id=location.id,
        data=dict(
            address=address,
            city_id=location.city.id
        )
    )
    assert 'id' in resp
    location = Location.query.get(resp['id'])
    assert location

    assert 'address' in resp
    assert resp['address'] == location.address == address
    assert 'city' in resp
    assert 'id' in resp['city']
    assert resp['city']['id'] == location.city.id
    assert 'name' in resp['city']
    assert resp['city']['name'] == location.city.name


@pytest.mark.parametrize("address", [
    None,
    '',
    get_random_str(1),
    get_random_str(256),
])
def test_malformed_params_failure(client, add_user, address):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    location = add_location()

    resp = client.put(
        endpoint=endpoint,
        location_id=location.id,
        data=dict(
            address=address,
            city_id=location.city.id
        ),
        check_status=400
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
