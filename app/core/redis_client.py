import time
from datetime import datetime, timedelta

from fakeredis import FakeRedis
from redis.client import Redis
from redis.exceptions import LockError

from app.core.config import settings
from app.core.result import Result
from app.core.util import get_duration_from_timestamp

MAX_ATTEMPTS = 10


class RedisClient:
    def __init__(self):
        self.connected: bool = False
        self.failed_attempts: int = 0
        self.host_url: str = settings.REDIS_HOST
        self.host_port: int = settings.REDIS_PORT
        self.redis_db: int = settings.REDIS_DB
        self.redis_pw: str = settings.REDIS_PW
        self.rate_limit: int = settings.RATE_LIMIT_PER_PERIOD
        self.rate_limit_period: timedelta = settings.RATE_LIMIT_PERIOD_SECONDS
        self.rate_limit_burst: int = settings.RATE_LIMIT_BURST
        self.client: Redis = FakeRedis()

    @property
    def failed_to_connect(self):
        return not self.connected and self.failed_attempts >= MAX_ATTEMPTS

    def get_redis_client(self) -> Redis:
        if self.connected:
            return self.client
        while not self.connected and self.failed_attempts < MAX_ATTEMPTS:
            result = self._connect_to_server()
            if result.success and result.value:
                self.client = result.value
                self.connected = True
            else:
                self.failed_attempts += 1
                time.sleep(3)
        return self.client

    def _connect_to_server(self) -> Result[Redis]:
        client = Redis(host=self.host_url, port=self.host_port, db=self.redis_db, password=self.redis_pw)
        if client.ping():
            return Result.Ok(client)
        return Result.Fail("Redis server did not respond to PING message.")

    def rate_limit_exceeded(self, key: str) -> Result:
        allowed_at: float = 0.0
        arrived_at = datetime.now().timestamp()
        emission_interval = round(int(self.rate_limit_period.total_seconds()) / float(self.rate_limit))
        self.client.setnx(key, 0)
        try:
            with self.client.lock("lock:" + key, blocking_timeout=5):
                tat = float(self.client.get(key) or 0)
                allowed_at = tat - (emission_interval * self.rate_limit_burst)
                if allowed_at < arrived_at:
                    new_tat = max(tat, arrived_at) + emission_interval
                    self.client.set(key, new_tat)
                    return Result.Ok()
                return Result.Fail(self._get_limit_exceeded_error_message(allowed_at))
        except LockError:  # pragma: no cover
            return Result.Fail(self._get_limit_exceeded_error_message(allowed_at))

    def _get_limit_exceeded_error_message(self, allowed_at: float) -> str:
        limit_duration = get_duration_from_timestamp(allowed_at)
        return (
            f"API rate limit of {self.rate_limit} requests in {self.rate_limit_period.seconds} seconds exceeded, "
            f"please wait {limit_duration} before submitting another request"
        )


redis = RedisClient()
