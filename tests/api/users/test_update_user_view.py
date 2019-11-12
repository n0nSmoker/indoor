import pytest

from lib.utils import get_random_str

from app.users.models import User
from app.users.constants import ROLE_MANAGER, ROLE_ADMIN


endpoint = 'users.update_user_view'


@pytest.mark.parametrize("name,role,email", [
    (None, ROLE_MANAGER, f'{get_random_str()}@new.com',),
    (f'User-{get_random_str()}', None, f'{get_random_str()}@new.com',),
    (f'User-{get_random_str()}', ROLE_ADMIN, None,),
])
def test_default(client, add_user, name, role, email):
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
    new_user = User.query.filter_by(id=resp['id']).one_or_none()
    assert new_user

    for var_name in ('name', 'email', 'role'):
        val = locals()[var_name]
        if val is not None:
            assert getattr(user, var_name) == val


def test_no_params_failure():
    pass


def test_malformed_params_failure():
    pass


def test_not_all_params_passed_failure():
    pass
