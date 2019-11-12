import pytest

from lib.utils import get_random_str

from app.users.models import User
from app.users.constants import ROLES, ROLE_USER


endpoint = 'users.add_user_view'


@pytest.mark.parametrize("role", [ROLES[0][0], ROLES[1][0], ROLES[2][0]])
def test_default(client, role):
    name = f'User-{get_random_str()}'
    password = get_random_str()
    email = f'{get_random_str()}@new.com'
    resp = client.post(
        endpoint=endpoint,
        data=dict(
            name=name,
            password=password,
            email=email,
            role=role,
        )
    )
    assert 'id' in resp
    instance = User.query.filter_by(id=resp['id']).one_or_none()
    assert instance

    assert instance.name == name
    assert instance.email == email
    assert instance.role == role


def test_no_role_failure(client):
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
    instance = User.query.filter_by(id=resp['id']).one_or_none()
    assert instance

    assert instance.name == name
    assert instance.email == email
    assert instance.role == ROLE_USER  # the default role


def test_duplicate_email_failure(client):
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
    instance = User.query.filter_by(id=resp['id']).one_or_none()
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
    assert 'title' in resp
    assert resp['title'].lower().find('email') != -1


@pytest.mark.parametrize("name,password,email", [
    (None, get_random_str(), f'{get_random_str()}@new.com',),
    (f'User-{get_random_str()}', None, f'{get_random_str()}@new.com',),
    (f'User-{get_random_str()}', get_random_str(), None,),
])
def test_no_required_params_failure(client, name, password, email):
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
    assert 'meta' in resp['errors'][0]
    assert 'field' in resp['errors'][0]['meta']
    info = resp['errors'][0]['meta']['field']
    for var_name in ('name', 'email', 'password'):
        val = locals()[var_name]
        if val is None:
            assert info == var_name
