import pytest

from lib.utils import get_random_str

from tests.helpers import add_contact

from app.users.constants import ROLE_ADMIN, ROLE_USER
from app.devices.models import Contact


endpoint = 'devices.update_contact_view'


def test_default(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)
    contact_id = add_contact().id
    resp = client.put(
        endpoint=endpoint,
        contact_id=contact_id,
        data=dict(
            name=get_random_str(),
            tel=get_random_str(),
            comment=get_random_str(),
        )
    )
    assert 'id' in resp
    contact = Contact.query.get(resp['id'])
    assert contact

    assert 'name' in resp
    assert resp['name'] == contact.name
    assert 'tel' in resp
    assert resp['tel'] == contact.tel
    assert 'comment' in resp
    assert resp['comment'] == contact.comment


def test_not_admin_failure(client, add_user):
    _ = add_user(role=ROLE_USER, log_him_in=True)
    contact_id = add_contact().id
    resp = client.put(
        endpoint=endpoint,
        contact_id=contact_id,
        data=dict(
            name=get_random_str(),
            tel=get_random_str(),
            comment=get_random_str(),
        ),
        check_status=403
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1


@pytest.mark.parametrize("name,tel,comment", [
    (None, get_random_str(), get_random_str()),
    (get_random_str(), None, get_random_str()),
    (get_random_str(), '', get_random_str()),
    ('', get_random_str(), get_random_str()),
    (get_random_str(), get_random_str(9), ''),
    (get_random_str(4), get_random_str(), ''),
    (get_random_str(256), get_random_str(), ''),
    (get_random_str(), get_random_str(256), ''),
    (get_random_str(), get_random_str(), get_random_str(1025)),
])
def test_malformed_params_failure(client, add_user, name, tel, comment):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)
    contact_id = add_contact().id
    resp = client.put(
        endpoint=endpoint,
        contact_id=contact_id,
        data=dict(
            name=name,
            tel=tel,
            comment=comment,
        ),
        check_status=400
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
