import pytest
from lib.utils import get_random_str

from app.users.models import User
from app.users.constants import ROLE_MANAGER, ROLE_ADMIN, ROLE_USER


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
    resp = client.put(
        endpoint=endpoint,
        user_id=user.id,
        data=dict(
            name=name,
            role=role,
            email=email,
        )
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
