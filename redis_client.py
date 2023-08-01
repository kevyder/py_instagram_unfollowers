import redis
from constants import REDIS_URL


class RedisClient:
    def __init__(self):
        self.url = REDIS_URL

    def connect(self):
        try:
            self.connection = redis.Redis.from_url(url=self.url)
            self.connection.ping()  # Test the connection
            print("Connected to Redis server.")
        except redis.ConnectionError as e:
            raise ConnectionError(f"Could not connect to Redis server: {e}")

    def get(self, key):
        try:
            return self.connection.lrange(key, 0, -1)
        except redis.RedisError as e:
            raise Exception(f"Error retrieving value from Redis: {e}")

    def delete(self, key):
        try:
            self.connection.delete(key)
        except redis.RedisError as e:
            raise Exception(f"Error deleting value from Redis: {e}")

    def rpush(self, key, *values):
        try:
            self.connection.rpush(key, *values)
        except redis.RedisError as e:
            raise Exception(f"Error pushing elements to Redis list: {e}")

    def disconnect(self):
        try:
            if self.connection is not None:
                self.connection.close()
                print("Disconnected from Redis server.")
        except redis.ConnectionError as e:
            raise ConnectionError(f"Could not disconnect from Redis server: {e}")
