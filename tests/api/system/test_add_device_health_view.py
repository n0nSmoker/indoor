import pytest

from lib.utils import get_random_str

from app.system.models import DeviceHealth

from app.users.constants import ROLE_USER


endpoint = 'system.add_device_health_view'


@pytest.mark.parametrize("device_id,software_version", [
    # Valid parameters
    (get_random_str(255, punctuation=True), get_random_str(255, punctuation=True)),
    (get_random_str(1, punctuation=True), None),
])
def test_default(client, device_id, software_version):
    resp = client.post(
        endpoint=endpoint,
        data=dict(
            device_id=device_id,
            software_version=software_version
        )
    )
    assert 'id' in resp
    device_health = DeviceHealth.query.filter_by(id=resp['id']).one_or_none()
    assert device_health

    assert device_health.device_id == device_id
    assert device_health.software_version == software_version


@pytest.mark.parametrize("device_id,software_version,param_name", [
    # Malformed device_id
    ('', None, 'device_id'),
    (None, None, 'device_id'),
    (1, None, 'device_id'),
    (1.0, None, 'device_id'),

    # Malformed software_version
    (get_random_str(), get_random_str(length=256), 'software_version'),
    (get_random_str(), 1, 'software_version'),
    (get_random_str(), 1.0, 'software_version'),
])
def test_malformed_params_failure(client, device_id, software_version, param_name):
    resp = client.post(
        endpoint=endpoint,
        data=dict(
            device_id=device_id,
            software_version=software_version,
        ),
        check_status=400
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
    assert param_name in resp['errors'][0].lower()
