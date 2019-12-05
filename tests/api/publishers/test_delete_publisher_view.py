from app.publishers.models import Publisher
from app.users.constants import ROLE_USER, ROLE_ADMIN


endpoint = 'publishers.delete_publisher_view'


def test_default(client, add_user, add_publisher):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    publisher = add_publisher()
    resp = client.delete(
        endpoint=endpoint,
        publisher_id=publisher.id,
    )
    assert 'id' in resp
    assert resp['id'] == publisher.id
    assert not Publisher.query.filter_by(id=resp['id']).one_or_none()


def test_not_admin_failure(client, add_user, add_publisher):
    _ = add_user(role=ROLE_USER, log_him_in=True)

    publisher = add_publisher()
    _ = client.delete(
        endpoint=endpoint,
        publisher_id=publisher.id,
        check_status=403
    )


def test_wrong_id_failure(client, add_user, add_publisher):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    publisher = add_publisher()
    _ = client.delete(
        endpoint=endpoint,
        publisher_id=129129129129192,
        check_status=404
    )
    assert Publisher.query.filter_by(id=publisher.id).one_or_none()
