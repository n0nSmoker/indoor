import pytest

from app.users.constants import ROLE_ADMIN, ROLE_USER


endpoint = 'users.users_list_view'


def test_default(client, add_user):
    u1 = add_user(role=ROLE_ADMIN, log_him_in=True)
    u2 = add_user(role=ROLE_USER, log_him_in=False)
    resp = client.get(
        endpoint=endpoint
    )
    assert 'total' in resp
    assert resp['total'] == 2
    assert 'results' in resp
    assert len(resp['results']) == 2
    assert {u1.id, u2.id} == {r['id'] for r in resp['results']}
    assert 'password' not in resp['results'][0]
    assert 'password' not in resp['results'][1]


def test_not_admin_failure(client, add_user):
    _ = add_user(role=ROLE_USER, log_him_in=True)
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
    ('sort_by', 'password'),
    ('sort_by', '-password'),
    ('sort_by', '--name'),
])
def test_wrong_params_failure(client, add_user, param, value):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)
    resp = client.get(
        endpoint=endpoint,
        check_status=400,
        **{param: value}    
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
    assert param in resp['errors'][0].lower()
