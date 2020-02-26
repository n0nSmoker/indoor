
class Cache:
    """
    Abstract cache class
    """
    delim = ':'
    prefixes = dict(
        auth='auth'
    )

    def __init__(self, storage):
        self.storage = storage

    def _get(self, key):
        """
        Returns value by key
        :param key:
        :return: bytes
        """
        raise NotImplementedError('Depends on storage type')

    def _set(self, key, value, ttl=None):
        """
        Saves value
        :param key:
        :param value:
        :param ttl: time to live in seconds
        :return:
        """
        raise NotImplementedError('Depends on storage type')

    def _del(self, *keys):
        """
        Deletes value
        :param keys: list of strings
        :return:
        """
        raise NotImplementedError('Depends on storage type')

    def _get_auth_key(self, token):
        """
        Generates cache-key for auth data
        :param token:
        :return:
        """
        return f'{self.prefixes["auth"]}{self.delim}{token}'

    def get_user_id(self, token):
        """
        Returns user_id from storage
        :param token: str
        :return: str
        """
        return self._get(
            key=self._get_auth_key(token)
        )

    def set_user_id(self, user_id, token):
        """
        Saves user_id in storage
        :param user_id:
        :param token:
        :return:
        """
        self._set(
            key=self._get_auth_key(token),
            value=user_id,
            ttl=3600
        )

    def invalidate_auth_token(self, token):
        """
        Removes token and user data from the storage
        :param token:
        :return:
        """
        self._del(self._get_auth_key(token))


class RedisCache(Cache):
    def _get(self, key):
        return self.storage.get(key)

    def _set(self, key, value, ttl=None):
        self.storage.set(name=key, value=value, ex=ttl)

    def _del(self, *keys):
        self.storage.delete(*keys)
