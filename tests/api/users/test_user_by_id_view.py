from app.users.constants import ROLE_ADMIN

endpoint = 'users.user_by_id_view'


def test_defaut(client, add_user):
    _ = add_user(role=ROLE_ADMIN, log_him_in=True)

    user = add_user()
    resp = client.get(
        endpoint=endpoint,
        user_id=user.id,
    )
    assert 'id' in resp
    assert resp['id'] == user.id

    assert 'name' in resp
    assert resp['name'] == user.name

    assert 'role' in resp
    assert resp['role'] == user.role

    assert 'password' not in resp
