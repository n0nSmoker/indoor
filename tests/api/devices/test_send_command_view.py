import pytest

from app.devices import constants as DEVICE
from lib.utils import get_random_str

endpoint = 'devices.send_command_view'


@pytest.mark.parametrize("command,device_ids", [
    ('info', ['1', '2'],),
    ('restart', ['1', get_random_str()],),
    ('restart_device', [get_random_str()],),
])
def test_default(client, app, command, device_ids):
    test_ids = ['test|' + i for i in device_ids]
    resp = client.post(
        endpoint=endpoint,
        data=dict(
            command=command,
            device_ids=test_ids,
        ),
    )
    test_key = DEVICE.REDIS_KEY + DEVICE.REDIS_KEY_DELIMITER + 'test|'
    assert test_key + device_ids[0] in resp
    assert command in resp.values()
    assert command.encode('ascii') in app.cache.storage.lrange(test_key + device_ids[0], start=0, end=-1)

    # deleting a test records in redis storage
    for i in device_ids:
        app.cache.storage.rpop(test_key + i)



@pytest.mark.parametrize("command,device_ids", [
    # Malformed command
    ('test', ['1'],),
    ('', ['1'],),
    (None, ['1'],),
    (get_random_str(), ['1'],),

    # Malformed device_ids
    ('info', [''],),
    ('info', None,),
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
