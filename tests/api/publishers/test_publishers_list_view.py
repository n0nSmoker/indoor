import pytest

from lib.utils import get_random_str

from app.users.constants import ROLE_ADMIN, ROLE_USER
from tests.helpers import add_publisher

endpoint = 'publishers.publishers_list_view'

search_fields = ['name', 'comment']


def test_default(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    publisher = add_publisher()
    resp = client.get(
        endpoint=endpoint
    )
    assert 'total' in resp
    assert resp['total'] == 1
    assert 'results' in resp
    assert len(resp['results']) == 1
    assert publisher.id == resp['results'][0]['id']
    assert 'created_by' not in resp['results'][0]


def test_search_mode(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    # Create publishers
    test_cases = []
    all_ids = set()
    common_string = get_random_str(15)
    for params in [[f] for f in search_fields] + [search_fields]:
        # Add trash publishers to make some noise
        add_publisher(**{p: get_random_str() for p in params})
        
        # Add publishers with common string in params
        prefixed = common_string + get_random_str()
        postfixed = get_random_str() + common_string
        middle = get_random_str() + common_string + get_random_str()

        prefixed_id = add_publisher(**{p: prefixed for p in params}).id
        all_ids.update({
            prefixed_id,
            add_publisher(**{p: postfixed for p in params}).id,
            add_publisher(**{p: middle for p in params}).id,
        })
        test_cases.append((prefixed[:-1], {prefixed_id}))
    # Add common test case
    test_cases.append((common_string, all_ids))
    
    # Run test cases
    for query, publisher_ids in test_cases:
        resp = client.get(
            endpoint=endpoint,
            query=query,
            query_fields=[f for f in search_fields]
        )
        assert 'total' in resp
        assert resp['total'] == len(publisher_ids)

        assert 'results' in resp
        assert {r['id'] for r in resp['results']} == publisher_ids


def test_search_mode_failure(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    common_string = get_random_str(15)
    test_cases = [
        (add_publisher(**{p: get_random_str() + common_string}), p)
        for p in search_fields
    ]
    for publisher, param in test_cases:
        resp = client.get(
            endpoint=endpoint,
            query=common_string,
            query_fields=list(set(search_fields) - {param})
        )
        assert 'results' in resp
        assert publisher.id not in {r['id'] for r in resp['results']}


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

    ('query', get_random_str(1)),
    ('query', get_random_str(2)),
    ('query', get_random_str(101)),

    ('query_fields', search_fields + ['some_wrong_value']),
    ('query_fields', ['some_wrong_value']),
    ('query_fields', 'not_even_a_list'),
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
