import os
from datetime import datetime, timedelta

from fakeredis import FakeRedis
from redis import from_url as get_redis_client_from_url
from redis.client import Redis
from redis.exceptions import LockError

MAX_ATTEMPTS = 10


class RedisClient:
    failed_attempts = 0

    def __init__(self, db: int = 1):
        self.host_url = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379")
        self.db = db
        self.connected = False
        self._client = FakeRedis()

    @property
    def client(self):
        return self.get_redis_client()

    def get_redis_client(self) -> Redis:
        if self.connected and self._client:
            return self._client
        if os.environ.get("ENV", "DEV") == "TEST":  # pragma: no cover
            self.connected = True
            print("ENV=TEST, using FakeRedis client")
            return self._client
        client = get_redis_client_from_url(self.host_url, db=self.db)
        if not client.ping():  # pragma: no cover
            self.failed_attempts += 1
            if self.failed_attempts < MAX_ATTEMPTS:
                print("Redis server did not respond to PING message.")
                return self._client
            else:
                self._client = FakeRedis()
                self.connected = True
                print(f"Failed to connect to Redis server after {MAX_ATTEMPTS} failed attempts")
                return self._client
        self.connected = True
        self._client = client
        print("Redis client is connected to server.")
        return self._client

    def rate_limit_exceeded(self, key: str, rate: int, period: timedelta, burst: int) -> tuple[bool, float]:
        arrived_at = datetime.now().timestamp()
        emission_interval = round(int(period.total_seconds()) / float(rate))
        self.client.setnx(key, 0)
        try:
            with self.client.lock("lock:" + key, blocking_timeout=5):
                tat = float(self.client.get(key) or 0)
                allowed_at = tat - (emission_interval * burst)
                if allowed_at <= arrived_at:
                    new_tat = max(tat, arrived_at) + emission_interval
                    self.client.set(key, new_tat)
                    return (False, 0)
                return (True, allowed_at)
        except LockError:  # pragma: no cover
            return (True, 0)


redis = RedisClient()
