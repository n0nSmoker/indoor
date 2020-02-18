import pytest

from app.users.constants import ROLE_ADMIN, ROLE_USER, ROLE_MANAGER, STATUS_ARCHIVE
from lib.utils import get_random_str


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


def test_search_mode(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    name = 'string_in_name'
    names = [
        f'some prefix {name}',
        f'{name} some postfix',
        f'prefix {name} postfix',
        name,
    ]

    email = 'string_in_email'
    emails = [
        f'some_prefix_{email}',
        f'{email}_some_postfix',
        f'prefix_{email}_postfix',
        email,
    ]

    ids = set()
    for n, e in zip(names, emails):
        user = add_user(name=n, email=e)
        ids.add(user.id)

    # Check results
    for string in name, email:
        resp = client.get(
            endpoint=endpoint,
            query=string,
            limit=100  # To get all the results on one page
        )
        assert 'total' in resp
        assert resp['total'] == len(ids)
        assert 'results' in resp
        assert {r['id'] for r in resp['results']} == ids


def test_filter_role(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    for _ in range(5):
        add_user(role=ROLE_MANAGER)

    # Check results
    resp = client.get(
        endpoint=endpoint,
        role=ROLE_MANAGER,
        limit=100  # To get all the results on one page
    )
    assert 'results' in resp
    assert all(u['role'] == ROLE_MANAGER for u in resp['results'])


def test_filter_status(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    for _ in range(5):
        add_user(status=STATUS_ARCHIVE)

    # Check results
    resp = client.get(
        endpoint=endpoint,
        status=STATUS_ARCHIVE,
        limit=100  # To get all the results on one page
    )
    assert 'results' in resp
    assert all(u['status'] == STATUS_ARCHIVE for u in resp['results'])


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

    ('role', get_random_str(5)),

    ('status', get_random_str(5)),

    ('query', get_random_str(1)),
    ('query', get_random_str(2)),
    ('query', get_random_str(101)),
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
