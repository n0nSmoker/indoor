from lib.factory import create_app, create_db, create_tables, drop_db, init_app
import pytest


from .utils import Client


APP_NAME = 'indoor'

@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    test_app = create_app(name=APP_NAME)
    init_app(test_app)
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
def session(app, request): #noqa
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
def client(app): #noqa
    return Client(app=app)


@pytest.fixture(scope='session')
def empty_list_resp():
    return dict(results=[], total=0)


