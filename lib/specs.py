import logging

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from flask import jsonify
from flask_swagger_ui import get_swaggerui_blueprint


logger = logging.getLogger('specs')
logger.setLevel(logging.DEBUG)


def register_swagger(app, title, version, openapi_version="3.0.2",
                     swagger_url='/api/docs',
                     security_schemes=None
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
            app.spec.path(view=view)

    # Add security schemes if needed
    if security_schemes:
        assert isinstance(security_schemes, dict)
        for lbl, info in security_schemes.items():
            app.spec.components.security_scheme(lbl, info)

    # Add Swagger UI
    api_path = '/swagger.json'
    blueprint = get_swaggerui_blueprint(
        base_url = swagger_url,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        api_url = swagger_url + api_path,
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
    def swagger_json_view():
        return jsonify(app.spec.to_dict())

    # Register swaggerUI blueprint
    app.register_blueprint(blueprint, url_prefix=swagger_url)
