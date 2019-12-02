import pytest
from lib.utils import get_random_str


endpoint = 'users.logout_user_view'


def test_default(app, client, add_user):
    password = 'someStr0ngPassw000rd!@#$'
    user = add_user(password=password)

    # Login
    _ = client.post(
        endpoint='users.login_user_view',
        check_cookies={
            app.config.get('AUTH_COOKIE_NAME'): True
        },
        data=dict(
            email=user.email,
            password=password
        ))

    # Logout
    resp = client.post(
        endpoint=endpoint
    )
    assert resp == 'ok'

    # Second call should fail
    _ = client.post(
        endpoint=endpoint,
        check_status=403
    )


def test_not_authorised_failure(client):
    _ = client.post(
        endpoint=endpoint,
        check_status=403
    )
