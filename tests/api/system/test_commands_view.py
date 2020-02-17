from uuid import uuid4

from config import AUTH_TOKEN_HEADER_NAME
from tests.helpers import add_device


endpoint = 'system.commands_view'


def test_default(client):
    device = add_device(uid_token=str(uuid4()))
    resp = client.get(
        endpoint=endpoint,
        headers={
            AUTH_TOKEN_HEADER_NAME: f'{device.id}:{device.access_token}',
        },
    )
    assert 'results' in resp
    assert isinstance(resp['results'], list)
