import pytest

from lib.utils import get_random_str

from app.publishers.models import Publisher

from app.users.constants import ROLE_USER, ROLE_ADMIN


endpoint = 'publishers.add_publisher_view'


@pytest.mark.parametrize("name,comment,airtime", [
    # Valid parameters
    ('123', None, None),
    ('SomeName', '1', None),
    ('_', '_', 10),
    ('\t', '_', 15.5),
    ('|Ё|', '_', .5),
    ('   ', '   ', 100),
])
def test_default(client, add_user, name, comment, airtime):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)
    
    resp = client.post(
        endpoint=endpoint,
        data=dict(
            name=name,
            comment=comment,
            airtime=airtime,
        )
    )
    assert 'id' in resp
    publisher = Publisher.query.get(resp['id'])
    assert publisher

    assert publisher.name == name
    assert publisher.comment == comment
    assert publisher.airtime == airtime


def test_not_admin_failure(client, add_user):
    _ = add_user(role=ROLE_USER, log_him_in=True)

    _ = client.post(
        endpoint=endpoint,
        data=dict(
            name=get_random_str(),
        ),
        check_status=403
    )


def test_duplicate_name_failure(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    name = f'Name-{get_random_str()}'
    resp = client.post(
        endpoint=endpoint,
        data=dict(
            name=name,
        )
    )
    assert 'id' in resp
    publisher = Publisher.query.get(resp['id'])
    assert publisher
    assert publisher.name == name

    resp = client.post(
        endpoint=endpoint,
        data=dict(
            name=name,
        ),
        check_status=400
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
    assert 'name' in resp['errors'][0].lower()


@pytest.mark.parametrize("name,comment,airtime,param_name", [
    # Malformed name
    (None, get_random_str(), None, 'name'),
    (1, get_random_str(), None, 'name'),
    (100, get_random_str(), None, 'name'),
    ('', get_random_str(), None, 'name'),

    # Malformed comment
    (get_random_str(), 0, None, 'comment'),
    (get_random_str(), 10, None, 'comment'),
    (get_random_str(), 100, None, 'comment'),
    (get_random_str(), -10, None, 'comment'),
    (get_random_str(), .5, None, 'comment'),

    # Malformed airtime
    (get_random_str(), get_random_str(), 0, 'airtime'),
    (get_random_str(), get_random_str(), 105, 'airtime'),
    (get_random_str(), get_random_str(), -10, 'airtime'),
    (get_random_str(), get_random_str(), -.5, 'airtime'),

])
def test_malformed_params_failure(client, add_user, name, comment, airtime, param_name):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    resp = client.post(
        endpoint=endpoint,
        data=dict(
            name=name,
            comment=comment,
            airtime=airtime,
        ),
        check_status=400
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
    assert param_name in resp['errors'][0].lower()
