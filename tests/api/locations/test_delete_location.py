from app.locations.models import Location
from app.users.constants import ROLE_USER, ROLE_ADMIN
from tests.helpers import add_location

endpoint = 'locations.delete_location_view'


def test_default(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    location = add_location()
    resp = client.delete(
        endpoint=endpoint,
        location_id=location.id,
    )
    assert 'id' in resp
    assert resp['id'] == location.id
    assert not Location.query.get(resp['id'])


def test_not_admin_failure(client, add_user):
    _ = add_user(role=ROLE_USER, log_him_in=True)

    location = add_location()
    _ = client.delete(
        endpoint=endpoint,
        location_id=location.id,
        check_status=403
    )


def test_wrong_id_failure(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    location = add_location()
    _ = client.delete(
        endpoint=endpoint,
        location_id=129129129129192,
        check_status=404
    )
    assert Location.query.get(location.id)
