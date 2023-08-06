import logging
import time
from datetime import datetime, timedelta

from fakeredis import FakeRedis
from redis import from_url
from redis.client import Redis
from redis.exceptions import ConnectionError, LockError

from app.core.config import settings
from app.core.result import Result
from app.core.util import get_duration_from_timestamp

MAX_ATTEMPTS = 3


class RedisClient:
    def __init__(self):
        self.logger = logging.getLogger("app.api.error")
        self.connected: bool = False
        self.failed_attempts: int = 0
        self.redis_host: str = settings.REDIS_HOST
        self.redis_host_port: int = settings.REDIS_PORT
        self.redis_db: int = settings.REDIS_DB
        self.redis_pw: str = settings.REDIS_PW
        self.rate_limit: int = settings.RATE_LIMIT_PER_PERIOD
        self.rate_limit_period: timedelta = settings.RATE_LIMIT_PERIOD_SECONDS
        self.rate_limit_burst: int = settings.RATE_LIMIT_BURST
        self._client: Redis = FakeRedis()

    @property
    def redis_url(self) -> str:
        return (
            f"redis://:{self.redis_pw}@{self.redis_host}:{self.redis_host_port}/{self.redis_db}"
            if self.redis_pw
            else f"redis://{self.redis_host}:{self.redis_host_port}/{self.redis_db}"
        )

    @property
    def client(self) -> Redis:
        return self.get_redis_client()

    def get_redis_client(self) -> Redis:
        while not self.connected and self.failed_attempts < MAX_ATTEMPTS:
            try:
                client = from_url(self.redis_url)
                if client.ping():
                    self._client = client
                    self.connected = True
                    self.logger.info("Successfully connected to Redis server.")
                else:
                    self.handle_connect_attempt_failed()
            except ConnectionError:
                self.handle_connect_attempt_failed()
        return self._client

    def handle_connect_attempt_failed(self):
        self.failed_attempts += 1
        if self.failed_attempts < MAX_ATTEMPTS:
            self.logger.info(
                "Redis server did not respond to ping, retrying... " f"(attempt {self.failed_attempts}/{MAX_ATTEMPTS})."
            )
            time.sleep(3)
        else:
            self._client = FakeRedis()
            self.connected = False
            self.logger.info(f"Failed to connect to Redis server (attempt {self.failed_attempts}/{MAX_ATTEMPTS}).")

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
                    self.logger.info(f"Request allowed for IP: {key}")
                    return Result.Ok()
                self.logger.info(f"Rate limit exceeded for IP: {key}")
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
