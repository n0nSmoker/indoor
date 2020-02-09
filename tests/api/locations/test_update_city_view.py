import pytest

from lib.utils import get_random_str

from app.users.constants import ROLE_ADMIN, ROLE_USER
from app.locations.models import City
from tests.helpers import add_city

endpoint = 'locations.update_city_view'


@pytest.mark.parametrize("name", [
    '12345',
    '     ',
    '\n\n\n\n\n',
    '!@#$%^&*',
    get_random_str(255),
    get_random_str(2),
])
def test_default(client, add_user, name):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)
    city = add_city()

    resp = client.put(
        endpoint=endpoint,
        city_id=city.id,
        data=dict(
            name=name,
        )
    )
    assert 'id' in resp
    city = City.query.get(resp['id'])
    assert city

    assert 'name' in resp
    assert resp['name'] == city.name == name


@pytest.mark.parametrize("name", [
    None,
    '',
    get_random_str(1),
    get_random_str(256),
])
def test_malformed_params_failure(client, add_user, name):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)
    city = add_city()

    resp = client.put(
        endpoint=endpoint,
        city_id=city.id,
        data=dict(
            name=name,
        ),
        check_status=400
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
