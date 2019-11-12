import pytest
from lib.utils import get_random_str


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


@pytest.mark.parametrize('email,password', [
    (None, 'GHJKLKJHJK'),
    ('email@mail.ru', None),
    ('', 'Passasasewewe'),
    ('email@mmail.ru', ''),
    ('WrongEmail.ru', 'asdadadssdas'),
    ('WrongEmail@ru', 'asdadadssdas'),
    ('smallPassword@mmm.ru', '123'),
    ('TooSmallPassword@mmm.ru', '123ww'),
    ('TooLongPassword@mmm.ru', get_random_str(101)),
])
def test_wrong_param_failure(client, email, password):
    _ = client.post(
        endpoint=endpoint,
        check_status=400,
        data=dict(
            email=email,
            password=password
        ))
