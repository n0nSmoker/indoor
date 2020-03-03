import pytest
from flask import current_app as app
from tests.helpers import add_command

from app.devices import constants as DEVICE

from random import randint

device_id = randint(10 ** 9, 10 ** 9 + 100)
command1 = DEVICE.COMMANDS[0][1]
command2 = DEVICE.COMMANDS[1][1]

endpoint = 'devices.commands_by_id_view'


def test_default(client):
    add_command(command=command1, device_id=device_id)  # Create first record on redis storage by device_id
    add_command(command=command2, device_id=device_id)  # Create second record on redis storage by device_id
    resp = client.get(
        endpoint=endpoint,
        device_id=device_id,
    )
    assert len(resp) == 2  # two records created by the test id
    assert command1 == resp[0] and command2 == resp[1]
    redis_key = DEVICE.REDIS_KEY + DEVICE.REDIS_KEY_DELIMITER
    assert resp[0].encode('ascii') in app.cache.storage.lrange(redis_key + f'{device_id}', start=0, end=-1)
    assert resp[1].encode('ascii') in app.cache.storage.lrange(redis_key + f'{device_id}', start=0, end=-1)

    # Deleting a test records in redis storage
    assert command2.encode('ascii') == app.cache.storage.rpop(redis_key + f'{device_id}')
    assert command1.encode('ascii') == app.cache.storage.rpop(redis_key + f'{device_id}')

