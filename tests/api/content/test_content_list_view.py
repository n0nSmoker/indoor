import pytest

from lib.utils import get_random_str

from tests.helpers import add_content

from app.users.constants import ROLE_ADMIN, ROLE_MANAGER

endpoint = 'content.files_list_view'


def test_default(client, add_user):
    user = add_user(role=ROLE_MANAGER, log_him_in=True)
    ids = [add_content(created_by=user.id, publisher_id=user.publisher_id).id for _ in range(3)]

    # add some noise
    user2 = add_user(role=ROLE_MANAGER)
    for _ in range(10):
        add_content(created_by=user2.id, publisher_id=user2.publisher_id)

    resp = client.get(endpoint=endpoint)
    assert 'total' in resp
    assert resp['total'] == len(ids)

    assert 'results' in resp
    assert len(resp['results']) == len(ids)
    for item in resp['results']:
        assert 'id' in item
        assert item['id'] in ids
        assert 'publisher' in item
        assert user.publisher_id == item['publisher']['id']


def test_not_auth_failure(client, add_user):
    _ = add_user(role=ROLE_MANAGER, log_him_in=False)
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
        page=-1,
        param=value
    )
