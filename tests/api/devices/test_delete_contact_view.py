from app.devices.models import Contact
from app.users.constants import ROLE_USER, ROLE_ADMIN
from tests.helpers import add_contact

endpoint = 'devices.delete_contact_view'


def test_default(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    contact = add_contact()
    resp = client.delete(
        endpoint=endpoint,
        contact_id=contact.id,
    )
    assert 'id' in resp
    assert resp['id'] == contact.id
    assert not Contact.query.get(resp['id'])


def test_not_admin_failure(client, add_user):
    _ = add_user(role=ROLE_USER, log_him_in=True)

    contact = add_contact()
    _ = client.delete(
        endpoint=endpoint,
        contact_id=contact.id,
        check_status=403
    )


def test_wrong_id_failure(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    contact = add_contact()
    _ = client.delete(
        endpoint=endpoint,
        contact_id=129129129129192,
        check_status=404
    )
    assert Contact.query.get(contact.id)
