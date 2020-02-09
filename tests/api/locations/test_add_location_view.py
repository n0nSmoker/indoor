import pytest

from lib.utils import get_random_str

from app.users.constants import ROLE_ADMIN, ROLE_USER
from app.locations.models import Location
from tests.helpers import add_city


endpoint = 'locations.add_location_view'


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
    city = add_city()

    resp = client.post(
        endpoint=endpoint,
        data=dict(
            address=address,
            city_id=city.id
        )
    )
    assert 'id' in resp
    location = Location.query.get(resp['id'])
    assert location

    assert 'address' in resp
    assert resp['address'] == location.address == address
    assert 'city' in resp
    assert 'id' in resp['city']
    assert resp['city']['id'] == city.id


@pytest.mark.parametrize("address", [
    None,
    '',
    get_random_str(1),
    get_random_str(256),
])
def test_malformed_params_failure(client, add_user, address):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)
    city = add_city()

    resp = client.post(
        endpoint=endpoint,
        data=dict(
            address=address,
            city_id=city.id
        ),
        check_status=400
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
