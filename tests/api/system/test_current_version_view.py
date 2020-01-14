import pytest

from lib.utils import get_random_str
from app.system.constants import OS


endpoint = 'system.current_version_view'


@pytest.mark.parametrize("os_version", [
    *OS,
])
def test_default(client, os_version):
    resp = client.get(
        endpoint=endpoint,
        os_version=os_version
    )
    assert 'version' in resp
    assert 'download_url' in resp


@pytest.mark.parametrize("os_version, param_name", [
    # Malformed os_version
    (None, 'os_version'),
    (get_random_str(255, punctuation=True), 'os_version'),
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
