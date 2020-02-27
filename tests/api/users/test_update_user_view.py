import pytest
from lib.utils import get_random_str

from app.users.models import User
from app.users.constants import ROLE_MANAGER, ROLE_ADMIN, ROLE_USER
from tests.helpers import add_publisher


endpoint = 'users.update_user_view'


@pytest.mark.parametrize("name,role,email", [
    (None, ROLE_MANAGER, f'{get_random_str()}@new.com',),
    (f'User-{get_random_str()}', None, f'{get_random_str()}@new.com',),
    (f'User-{get_random_str()}', ROLE_ADMIN, None,),
    (f'User-{get_random_str()}', ROLE_USER, None,),
])
def test_default(client, add_user, name, role, email):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    user = add_user()
    data = dict(
        name=name,
        role=role,
        email=email,
    )
    if role == ROLE_MANAGER:
        publisher = add_publisher()
        data['publisher_id'] = publisher.id
    resp = client.put(
        endpoint=endpoint,
        user_id=user.id,
        data=data,
    )
    assert 'id' in resp
    assert resp['id'] == user.id
    new_user = User.query.get(resp['id'])
    assert new_user

    for var_name in ('name', 'email', 'role'):
        val = locals()[var_name]
        if val is not None:
            assert getattr(user, var_name) == val


def test_no_params_failure(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    user = add_user()
    _ = client.put(
        endpoint=endpoint,
        user_id=user.id,
        check_status=400,
        data=dict(
            name=None,
            role=None,
            email=None,
        )
    )


@pytest.mark.parametrize("name,role,email", [
    (None, 'WrongRole', f'{get_random_str()}@new.com',),
    (123, None, f'{get_random_str()}@new.com',),
    (f'User-{get_random_str()}', ROLE_ADMIN, 'Wrong_email',),
    (f'User-{get_random_str()}', ROLE_USER, 'Wrong_.email@',),
])
def test_malformed_params_failure(client, add_user, name, role, email):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    user = add_user()
    _ = client.put(
        endpoint=endpoint,
        user_id=user.id,
        check_status=400,
        data=dict(
            name=name,
            role=role,
            email=email,
        )
    )


@pytest.mark.parametrize("role", [ROLE_MANAGER, ROLE_ADMIN])
def test_user_publisher_id_field(client, add_user, role):
    """
    Checks that user can not update role to manager without publisher_id and admin with it
    """
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)
    user = add_user()

    data = dict(role=role)
    if role == ROLE_ADMIN:
        publisher = add_publisher()
        data['publisher_id'] = publisher.id
    resp = client.put(
        endpoint=endpoint,
        user_id=user.id,
        data=data,
        check_status=400
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
    assert 'publisher_id' in resp['errors'][0]
