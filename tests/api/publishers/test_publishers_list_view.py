import pytest

from lib.utils import get_random_str

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


@pytest.mark.parametrize('param', ['comment', 'name'])
def test_search_mode(client, add_user, add_publisher, param):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    # Create publishers
    common_string = get_random_str(15)
    params = [
        {param: common_string + get_random_str()},
        {param: common_string + get_random_str()},
        {param: get_random_str() + common_string},
        {param: get_random_str() + common_string + get_random_str()},
    ]
    publishers = [add_publisher(**p) for p in params]
    # Add trash publishers to make some noise
    [add_publisher(**{param: get_random_str()}) for _ in range(10)]

    # Prepare test cases
    param2publisher_ids = [
        (getattr(publishers[0], param)[:-1], {publishers[0].id}),
        (common_string, {p.id for p in publishers})
    ]
    # Run test cases
    for search, publisher_ids in param2publisher_ids:
        resp = client.get(
            endpoint=endpoint,
            **{param: search}
        )
        assert 'total' in resp
        assert resp['total'] == len(publisher_ids)

        assert 'results' in resp
        assert {r['id'] for r in resp['results']} == publisher_ids


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

    ('name', get_random_str(1)),
    ('name', get_random_str(2)),
    ('name', get_random_str(101)),

    ('comment', get_random_str(1)),
    ('comment', get_random_str(2)),
    ('comment', get_random_str(101)),
])
def test_wrong_params_failure(client, add_user, param, value):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)
    _ = client.get(
        endpoint=endpoint,
        check_status=400,
        **{param: value}    
    )
