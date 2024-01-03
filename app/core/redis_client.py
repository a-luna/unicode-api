import logging
import os
import time
from datetime import datetime
from typing import Protocol

from fakeredis import FakeRedis
from redis import from_url
from redis.client import Redis
from redis.exceptions import ConnectionError

from app.config import get_settings
from app.core.util import dtaware_fromtimestamp

MAX_ATTEMPTS = 3


class IRedisClient(Protocol):
    @property
    def client(self) -> Redis:
        ...

    def lock(self, name: str, blocking_timeout: int) -> Redis.lock:
        """
        Return a new Lock object using key ``name`` that mimics
        the behavior of threading.Lock.

        ``blocking_timeout`` indicates the maximum amount of time in seconds to spend trying to acquire the lock.
         A value of ``None`` indicates continue trying forever. ``blocking_timeout`` can be specified as a float
         or integer, both representing the number of seconds to wait.
        """
        ...

    def setnx(self, name: str, value: str) -> None:
        """
        Set the value of key ``name`` to ``value`` if key doesn't exist.
        """
        ...

    def set(self, name: str, value: str) -> None:
        """
        Set the value at key ``name`` to ``value``
        """
        ...

    def get(self, name: str) -> str:
        """
        Return the value at key ``name``, or None if the key doesn't exist
        """
        ...

    def time(self) -> float:
        """
        Returns the server time as a 2-item tuple of ints:
        (seconds since epoch, microseconds into this second).
        """
        ...

    def now(self) -> datetime:
        ...


class RedisClient:
    def __init__(self):
        self.settings = get_settings()
        self.logger = logging.getLogger("app.api")
        self.connected: bool = False
        self.failed_attempts: int = 0
        self.redis_host: str = self.settings.REDIS_HOST
        self.redis_host_port: int = self.settings.REDIS_PORT
        self.redis_db: int = self.settings.REDIS_DB
        self.redis_pw: str = self.settings.REDIS_PW
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
        if self.settings.is_test:
            return FakeRedis()
        while not self.connected and self.failed_attempts < MAX_ATTEMPTS:
            try:
                self.logger.info("Attempting to connect to to Redis server...")
                client = from_url(self.redis_url)
                if client.ping():
                    self._client = client
                    self.connected = True
                    self.logger.info("Successfully connected to Redis server.")
                else:
                    self.handle_connect_attempt_failed()
            except ConnectionError:  # noqa: PERF203
                self.handle_connect_attempt_failed()
        return self._client

    def handle_connect_attempt_failed(self):
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

    def lock(self, name: str, blocking_timeout: int) -> Redis.lock:
        return self.client.lock(name, blocking_timeout=blocking_timeout)

    def setnx(self, name: str, value: str) -> None:
        return self.client.setnx(name, value)

    def set(self, name: str, value: str) -> None:
        return self.client.set(name, value)

    def get(self, name: str) -> str:
        return self.client.get(name)

    def time(self) -> float:
        (seconds, microseconds) = self.client.time()
        return float(f"{seconds}.{microseconds}")

    def now(self) -> datetime:
        return dtaware_fromtimestamp(self.time())


class TestRedisClient:
    def __init__(self) -> None:
        self.db = {}

    @property
    def client(self) -> Redis:
        return FakeRedis()

    def lock(self, name: str, blocking_timeout: int) -> Redis.lock:
        return self.client.lock(name, blocking_timeout=blocking_timeout)

    def setnx(self, name: str, value: str) -> None:
        if name not in self.db:
            self.db[name] = value

    def set(self, name: str, value: str) -> None:
        self.db[name] = value

    def get(self, name: str) -> str:
        return self.db.get(name, None)

    def time(self) -> float:
        return datetime.now().timestamp()

    def now(self) -> datetime:
        return dtaware_fromtimestamp(self.time())


redis = RedisClient() if "TEST" not in os.environ.get("ENV", "DEV") else TestRedisClient()
