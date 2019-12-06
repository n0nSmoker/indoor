import pytest
from lib.utils import get_random_str

from app.publishers.models import Publisher
from app.users.constants import ROLE_ADMIN, ROLE_USER


endpoint = 'publishers.update_publisher_view'


@pytest.mark.parametrize("name,comment,airtime", [
    (get_random_str(), None, None),
    (get_random_str(), get_random_str(), None,),
    (get_random_str(), get_random_str(), 10.5,),
])
def test_default(client, add_user, add_publisher, name, comment, airtime):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    publisher = add_publisher()
    resp = client.put(
        endpoint=endpoint,
        publisher_id=publisher.id,
        data=dict(
            name=name,
            comment=comment,
            airtime=airtime,
        )
    )
    assert 'id' in resp
    assert resp['id'] == publisher.id
    updated_publisher = Publisher.query.filter_by(id=resp['id']).one_or_none()
    assert updated_publisher

    assert 'name' in resp
    assert updated_publisher.name == name == resp['name']

    assert 'comment' in resp
    assert updated_publisher.comment == comment == resp['comment']

    assert 'airtime' in resp
    assert updated_publisher.airtime == airtime == resp['airtime']


def test_no_params_failure(client, add_user, add_publisher):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    publisher = add_publisher()
    _ = client.put(
        endpoint=endpoint,
        publisher_id=publisher.id,
        check_status=400,
        data=dict(
            name=None,
            comment=None,
            airtime=None,
        )
    )


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
def test_malformed_params_failure(client, add_user, add_publisher, name, comment, airtime, param_name):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    publisher = add_publisher()
    resp = client.put(
        endpoint=endpoint,
        publisher_id=publisher.id,
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
