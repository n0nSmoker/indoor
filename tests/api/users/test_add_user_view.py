import pytest

from lib.utils import get_random_str

from app.users.models import User
from app.users.constants import ROLES, ROLE_USER, ROLE_ADMIN, ROLE_MANAGER
from tests.helpers import add_publisher


endpoint = 'users.add_user_view'


@pytest.mark.parametrize("role", [ROLES[0][0], ROLES[1][0], ROLES[2][0]])
def test_default(client, add_user, role):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)
    role_is_manager = role == ROLE_MANAGER

    name = f'User-{get_random_str()}'
    password = get_random_str()
    email = f'{get_random_str()}@new.com'
    data = dict(
        name=name,
        password=password,
        email=email,
        role=role,
    )

    if role_is_manager:
        publisher = add_publisher()
        data['publisher_id'] = publisher.id

    resp = client.post(
        endpoint=endpoint,
        data=data,
    )
    assert 'id' in resp
    instance = User.query.get(resp['id'])
    assert instance

    assert instance.name == name
    assert instance.email == email
    assert instance.role == role
    if role_is_manager:
        assert instance.publisher_id == publisher.id


def test_default_role(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    name = f'User-{get_random_str()}'
    password = get_random_str()
    email = f'{get_random_str()}@new.com'
    resp = client.post(
        endpoint=endpoint,
        data=dict(
            name=name,
            password=password,
            email=email,
        )
    )
    assert 'id' in resp
    instance = User.query.get(resp['id'])
    assert instance

    assert instance.name == name
    assert instance.email == email
    assert instance.role == ROLE_USER  # the default role


def test_not_admin_failure(client, add_user):
    _ = add_user(role=ROLE_USER, log_him_in=True)

    _ = client.post(
        endpoint=endpoint,
        data=dict(
            name=f'User-{get_random_str()}',
            password=get_random_str(),
            email=f'{get_random_str()}@new.com',
        ),
        check_status=403
    )


def test_duplicate_email_failure(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    name = f'User-{get_random_str()}'
    password = get_random_str()
    email = f'{get_random_str()}@new.com'
    resp = client.post(
        endpoint=endpoint,
        data=dict(
            name=name,
            password=password,
            email=email,
        )
    )
    assert 'id' in resp
    instance = User.query.get(resp['id'])
    assert instance
    assert instance.email == email

    resp = client.post(
        endpoint=endpoint,
        data=dict(
            name=name,
            password=password,
            email=email,
        ),
        check_status=400
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
    assert 'email' in resp['errors'][0].lower()


@pytest.mark.parametrize("name,password,email", [
    (None, get_random_str(), f'{get_random_str()}@new.com',),
    (f'User-{get_random_str()}', None, f'{get_random_str()}@new.com',),
    (f'User-{get_random_str()}', get_random_str(), None,),
])
def test_no_required_params_failure(client, add_user, name, password, email):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    resp = client.post(
        endpoint=endpoint,
        data=dict(
            name=name,
            password=password,
            email=email,
        ),
        check_status=400
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
    info = resp['errors'][0]
    for var_name in ('name', 'email', 'password'):
        val = locals()[var_name]
        if val is None:
            assert var_name in info


@pytest.mark.parametrize("role", [ROLE_MANAGER, ROLE_ADMIN])
def test_user_publisher_id_field(client, add_user, role):
    """
    Checks that user can not add manager without publisher_id and admin with it
    """
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    name = f'User-{get_random_str()}'
    password = get_random_str()
    email = f'{get_random_str()}@new.com'
    data = dict(
        name=name,
        password=password,
        email=email,
        role=role,
    )
    if role == ROLE_ADMIN:
        publisher = add_publisher()
        data['publisher_id'] = publisher.id
    resp = client.post(
        endpoint=endpoint,
        data=data,
        check_status=400
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
    assert 'publisher_id' in resp['errors'][0]
