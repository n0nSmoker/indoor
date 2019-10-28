from app.users.models import User


module_name = 'user'


def test_create_user(client):
    resp = client.post(
        endpoint=f'{module_name}s.add_{module_name}_view',
    )
    assert 'data' in resp
    data = resp['data']
    assert 'id' in data
    assert User.query.filter_by(id=data['id']).one_or_none()


def test_user_list(client):
    resp = client.get(
        endpoint=f'{module_name}s.list_view',
    )
    assert 'data' in resp
    data = resp['data']
    assert 'results' in data
    assert 'total' in data


def test_user_by_id(client):
    resp = client.get(
        endpoint=f'{module_name}s.{module_name}_by_id_view',
        user_id=User.query.first().id,
    )
    assert 'data' in resp
    data = resp['data']
    assert 'id' in data


def test_update_user(client):
    resp = client.put(
        endpoint=f'{module_name}s.update_{module_name}_view',
        user_id=User.query.first().id,
    )
    assert 'data' in resp
    data = resp['data']
    assert 'id' in data
    assert User.query.filter_by(id=data['id']).one().to_dict() == data


def test_delete_user(client):
    resp = client.delete(
        endpoint=f'{module_name}s.delete_{module_name}_view',
        user_id=User.query.first().id,
    )
    assert 'data' in resp
    data = resp['data']
    assert not User.query.filter_by(id=data['id']).one_or_none()
