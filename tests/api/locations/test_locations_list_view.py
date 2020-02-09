import pytest

from lib.utils import get_random_str

from app.users.constants import ROLE_ADMIN, ROLE_USER
from tests.helpers import add_location

endpoint = 'locations.locations_list_view'


def test_default(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    location = add_location()
    resp = client.get(
        endpoint=endpoint
    )
    assert 'total' in resp
    assert resp['total'] == 1
    assert 'results' in resp
    assert len(resp['results']) == 1
    assert 'id' in resp['results'][0]
    assert resp['results'][0]['id'] == location.id

    location2 = add_location()
    resp = client.get(
        endpoint=endpoint
    )
    assert 'total' in resp
    assert resp['total'] == 2
    assert 'results' in resp
    assert len(resp['results']) == 2
    assert {r['id'] for r in resp['results']} == {location.id, location2.id}


def test_search_mode(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    common_string = 'FGHJ#$%^&12'
    ids = {
        add_location(address=f'prefixXXX{common_string}').id,
        add_location(address=f'prefixXXX{common_string}postfix123').id,
        add_location(address=f'{common_string}postfix123').id,
        add_location(address=common_string).id,

        add_location(city_name=f'prefixXXX{common_string}').id,
        add_location(city_name=f'prefixXXX{common_string}postfix123').id,
        add_location(city_name=f'{common_string}postfix123').id,
        add_location(city_name=common_string).id,
    }
    # Add some noise
    for _ in range(10):
        add_location()

    # Search
    resp = client.get(
        endpoint=endpoint,
        query=common_string
    )
    assert 'total' in resp
    assert resp['total'] == 8

    assert 'results' in resp
    assert len(resp['results']) == 8
    assert {r['id'] for r in resp['results']} == ids


def test_not_auth_failure(client, add_user):
    _ = add_user(role=ROLE_USER, log_him_in=False)
    _ = client.get(
        endpoint=endpoint,
        check_status=403
    )


@pytest.mark.parametrize('param,value', [
    ('page', -1),
    ('page', -10),
    ('page', 101),
    ('page', 0),

    ('limit', 0),
    ('limit', 1001),
    ('limit', -1),
    ('limit', -10),

    ('sort_by', 'wrong_field'),
    ('sort_by', '-wrong_field'),
    ('sort_by', 'created_by'),
    ('sort_by', '-created_by'),
    ('sort_by', '--name'),

    ('query', get_random_str(1)),
    ('query', get_random_str(101)),
])
def test_wrong_params_failure(client, add_user, param, value):
    _ = add_user(role=ROLE_USER, log_him_in=True)
    _ = client.get(
        endpoint=endpoint,
        check_status=400,
        **{param: value}
    )
