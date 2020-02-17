import pytest
from uuid import uuid4
from datetime import datetime, timedelta

from lib.utils import get_random_str
from tests.helpers import add_device_health, add_device

endpoint = 'system.devices_health_list_view'


def test_default(client, add_user):
    _ = add_user(log_him_in=True)
    device = add_device(uid_token=str(uuid4()))
    device_health = add_device_health(device_id=device.id)

    resp = client.get(
        endpoint=endpoint
    )
    assert 'total' in resp
    assert resp['total'] > 0
    assert 'results' in resp
    assert any([r['id'] == device_health.id for r in resp['results']])


def test_filter_by_id(client, add_user):
    _ = add_user(log_him_in=True)
    device1 = add_device(uid_token=str(uuid4()))
    device2 = add_device(uid_token=str(uuid4()))
    device_health_first = add_device_health(device_id=device1.id)
    device_health_second = add_device_health(device_id=device2.id)

    resp = client.get(
        endpoint=endpoint,
        device_id=device_health_first.device_id
    )

    assert 'total' in resp
    assert resp['total'] > 0
    assert 'results' in resp
    assert all([r['device']['id'] == device_health_first.device_id for r in resp['results']])
    assert all([r['device']['id'] != device_health_second.device_id for r in resp['results']])


def test_filter_by_date_range(client, add_user):
    _ = add_user(log_him_in=True)
    device = add_device(uid_token=str(uuid4()))
    date_time_now = datetime.utcnow()
    date_time_future = date_time_now + timedelta(days=5)
    date_time_past = date_time_now - timedelta(days=5)
    device_health_future = add_device_health(device_id=device.id, created_at=date_time_future)
    device_health_now = add_device_health(device_id=device.id, created_at=date_time_now)
    device_health_past = add_device_health(device_id=device.id, created_at=date_time_past)
    resp = client.get(
        endpoint=endpoint,
        start_date_time=date_time_now,
        end_date_time=date_time_future
    )

    assert 'total' in resp
    assert resp['total'] > 0
    assert 'results' in resp
    date_time_now_str = datetime.strftime(date_time_now, '%Y-%m-%dT%H:%M:%S.%f')
    date_time_future_str = datetime.strftime(date_time_future, '%Y-%m-%dT%H:%M:%S.%f')
    assert all([r['created_at'] >= date_time_now_str for r in resp['results']])
    assert all([r['created_at'] <= date_time_future_str for r in resp['results']])
    assert any([r['id'] == device_health_now.id or r['id'] == device_health_future.id for r in resp['results']])
    assert not any([r['id'] == device_health_past.id for r in resp['results']])


@pytest.mark.parametrize('param,value', [
    ('page', -1),
    ('page', -10),
    ('page', 101),
    ('page', 0),

    ('limit', 0),
    ('limit', 1001),
    ('limit', -1),
    ('limit', -10),

    ('sort_by', 'wrong_field'),
    ('sort_by', '-wrong_field'),
    ('sort_by', 'created_by'),
    ('sort_by', '-created_by'),
    ('sort_by', '--name'),

    ('start_date_time', 1),
    ('start_date_time', get_random_str()),

    ('end_date_time', 1),
    ('end_date_time', get_random_str()),
])
def test_malformed_params_failure(client, add_user, param, value):
    _ = add_user(log_him_in=True)
    resp = client.get(
        endpoint=endpoint,
        check_status=400,
        **{param: value}
    )
    assert 'errors' in resp
    assert len(resp['errors']) == 1
    assert param in resp['errors'][0].lower()
