import pytest

from lib.utils import get_random_str

from app.users.models import User
from app.users.constants import ROLES, ROLE_ANON


module_name = 'user'


@pytest.mark.parametrize("role", [ROLES[0][0], ROLES[1][0], ROLES[2][0]])
def test_create_user_default(client, role):
    name = f'User-{get_random_str()}'
    password = get_random_str()
    email = f'{get_random_str()}@new.com'
    resp = client.post(
        endpoint=f'{module_name}s.add_{module_name}_view',
        data=dict(
            name=name,
            password=password,
            email=email,
            role=role,
        )
    )
    assert 'data' in resp
    data = resp['data']
    assert 'id' in data
    instance = User.query.filter_by(id=data['id']).one_or_none()
    assert instance

    assert instance.name == name
    assert instance.email == email
    assert instance.role == role


def test_create_user_no_role(client):
    name = f'User-{get_random_str()}'
    password = get_random_str()
    email = f'{get_random_str()}@new.com'
    resp = client.post(
        endpoint=f'{module_name}s.add_{module_name}_view',
        data=dict(
            name=name,
            password=password,
            email=email,
        )
    )

    assert 'data' in resp
    data = resp['data']
    assert 'id' in data
    instance = User.query.filter_by(id=data['id']).one_or_none()
    assert instance

    assert instance.name == name
    assert instance.email == email
    assert instance.role == ROLE_ANON  # the default role


def test_create_user_duplicate_email(client):
    name = f'User-{get_random_str()}'
    password = get_random_str()
    email = f'{get_random_str()}@new.com'
    resp = client.post(
        endpoint=f'{module_name}s.add_{module_name}_view',
        data=dict(
            name=name,
            password=password,
            email=email,
        )
    )

    assert 'data' in resp
    data = resp['data']
    assert 'id' in data
    instance = User.query.filter_by(id=data['id']).one_or_none()
    assert instance
    assert instance.email == email

    resp = client.post(
        endpoint=f'{module_name}s.add_{module_name}_view',
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
def test_create_user_no_required_params(client, name, password, email):
    resp = client.post(
        endpoint=f'{module_name}s.add_{module_name}_view',
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


def test_user_list(client, add_user):
    user = add_user()
    resp = client.get(
        endpoint=f'{module_name}s.list_view',
    )
    assert 'data' in resp
    data = resp['data']
    assert 'total' in data
    assert data['total'] > 0
    assert 'results' in data
    assert any([r['id'] == user.id for r in data['results']])


def test_user_by_id(client, add_user):
    user = add_user()
    resp = client.get(
        endpoint=f'{module_name}s.{module_name}_by_id_view',
        user_id=user.id,
    )
    assert 'data' in resp
    data = resp['data']

    assert 'id' in data
    assert data['id'] == user.id

    assert 'name' in data
    assert data['name'] == user.name

    assert 'role' in data
    assert data['role'] == user.role

    assert 'password' not in data


def test_update_user(client, add_user):
    user = add_user()
    new_name = 'GHJKJHGHJKJHJK123NNAAME'
    resp = client.put(  
        endpoint=f'{module_name}s.update_{module_name}_view',
        user_id=user.id,
        data=dict(
            name=new_name,
        )
    )
    assert 'data' in resp
    data = resp['data']

    assert 'id' in data
    assert data['id'] == user.id
    new_user = User.query.filter_by(id=data['id']).one_or_none()
    assert new_user

    assert new_user.name == new_name


def test_delete_user(client, add_user):
    user = add_user()
    resp = client.delete(
        endpoint=f'{module_name}s.delete_{module_name}_view',
        user_id=user.id,
    )
    assert 'data' in resp
    data = resp['data']

    assert 'id' in data
    assert data['id'] == user.id
    assert not User.query.filter_by(id=data['id']).one_or_none()
