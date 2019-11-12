import pytest

from app.users.utils import get_user_by_id
from lib.auth import AuthManager
from lib.factory import create_app, create_db, create_tables, drop_db, init_app
from lib.utils import get_random_str

from app.users.models import User

from .utils import Client, db_func_fixture


APP_NAME = 'indoor'


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    test_app = create_app(name=APP_NAME)
    init_app(test_app)
    AuthManager(test_app, get_user_func=get_user_by_id)

    dsn = test_app.config['SQLALCHEMY_DATABASE_URI']
    drop_db(dsn)
    create_db(dsn)
    
    # Establish an application context before running the tests.
    ctx = test_app.app_context()
    ctx.push()

    create_tables(test_app)  # Only after context was pushed

    # Add test client
    test_app.client = test_app.test_client()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return test_app


@pytest.fixture
def session(app, request):  #noqa
    """Creates a new database session for a test."""
    connection = app.db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    test_session = app.db.create_scoped_session(options=options)

    app.db.session = test_session

    def teardown():
        transaction.rollback()
        connection.close()
        test_session.remove()

    request.addfinalizer(teardown)
    return test_session


@pytest.fixture(scope='session')
def client(app):  #noqa
    return Client(app=app)


@pytest.fixture(scope='session')
def empty_list_resp():
    return dict(results=[], total=0)


@db_func_fixture(scope='module')
def add_user(client):
    def func(name=None, email=None, password=None, role=None, log_him_in=False):
        req = dict(
            name=name or f'User_{get_random_str()}',
            email=email or f'{get_random_str()}@email.com',
            password=password or get_random_str(),
        )
        if role:
            req['role'] = role

        resp = client.post(
            endpoint=f'users.add_user_view',
            data=req
        )
        assert 'id' in resp

        if log_him_in:
            client.post(
                endpoint='users.login_user_view',
                data=dict(
                    email=req['email'],
                    password=req['password']
                )
            )

        return User.query.filter_by(id=resp['id']).one()
    return func


@pytest.fixture(scope='session')
def login(app, client):
    def func(email, password):
        _ = client.post(
            endpoint='users.login_user_view',
            data=dict(
                email=email,
                password=password
            )
        )
        cookie = client.get_cookies(key=app.config['AUTH_COOKIE_NAME'])
        return cookie.value  # SID
    return func


