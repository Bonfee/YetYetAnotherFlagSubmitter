import redis
from config import Config


# Initialize new redis connection
class RedisConnection(object):

    def __init__(self):
        self.red = redis.Redis(Config.Redis.ip, Config.Redis.port)
