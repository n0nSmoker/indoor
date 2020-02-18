import pytest

from lib.utils import get_random_str

from tests.helpers import add_content

from app.users.constants import ROLE_ADMIN, ROLE_USER

endpoint = 'content.files_list_view'


def test_default(client, add_user):
    user = add_user(role=ROLE_USER, log_him_in=True)
    content = add_content(created_by=user.id)
    resp = client.get(
        endpoint=endpoint
    )
    assert 'total' in resp
    assert resp['total'] == 1

    assert 'results' in resp
    assert len(resp['results']) == 1
    assert 'id' in resp['results'][0]
    assert content.id == resp['results'][0]['id']


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
        page=-1,
        param=value
    )
