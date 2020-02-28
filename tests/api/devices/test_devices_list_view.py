import pytest

from lib.utils import get_random_str

from app.users.constants import ROLE_ADMIN, ROLE_USER
from tests.helpers import add_device, add_location, add_contact

endpoint = 'devices.devices_list_view'
search_fields = ['name', 'comment']


def test_default(client, add_user):
    _ = add_user(role=ROLE_USER, log_him_in=True)

    device = add_device()
    resp = client.get(
        endpoint=endpoint
    )
    assert 'total' in resp
    assert resp['total'] == 1

    assert 'results' in resp
    assert len(resp['results']) == 1
    assert 'id' in resp['results'][0]
    assert device.id == resp['results'][0]['id']

    assert 'access_token' not in resp['results'][0]
    assert 'uid_token' not in resp['results'][0]


def test_search_mode(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    string = 'common string to find'
    strings = [
        f'some prefix {string}',
        f'{string} some postfix',
        f'prefix {string} postfix',
        string,
    ]

    # Create devices
    ids = set()
    for s in strings:
        location = add_location(address=s)
        ids.add(add_device(location_id=location.id).id)

        contact = add_contact(name=s)
        ids.add(add_device(contact_id=contact.id).id)

        contact = add_contact(tel=s)
        ids.add(add_device(contact_id=contact.id).id)

        ids.add(add_device(comment=s).id)

    # Add some noise
    for s in strings:
        # We do not search by city_name
        location = add_location(city_name=get_random_str())
        add_device(location_id=location.id)

        location = add_location(address=get_random_str())
        add_device(location_id=location.id)

        contact = add_contact(name=get_random_str())
        add_device(contact_id=contact.id)

        contact = add_contact(tel=get_random_str())
        add_device(contact_id=contact.id)

        add_device(comment=get_random_str())

    # Check results
    resp = client.get(
        endpoint=endpoint,
        query=string,
        limit=100  # To get all the results on one page
    )
    assert 'total' in resp
    assert resp['total'] == len(ids)
    assert 'results' in resp
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
    ('sort_by', '--status'),

    ('query', get_random_str(1)),
    ('query', get_random_str(2)),
    ('query', get_random_str(101)),
])
def test_wrong_params_failure(client, add_user, param, value):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)
    _ = client.get(
        endpoint=endpoint,
        check_status=400,
        **{param: value}    
    )
