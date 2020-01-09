import pytest

from lib.utils import get_random_str

endpoint = 'system.current_version_view'


def test_default(client):
    resp = client.get(
        endpoint=endpoint,
        os_version=get_random_str(150)
    )
    assert 'version' in resp
    assert 'download_url' in resp


@pytest.mark.parametrize("os_version, param_name", [
    # Malformed os_version
    (None, 'os_version'),
    (get_random_str(1025), 'os_version'),
])
def test_malformed_params_failure(client, os_version, param_name):
    resp = client.get(
        endpoint=endpoint,
        os_version=os_version,
        check_status=400,
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
    assert param_name in resp['errors'][0].lower()
