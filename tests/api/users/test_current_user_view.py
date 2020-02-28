from app.users.constants import ROLE_ADMIN


endpoint = 'users.current_user_view'


def test_defaut(client, add_user):
    """
    Checks that user can get his own data
    """
    user = add_user(role=ROLE_ADMIN, log_him_in=True)

    resp = client.get(endpoint=endpoint)
    assert 'id' in resp
    assert resp['id'] == user.id

    assert 'name' in resp
    assert resp['name'] == user.name

    assert 'role' in resp
    assert resp['role'] == user.role

    assert 'is_admin' in resp
    assert resp['is_admin'] == user.is_admin

    assert 'password' not in resp


def test_without_login(client):
    """
    Check 403 if user is not logged in
    """
    client.get(endpoint=endpoint, check_status=403)
