from flask import Blueprint

from lib.utils import success, fail
from lib.webargs import parser

from .utils import save_device_health
from .models import DeviceHealth, DeviceHealthException
from .schemas import (OSVersionSchema, FilterDeviceHealthSchema, DeviceHealthListSchema,
                      DeviceHealthSchema, AddDeviceHealthSchema,)


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
        'version': f'1.13.64',
        'os_version': os_version,
        'download_url': f'https://download.software/1.13.64_{os_version.replace(" ", "_")}.file',
    })


@mod.route('/health/')
@parser.use_kwargs(FilterDeviceHealthSchema())
def devices_health_list_view(page, limit, sort_by, device_id, start_date_time, end_date_time):
    """Get list of devices health.
    ---
    get:
      tags:
        - System
      security:
        - cookieAuth: []
      parameters:
      - in: query
        schema: FilterDeviceHealthSchema
      responses:
        200:
          content:
            application/json:
              schema: DeviceHealthListSchema
        403:
          description: Forbidden
        400:
          content:
            application/json:
              schema: FailSchema
        5XX:
          description: Unexpected error
    """
    q = DeviceHealth.query

    if device_id:
        q = q.filter(DeviceHealth.device_id == device_id)
    if start_date_time:
        q = q.filter(DeviceHealth.created_at >= start_date_time)
    if end_date_time:
        q = q.filter(DeviceHealth.created_at <= end_date_time)

    total = q.count()
    q = q.order_by(sort_by).offset((page - 1) * limit).limit(limit)
    return success(DeviceHealthListSchema().dump(dict(
        results=q,
        total=total,
    )))


@mod.route('/health/', methods=['POST'])
@parser.use_kwargs(AddDeviceHealthSchema())
def add_device_health_view(**kwargs):
    """Add device health
    ---
    post:
      tags:
        - System
      security:
        - cookieAuth: []
      requestBody:
        content:
          application/x-www-form-urlencoded:
            schema: AddDeviceHealthSchema
      responses:
        200:
          content:
            application/json:
              schema: DeviceHealthSchema
        400:
          content:
            application/json:
              schema: FailSchema
        403:
          description: Forbidden
        5XX:
          description: Unexpected error
    """
    try:
        device_health = save_device_health(**kwargs)
    except DeviceHealthException as e:
        return fail(str(e))

    return success(DeviceHealthSchema().dump(device_health))
