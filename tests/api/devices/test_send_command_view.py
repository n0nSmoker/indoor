import pytest

from app.devices import constants as DEVICE
from lib.utils import get_random_str

endpoint = 'devices.send_command_view'


@pytest.mark.parametrize("command,device_ids", [
    ('info', ['1'],),
    ('restart', ['1', '2'],),
    ('restart_device', ['1', get_random_str()],),
    ('restart_device', [get_random_str()],),
])
def test_default(client, app, command, device_ids):
    resp = client.post(
        endpoint=endpoint,
        data=dict(
            command=command,
            device_ids=device_ids,
        ),
    )
    assert DEVICE.REDIS_KEY + '/' + device_ids[0] in resp


@pytest.mark.parametrize("command,device_ids", [
    ('test', ['1'],),
    ('', ['1'],),
    (None, ['1'],),
    (get_random_str(), ['1'],),
])
def test_malformed_params_failure(client, app, command, device_ids):
    resp = client.post(
        endpoint=endpoint,
        data=dict(
            command=command,
            device_ids=device_ids,
        ),
        check_status=400
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
