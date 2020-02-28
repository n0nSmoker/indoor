import pytest

endpoint = 'devices.send_command_view'


@pytest.mark.parametrize("command,device_ids", [
    ('info', [1],),
])
def test_default(client, app, command, device_ids):
    redis_key = 'test'
    resp = client.post(
        endpoint=endpoint,
        data=dict(
            command=command,
            device_ids=device_ids,
            redis_key=redis_key,
        ),
    )
    assert 'command' in resp
    assert 'device_ids' in resp
    assert resp['command'] == command
    assert resp['device_ids'] == device_ids
    assert b'info1' in app.cache.storage.lrange(redis_key, start=0, end=-1)
    app.cache.storage.rpop(redis_key)


@pytest.mark.parametrize("command,device_ids", [
    ('test', [1],),
    ('', [1],),
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
