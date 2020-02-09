import pytest

from lib.utils import get_random_str

from app.devices.models import Device


endpoint = 'devices.register_device_view'


@pytest.mark.parametrize("token", [
    get_random_str(10)
])
def test_default(client, token):

    resp = client.post(
        endpoint=endpoint,
        data=dict(
            uid_token=token,
        )
    )
    assert 'access_token' in resp
    assert resp['access_token']

    assert 'id' in resp
    device = Device.query.filter_by(id=resp['id']).one_or_none()
    assert device

    assert len(resp.keys()) == 2


@pytest.mark.parametrize("token", [
    None,
    123,
    '',
    get_random_str(9),
    get_random_str(256),
])
def test_malformed_params_failure(client, token):
    resp = client.post(
        endpoint=endpoint,
        data=dict(
            uid_token=token,
        ),
        check_status=400
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
    assert 'uid_token' in resp['errors'][0].lower()
