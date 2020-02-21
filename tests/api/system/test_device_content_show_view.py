from config import AUTH_TOKEN_HEADER_NAME
from tests.helpers import add_content, add_device


endpoint = 'system.device_content_show_view'


def test_default(client, add_user):
    user = add_user()
    content = add_content(created_by=user.id)
    device = add_device()
    resp = client.post(
        endpoint=endpoint,
        file_id=content.id,
        headers={
            AUTH_TOKEN_HEADER_NAME: f'{device.id}:{device.access_token}',
        },
    )
    assert resp == 'ok'
