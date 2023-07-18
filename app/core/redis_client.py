from datetime import datetime, timedelta

from fakeredis import FakeRedis
from redis.client import Redis
from redis.exceptions import LockError

from app.core.config import settings

MAX_ATTEMPTS = 10


class RedisClient:
    failed_attempts = 0

    def __init__(self):
        self.connected = False
        self._client = FakeRedis()

    @property
    def client(self):
        return self.get_redis_client()

    def get_redis_client(self) -> Redis:
        if self.connected and self._client:
            return self._client
        client = Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, password=settings.REDIS_PW
        )
        if not client.ping():
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
