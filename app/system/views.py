from flask import Blueprint

from app.common.decorators import auth_required, device_auth_required
from app.content.schemas import FileListSchema, File
from lib.auth.manager import current_device
from lib.utils import success, fail
from lib.webargs import parser

from .utils import save_device_health
from .models import DeviceHealth, DeviceHealthException
from .schemas import (OSVersionSchema, FilterDeviceHealthSchema, DeviceHealthListSchema,
                      DeviceHealthSchema, AddDeviceHealthSchema,)


mod = Blueprint('system', __name__, url_prefix='/system')


@mod.route('/version/')
@parser.use_kwargs(OSVersionSchema)
def current_version_view(os_name):
    """
    Get last available software version for given OS
    ---
    get:
        tags:
          - System
        parameters:
        - in: query
          schema: OSVersionSchema
        responses:
          200:
            content:
              application/json:
                schema: SoftwareVersionSchema
          400:
            content:
              application/json:
                schema: FailSchema
          5XX:
            description: Unexpected error
    """
    return success({
        'version': f'1.13.64',
        'os_name': os_name,
        'download_url': f'https://0.0.0.0/1.13.64_{os_name}.file',
    })


@mod.route('/health/')
@auth_required
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
@device_auth_required
@parser.use_kwargs(AddDeviceHealthSchema())
def add_device_health_view(**kwargs):
    """Add device health
    ---
    post:
      tags:
        - System
      security:
        - tokenAuth: []
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
        5XX:
          description: Unexpected error
    """
    try:
        device_health = save_device_health(device_id=current_device.id, **kwargs)
    except DeviceHealthException as e:
        return fail(str(e))

    return success(DeviceHealthSchema().dump(device_health))


@mod.route('/commands/')
@device_auth_required
def commands_view():
    """Get list of device commands.
    ---
    get:
      tags:
        - System
      security:
        - tokenAuth: []
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  results:
                    type: array
                    items:
                      type: object
                      properties:
                        name:
                          type: string
        400:
          content:
            application/json:
              schema: FailSchema
        5XX:
          description: Unexpected error
    """
    # TODO: get device specified commands list # noqa
    return success(dict(results=[]))


@mod.route('/logs/', methods=['POST'])
@device_auth_required
def logs_view():
    """Save device logs file.
    ---
    post:
      tags:
        - System
      security:
        - tokenAuth: []
      responses:
        200:
          content:
            application/json:
              schema:
                type: string
                example: ok
        400:
          content:
            application/json:
              schema: FailSchema
        5XX:
          description: Unexpected error
    """
    # TODO: save logs file somewhere # noqa
    return success('ok')


@mod.route('/content/')
@device_auth_required
def device_content_list_view():
    # TODO: return device specified files list # noqa
    return success(FileListSchema().dump(dict(
        results=File.query.limit(100)
    )))


@mod.route('/content/<int:file_id>/show/', methods=['POST'])
@device_auth_required
def device_content_show_view(file_id):  # noqa
    # TODO: save file show # noqa
    return success('ok')
