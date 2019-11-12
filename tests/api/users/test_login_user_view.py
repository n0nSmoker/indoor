endpoint = 'users.login_user_view'


def test_default(app, client, add_user):
    password = 'someStr0ngPassw000rd!@#$'
    user = add_user(password=password)
    _ = client.post(
        endpoint=endpoint,
        check_cookies={
            app.config.get('AUTH_COOKIE_NAME'): True
        },
        data=dict(
            email=user.email,
            password=password
        ))
