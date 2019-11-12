from .models import User


def get_user_by_id(user_id):
    return User.query.get(int(user_id))
