from app.users.constants import ROLE_ADMIN, ROLE_USER
from tests.helpers import add_publisher

endpoint = 'publishers.publisher_by_id_view'


def test_default(client, add_user, add_publisher):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    publisher = add_publisher()
    resp = client.get(
        endpoint=endpoint,
        publisher_id=publisher.id,
    )
    assert 'id' in resp
    assert resp['id'] == publisher.id

    assert 'name' in resp
    assert resp['name'] == publisher.name

    assert 'created_by' not in resp


def test_not_admin_failure(client, add_user):
    _ = add_user(role=ROLE_USER, log_him_in=True)

    publisher = add_publisher()
    _ = client.get(
        endpoint=endpoint,
        publisher_id=publisher.id,
        check_status=403
    )


def test_wrong_id_failure(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    publisher = add_publisher()
    _ = client.get(
        endpoint=endpoint,
        publisher_id=publisher.id + 100,
        check_status=404
    )
