import pytest
from flask import current_app as app

from app.devices import constants as DEVICE

from lib.utils import get_random_str
from random import randint

key1 = randint(10**9, 10**9+100)
key2 = randint(10**9, 10**9+100)
key3 = randint(10**9, 10**9+100)

endpoint = 'devices.send_command_view'


@pytest.mark.parametrize("command,device_ids", [
    (DEVICE.COMMANDS[0][1], [key1],),
    (DEVICE.COMMANDS[1][1], [key1, key2],),
    (DEVICE.COMMANDS[1][1], [key1, key2, key3],),
])
def test_default(client, command, device_ids):
    resp = client.post(
        endpoint=endpoint,
        data=dict(
            command=command,
            device_ids=device_ids,
        ),
    )
    assert 'Ok' in resp
    assert f'{command}' in resp
    assert f'{len(device_ids)}' in resp
    redis_key = DEVICE.REDIS_KEY + DEVICE.REDIS_KEY_DELIMITER
    assert command.encode('ascii') in app.cache.storage.lrange(redis_key + f'{device_ids[0]}', start=0, end=-1)

    # Deleting a test records in redis storage
    for i in device_ids:
        assert command.encode('ascii') == app.cache.storage.rpop(redis_key + f'{i}')


@pytest.mark.parametrize("command,device_ids", [
    # Malformed command
    (None, [key1],),
    ('', [key1],),
    ('test', [key1],),
    (get_random_str(), [key1],),

    # Malformed device_ids
    (DEVICE.COMMANDS[0][1], [''],),
    (DEVICE.COMMANDS[0][1], ['1a'],),
    (DEVICE.COMMANDS[0][1], ['abc'],),
    (DEVICE.COMMANDS[0][1], ['1,2,,3'],),
    (DEVICE.COMMANDS[0][1], [get_random_str()],),
])
def test_malformed_params_failure(client, command, device_ids):
    resp = client.post(
        endpoint=endpoint,
        data=dict(
            command=command,
            device_ids=device_ids,
        ),
        check_status=400,
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
