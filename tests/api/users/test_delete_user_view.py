from app.users.models import User


endpoint = 'users.delete_user_view'


def test_default(client, add_user):
    user = add_user()
    resp = client.delete(
        endpoint=endpoint,
        user_id=user.id,
    )
    assert 'id' in resp
    assert resp['id'] == user.id
    assert not User.query.filter_by(id=resp['id']).one_or_none()


def test_wrong_id_failure(client, add_user):
    user = add_user()
    _ = client.delete(
        endpoint=endpoint,
        user_id=129129129129192,
        check_status=404
    )
    assert User.query.filter_by(id=user.id).one_or_none()
