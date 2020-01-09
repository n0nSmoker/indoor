from flask import Blueprint

from lib.utils import success
from lib.webargs import parser

from .schemas import OSVersionSchema


mod = Blueprint('system', __name__, url_prefix='/system')


@mod.route('/version/')
@parser.use_kwargs(OSVersionSchema)
def current_version_view(os_version):
    """
    Get last available software version for given OS
    ---
    get:
        tags:
          - System
        security:
          - cookieAuth: []
        parameters:
        - in: query
          schema: OSVersionSchema
        responses:
          200:
            content:
              application/json:
                schema: SoftwareVersionSchema
          403:
            description: Forbidden
          400:
            content:
              application/json:
                schema: FailSchema
          5XX:
            description: Unexpected error
    """
    return success({
        'version': f'1.13.64 for {os_version}',
        'download_url': f'https://download.software/1.13.64.{os_version}.file',
    })
