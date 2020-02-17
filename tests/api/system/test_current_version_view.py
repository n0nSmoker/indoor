import pytest

from lib.utils import get_random_str
from app.system.constants import OS


endpoint = 'system.current_version_view'


@pytest.mark.parametrize("os_name", [
    *OS,
])
def test_default(client, os_name):
    resp = client.get(
        endpoint=endpoint,
        os_name=os_name
    )
    assert 'version' in resp
    assert 'download_url' in resp


@pytest.mark.parametrize("os_name, param_name", [
    # Malformed os_version
    (None, 'os_name'),
    (get_random_str(255, punctuation=True), 'os_name'),
])
def test_malformed_params_failure(client, os_name, param_name):
    resp = client.get(
        endpoint=endpoint,
        os_name=os_name,
        check_status=400,
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
    assert param_name in resp['errors'][0].lower()
