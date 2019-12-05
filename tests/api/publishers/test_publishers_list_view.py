import pytest

from app.users.constants import ROLE_ADMIN, ROLE_USER


endpoint = 'publishers.publishers_list_view'


def test_default(client, add_user, add_publisher):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    publisher = add_publisher()
    resp = client.get(
        endpoint=endpoint
    )
    assert 'total' in resp
    assert resp['total'] > 0
    assert 'results' in resp
    assert any([r['id'] == publisher.id for r in resp['results']])
    assert 'created_by' not in resp['results'][0]


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
    ('sort_by', 'created_by'),
    ('sort_by', '-created_by'),
    ('sort_by', '--name'),
])
def test_wrong_params_failure(client, add_user, param, value):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)
    _ = client.get(
        endpoint=endpoint,
        check_status=400,
        **{param: value}    
    )
