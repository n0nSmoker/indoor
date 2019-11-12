import logging
import subprocess
from flask import url_for
from IPython import embed
from lib.factory import create_app, create_db, drop_db, init_app, is_db_exists


from lib.swagger import init_docs
from lib.utils import ApiException, find_models_and_tables
from lib.auth import AuthManager


from app.users.utils import get_user_by_id


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S'
)


app = create_app(name='indoor')
init_app(app)
AuthManager(app, get_user_func=get_user_by_id)

app.register_error_handler(ApiException, lambda err: err.to_result())

init_docs(app=app, title='indoor API', version='0.0.1')


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
def routes():
    """ List all avalable routes """
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)


if __name__ == '__main__':
    app.run()
