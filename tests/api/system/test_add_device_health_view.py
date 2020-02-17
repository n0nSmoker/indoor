import pytest
from uuid import uuid4

from lib.utils import get_random_str

from app.system.models import DeviceHealth
from config import AUTH_TOKEN_HEADER_NAME
from tests.helpers import add_device


endpoint = 'system.add_device_health_view'


@pytest.mark.parametrize("software_version", [
    # Valid parameters
    get_random_str(255, punctuation=True),
    None,
])
def test_default(client, software_version):
    device = add_device(uid_token=str(uuid4()))
    resp = client.post(
        endpoint=endpoint,
        data=dict(
            software_version=software_version,
        ),
        headers={
            AUTH_TOKEN_HEADER_NAME: f'{device.id}:{device.access_token}',
        },
    )
    assert 'id' in resp
    device_health = DeviceHealth.query.filter_by(id=resp['id']).one_or_none()
    assert device_health

    assert device_health.device_id == device.id
    assert device_health.software_version == software_version


@pytest.mark.parametrize("software_version,param_name", [
    # Malformed software_version
    (get_random_str(length=256), 'software_version'),
    (1, 'software_version'),
    (1.0, 'software_version'),
])
def test_malformed_params_failure(client, software_version, param_name):
    device = add_device(uid_token=str(uuid4()))
    resp = client.post(
        endpoint=endpoint,
        data=dict(
            software_version=software_version,
        ),
        headers={
            AUTH_TOKEN_HEADER_NAME: f'{device.id}:{device.access_token}',
        },
        check_status=400,
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
    assert param_name in resp['errors'][0].lower()
