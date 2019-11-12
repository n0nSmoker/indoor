
endpoint = 'users.list_view'


def test_default(client, add_user):
    user = add_user(log_him_in=True)
    resp = client.get(
        endpoint=endpoint
    )
    assert 'total' in resp
    assert resp['total'] > 0
    assert 'results' in resp
    assert any([r['id'] == user.id for r in resp['results']])


def test_wrong_params_failure():
    pass
