import redis


class RedisUtils(object):

    def __init__(self):
        self._redis = self._get_connection('localhost', 6379)

    def _get_connection(self, ahost, aport):
        pool = redis.ConnectionPool(host=ahost, port=aport, decode_responses=True)
        return redis.Redis(connection_pool=pool)

    def set(self, name, value, exp):
        self._redis.set(name, value, exp)

    def get(self, name):
        return self._redis.get(name)

