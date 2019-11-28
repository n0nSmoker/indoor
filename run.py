import logging
import os
import subprocess

from IPython import embed
from lib.factory import create_app, create_db, drop_db, init_app, is_db_exists
from lib.specs import register_swagger
from lib.utils import ApiException, find_models_and_tables
from lib.auth import AuthManager

from app.users.utils import get_user_by_id


logging.basicConfig(
    level=os.environ.get('LOG_LEVEL', logging.WARNING),
    format='%(asctime)s | %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S'
)


app = create_app(name='indoor')
init_app(app)
AuthManager(app, get_user_func=get_user_by_id)

# Register specs and SwaggerUI
register_swagger(
    app=app,
    title='Indoor API',
    version='0.1',
    security_schemes={
        "cookieAuth": {
            "type": "apiKey",
            "in": "cookie",
            "name": app.config['AUTH_COOKIE_NAME']
        }
    }
)

app.register_error_handler(ApiException, lambda err: err.to_result())


@app.cli.command()
def init():
    """Creates all tables, admin and so on if needed"""
    dsn = app.config.get('SQLALCHEMY_DATABASE_URI')
    if dsn:
        if not is_db_exists(dsn):
            create_db(dsn)


@app.cli.command()
def drop_all():
    """Drop and recreates all tables"""
    dsn = app.config.get('SQLALCHEMY_DATABASE_URI')
    if dsn and input('Do you want to DROP DATABASE:%s ?!' % dsn):
        drop_db(dsn)


@app.cli.command()
def debug():
    """Runs the shell with own context and ipython"""
    import re  # noqa
    import os  # noqa
    from pprintpp import pprint as p  # noqa
    from lib.factory import db  # noqa

    shell_context = locals()
    shell_context.update(find_models_and_tables())

    embed(user_ns=shell_context)


@app.cli.command()
def dbshell():
    connect_args = app.db.engine.url.translate_connect_args()
    connect_url = "postgresql://{username}:{password}@{host}:{port}/{database}".format(**connect_args)
    subprocess.call(['pgcli', connect_url])


@app.cli.command()
def addadmin():
    """ Create admin user """
    from app.users.utils import create_user
    from app.users.constants import ROLE_ADMIN

    email = input('Email: ')
    password = input('Password: ')

    create_user(
        email=email,
        password=password,
        role=ROLE_ADMIN,
        name=email.split('@')[0]
    )

    logging.info('Administrator user - email:%s password:%s Successfully created', email, password)


if __name__ == '__main__':
    app.run()
