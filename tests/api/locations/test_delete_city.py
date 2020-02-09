from app.locations.models import City
from app.users.constants import ROLE_USER, ROLE_ADMIN
from tests.helpers import add_city

endpoint = 'locations.delete_city_view'


def test_default(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    city = add_city()
    resp = client.delete(
        endpoint=endpoint,
        city_id=city.id,
    )
    assert 'id' in resp
    assert resp['id'] == city.id
    assert not City.query.get(resp['id'])


def test_not_admin_failure(client, add_user):
    _ = add_user(role=ROLE_USER, log_him_in=True)

    city = add_city()
    _ = client.delete(
        endpoint=endpoint,
        city_id=city.id,
        check_status=403
    )


def test_wrong_id_failure(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    city = add_city()
    _ = client.delete(
        endpoint=endpoint,
        city_id=129129129129192,
        check_status=404
    )
    assert City.query.get(city.id)
