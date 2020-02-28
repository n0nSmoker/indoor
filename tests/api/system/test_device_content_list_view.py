from app.users.constants import ROLE_MANAGER
from tests.helpers import add_content, add_device

from config import AUTH_TOKEN_HEADER_NAME


endpoint = 'system.device_content_list_view'


def test_default(client, add_user):
    user = add_user(role=ROLE_MANAGER)
    _ = add_content(created_by=user.id, publisher_id=user.publisher_id)
    device = add_device()

    resp = client.get(
        endpoint=endpoint,
        headers={
            AUTH_TOKEN_HEADER_NAME: f'{device.id}:{device.access_token}',
        },
    )

    assert 'results' in resp
    assert resp['results']
    for file in resp['results']:
        assert 'id' in file
        assert 'src' in file
