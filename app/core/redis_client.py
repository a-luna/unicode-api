import logging
import os
import time

from fakeredis import FakeRedis
from redis import from_url
from redis.client import Redis
from redis.exceptions import ConnectionError

from app.core.config import get_settings

MAX_ATTEMPTS = 3


class RedisClient:
    def __init__(self):
        settings = get_settings()
        self.logger = logging.getLogger("app.api")
        self.connected: bool = False
        self.failed_attempts: int = 0
        self.redis_host: str = settings.REDIS_HOST
        self.redis_host_port: int = settings.REDIS_PORT
        self.redis_db: int = settings.REDIS_DB
        self.redis_pw: str = settings.REDIS_PW
        self._client: Redis

    @property
    def redis_url(self) -> str:
        return (
            f"redis://:{self.redis_pw}@{self.redis_host}:{self.redis_host_port}/{self.redis_db}"
            if self.redis_pw
            else f"redis://{self.redis_host}:{self.redis_host_port}/{self.redis_db}"
        )

    @property
    def client(self) -> Redis:
        return self._get_redis_client() if os.environ.get("ENV", "") != "TEST" else FakeRedis()

    def get_redis_client(self) -> Redis:
        while not self.connected and self.failed_attempts < MAX_ATTEMPTS:
            try:
                self.logger.info("Attempting to connect to to Redis server...")
                client = from_url(self.redis_url)
                if client.ping():
                    self._client = client
                    self.connected = True
                    self.logger.info("Successfully connected to Redis server.")
                else:
                    self._handle_connect_attempt_failed()
            except ConnectionError:  # noqa: PERF203
                self._handle_connect_attempt_failed()
        return self._client

    def _handle_connect_attempt_failed(self):
        self.failed_attempts += 1
        if self.failed_attempts < MAX_ATTEMPTS:
            self.logger.warning(
                "Redis server did not respond to ping, will retry in 3 seconds... "
                f"(attempt {self.failed_attempts}/{MAX_ATTEMPTS})"
            )
            time.sleep(3)
        else:
            self._client = FakeRedis()
            self.connected = False
            self.logger.warning(f"Failed to connect to Redis server (attempt {self.failed_attempts}/{MAX_ATTEMPTS}).")

    def lock(self, key: str, blocking_timeout: int) -> Redis.lock:
        return self.get_redis_client().lock(key, blocking_timeout=blocking_timeout)

    def setnx(self, key: str, value: str) -> None:
        return self.get_redis_client().setnx(key, value)

    def get(self, key: str) -> str:
        return self.get_redis_client().get(key)

    def set(self, key: str, value: str) -> None:
        return self.get_redis_client().set(key, value)


redis = RedisClient()
