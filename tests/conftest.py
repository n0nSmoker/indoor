import pytest

from app.users.utils import get_user_by_id, create_user
from app.users.constants import ROLE_USER

from app.publishers.utils import save_publisher

from lib.auth.manager import AuthManager
from lib.factory import create_app, create_db, create_tables, drop_db, init_app
from lib.utils import get_random_str

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


@db_func_fixture(scope='module')
def add_publisher():
    def func(name=None, comment=None, airtime=None, created_by=None):
        return save_publisher(
            name=name or get_random_str(),
            comment=comment,
            airtime=airtime,
            created_by=created_by
        )
    return func


@db_func_fixture(scope='module')
def add_user(client):
    def func(name=None, email=None, password=None, role=ROLE_USER, log_him_in=False, **kwargs):
        name = name or f'User_{get_random_str()}'
        email = email or f'{get_random_str()}@email.com'
        password = password or get_random_str()

        user = create_user(
            name=name,
            email=email,
            password=password,
            role=role,
            **kwargs
        )

        if log_him_in:
            client.post(
                endpoint='users.login_user_view',
                data=dict(
                    email=email,
                    password=password
                )
            )

        return user
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
