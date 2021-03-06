import logging

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from flask import jsonify
from flask_swagger_ui import get_swaggerui_blueprint

from werkzeug.routing import FloatConverter, IntegerConverter

from lib.auth.decorators import basic_auth_decorator

logger = logging.getLogger('specs')
logger.setLevel(logging.DEBUG)


def register_swagger(app, title, version, openapi_version="3.0.2",
                     swagger_url='/api/docs',
                     security_schemes=None,
                     username=None,
                     password=None
                     ):
    """
    Generates specs and registers SwaggerUI blueprint
    :param app:
    :param str title: app title
    :param str version: app version
    :param str openapi_version:
    :param str swagger_url: URL for swaggerUI
    :param dict security_schemes: Swagger security schemas
        To get Examples see:
        https://apispec.readthedocs.io/en/latest/special_topics.html#documenting-security-schemes
        https://swagger.io/docs/specification/authentication/
    :param str username: Username for basic auth.
        No auth on swagger blueprint if None
    :param str password: Password for basic auth
    :return:
    """
    # Generate specs
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
            app.spec.path(
                view=view,
                parameters=get_inline_params(app, endpoint=key)
            )

    # Add security schemes if needed
    if security_schemes:
        assert isinstance(security_schemes, dict)
        for lbl, info in security_schemes.items():
            app.spec.components.security_scheme(lbl, info)

    # Add Swagger UI
    api_path = '/swagger.json'
    blueprint = get_swaggerui_blueprint(
        base_url=swagger_url,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        api_url=swagger_url + api_path,
        config=None,  # Swagger UI config overrides
        # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration.
        #    'clientId': "your-client-id",
        #    'clientSecret': "your-client-secret-if-required",
        #    'realm': "your-realms",
        #    'appName': "your-app-name",
        #    'scopeSeparator': " ",
        #    'additionalQueryStringParams': {'test': "hello"}
        # }
    )

    # Add Swagger JSON route
    @blueprint.route(api_path)
    @basic_auth_decorator(
        username=username,
        password=password,
    )
    def swagger_json_view():
        return jsonify(app.spec.to_dict())

    # Register swaggerUI blueprint
    app.register_blueprint(blueprint, url_prefix=swagger_url)


def get_inline_params(app, endpoint):
    """
    Extracts inline params from endpoint and
    returns respective params for spec
    :param app:
    :param endpoint:
    :return:
    """
    parameters = []
    # Get url (APISpec works only with the first one)
    url = app.url_map._rules_by_endpoint[endpoint][0]

    # Check all inline params
    for param, type_ in url._converters.items():
        # Convert flask params type to swagger ones
        type_ = {
            IntegerConverter: 'integer',
            FloatConverter: 'number',
        }.get(type(type_), 'string')

        # Add param
        parameters.append({
            'in': 'path',
            'name': param,
            'schema': {'type': type_}
        })
    return parameters

