import logging

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin


logger = logging.getLogger('specs')
logger.setLevel(logging.DEBUG)


def register_specs(app, title, version, openapi_version="3.0.2"):
    app.spec = APISpec(
        title=title,
        version=version,
        openapi_version=openapi_version,
        plugins=[FlaskPlugin(), MarshmallowPlugin()],
    )

    with app.test_request_context():
        logger.debug('Registering view functions in APISpec...')
        for key, view in app.view_functions.items():
            logger.debug('Register view:%s', key)
            app.spec.path(view=view)
