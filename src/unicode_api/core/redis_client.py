"""
This module provides Redis client utilities for managing connections and operations with a Redis server,
including a production-ready client (`RedisClient`) and a mock client for testing (`TestRedisClient`).

Classes:
    IRedisClient (Protocol): Interface for Redis client implementations, specifying required methods
        and properties.

    RedisClient: Utility class for connecting to and interacting with a Redis server, with automatic
        connection retries and fallback to a fake Redis instance.

    TestRedisClient: In-memory mock implementation of a Redis client for testing purposes.

Constants:
    MAX_ATTEMPTS (int): Maximum number of connection attempts to the Redis server.

    redis (RedisClient | TestRedisClient): Singleton instance of the appropriate Redis client,
        depending on the application environment.

Usage:
    Use the `redis` instance to interact with Redis, e.g., `redis.set(key, value)`, `redis.get(key)`, etc.
    The client automatically handles connection retries and provides a fake Redis instance for testing environments.
"""

import logging
import time
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Protocol

from fakeredis import FakeRedis
from redis import from_url
from redis.client import Redis
from redis.exceptions import ConnectionError
from redis.lock import Lock

from unicode_api.config.api_settings import get_settings
from unicode_api.core.redis_types import RedisKey, RedisResponse, RedisValue
from unicode_api.core.util import dtaware_fromtimestamp

MAX_ATTEMPTS = 3


class IRedisClient(Protocol):
    @property
    def client(self) -> Redis:
        """
        Returns an active Redis client using config values generated from environment variables.
        """
        ...

    def lock(self, name: str, blocking_timeout: float | int) -> Any:
        """
        Return a new Lock object using key ``name`` that mimics
        the behavior of threading.Lock.

        ``blocking_timeout`` indicates the maximum amount of time in seconds to spend trying to acquire the lock.
         A value of ``None`` indicates continue trying forever. ``blocking_timeout`` can be specified as a float
         or integer, both representing the number of seconds to wait.
        """
        ...

    def setnx(self, name: RedisKey, value: RedisValue) -> RedisResponse:
        """
        Set the value of key ``name`` to ``value`` if key doesn't exist.
        """
        ...

    def set(self, name: RedisKey, value: RedisValue) -> RedisResponse:
        """
        Set the value at key ``name`` to ``value``
        """
        ...

    def get(self, name: RedisKey) -> RedisResponse:
        """
        Return the value at key ``name``, or None if the key doesn't exist
        """
        ...

    def time(self) -> float:
        """
        Return POSIX timestamp as a float value representing seconds since the epoch
        """
        ...

    def now(self) -> datetime:
        """
        Return the current time as a time-zone aware datetime object
        """
        ...


class RedisClient:
    """
    RedisClient is a utility class for managing Redis connections and operations.

    Attributes:
        settings (Settings): The application settings containing Redis configuration.
        logger (Logger): Logger instance for logging Redis client activities.
        connected (bool): Indicates whether the client is connected to the Redis server.
        failed_attempts (int): The number of failed connection attempts.
        _client (Redis): The Redis client instance.

    Properties:
        redis_host (str): The Redis server hostname.
        redis_host_port (int): The Redis server port.
        redis_db (int): The Redis database index.
        redis_pw (str): The Redis server password.
        redis_url (str): The Redis connection URL.
        client (Redis): The Redis client instance, connecting if not already connected.

    Methods:
        lock(name: str, blocking_timeout: float | int) -> Any:
            Creates a distributed lock with the given name and blocking timeout.

        setnx(name: RedisKey, value: RedisValue) -> RedisResponse:
            Sets a value in Redis only if the key does not already exist.

        set(name: RedisKey, value: RedisValue) -> RedisResponse:
            Sets a value in Redis for the given key.

        get(name: RedisKey) -> RedisResponse:
            Retrieves the value associated with the given key from Redis.

        time() -> float:
            Retrieves the current server time from Redis as a floating-point timestamp.

        now() -> datetime:
            Retrieves the current server time from Redis as a timezone-aware datetime object.
    """

    def __init__(self):
        """
        Initialize a Redis client instance.

        This constructor sets up the necessary configurations for connecting to a Redis server.
        It initializes the settings, logger, connection status, and failed connection attempts.

        Attributes:
            settings: Application settings retrieved from the configuration.
            logger: Logger instance for logging Redis client-related messages.
            connected (bool): Indicates whether the client is connected to the Redis server.
            failed_attempts (int): Tracks the number of failed connection attempts.
            _client (Redis): The Redis client instance (uninitialized at this stage).
        """
        self.settings = get_settings()
        self.logger = logging.getLogger("unicode_api.api")
        self.connected: bool = False
        self.failed_attempts: int = 0
        self._client: Redis

    @property
    def redis_host(self) -> str:
        """
        Retrieve the Redis host address from the application settings.

        Returns:
            str: The Redis host address as a string.
        """
        return self.settings.REDIS_HOST

    @property
    def redis_host_port(self) -> int:
        """
        Retrieve the port number for the Redis server from the application settings.

        Returns:
            int: The port number used to connect to the Redis server.
        """
        return self.settings.REDIS_PORT

    @property
    def redis_db(self) -> int:
        """
        Retrieve the Redis database index from the application settings.

        Returns:
            int: The Redis database index as specified in the settings.
        """
        return self.settings.REDIS_DB

    @property
    def redis_pw(self) -> str:
        """
        Retrieves the Redis password from the application settings.

        Returns:
            str: The Redis password if set in the settings; otherwise, an empty string.
        """
        return self.settings.REDIS_PW or ""

    @property
    def redis_url(self) -> str:
        """
        Constructs the Redis connection URL based on the provided credentials and configuration.

        Returns:
            str: The Redis connection URL. If a password is provided, it includes the password
            in the URL; otherwise, it omits the password.
        """
        return (
            f"redis://:{self.redis_pw}@{self.redis_host}:{self.redis_host_port}/{self.redis_db}"
            if self.redis_pw
            else f"redis://{self.redis_host}:{self.redis_host_port}/{self.redis_db}"
        )

    @property
    def client(self) -> Redis:
        """
        Establishes a connection to the Redis server and returns the Redis client instance.

        This method uses the `redis_url` property, which is constructed from the application
        settings, to attempt a connection to the Redis server. It will retry the connection
        until either a successful connection is made or the maximum number of allowed attempts
        (`MAX_ATTEMPTS`) is reached.

        Returns:
            Redis: An instance of the Redis client if the connection is successful.

        Raises:
            ConnectionError: If the connection fails after the maximum number of attempts.
        """
        while not self.connected and self.failed_attempts < MAX_ATTEMPTS:
            try:
                self.logger.info("Attempting to connect to Redis server...")
                client = from_url(self.redis_url)
                if client and client.ping():
                    self._client = client
                    self.connected = True
                    self.logger.info("Successfully connected to Redis server.")
                else:
                    self._handle_connect_attempt_failed()
            except ConnectionError:
                self._handle_connect_attempt_failed()
        return self._client

    def _handle_connect_attempt_failed(self) -> None:
        self.failed_attempts += 1
        if self.failed_attempts < MAX_ATTEMPTS:
            self.logger.info(
                "Redis server did not respond to ping, will retry in 3 seconds... "
                f"(attempt {self.failed_attempts}/{MAX_ATTEMPTS})"
            )
            time.sleep(3)
        else:
            self._client = FakeRedis()
            self.connected = False
            self.logger.warning(f"Failed to connect to Redis server (attempt {self.failed_attempts}/{MAX_ATTEMPTS}).")

    def lock(self, name: str, blocking_timeout: float | int) -> Lock:
        """
        Acquire a distributed lock using the Redis client.

        Args:
            name (str): The name of the lock.
            blocking_timeout (float | int): The maximum time in seconds to block
                while waiting to acquire the lock. If 0, the method will not block.

        Returns:
            Any: A lock object if the lock is successfully acquired, or None if
            the lock could not be acquired within the specified timeout.
        """
        return self.client.lock(name, blocking_timeout=blocking_timeout)

    def setnx(self, name: RedisKey, value: RedisValue) -> RedisResponse:
        """
        Set the value of a key only if the key does not already exist.

        Args:
            name (RedisKey): The key to set in the Redis database.
            value (RedisValue): The value to associate with the key.

        Returns:
            RedisResponse: A response indicating whether the key was set.
                           Returns True if the key was set, False if it already exists.
        """
        return self.client.setnx(name, value)

    def set(self, name: RedisKey, value: RedisValue) -> RedisResponse:
        """
        Set a value in the Redis database for the given key.

        Args:
            name (RedisKey): The key under which the value will be stored.
            value (RedisValue): The value to store in the Redis database.

        Returns:
            RedisResponse: The response from the Redis server, typically indicating
            whether the operation was successful.
        """
        return self.client.set(name, value)

    def get(self, name: RedisKey) -> RedisResponse:
        """
                Retrieve the value associated with the given Redis key.
        //
                Args:
                    name (RedisKey): The key whose value needs to be retrieved.

                Returns:
                    RedisResponse: The value associated with the key, or None if the key does not exist.
        """
        return self.client.get(name)

    def time(self) -> float:
        """
        Retrieve the current time from the Redis server or fallback to the local system time.

        Returns:
            float: The current time as a Unix timestamp. If the Redis server provides
            a valid response, the timestamp is constructed from the seconds and
            microseconds returned by the server. Otherwise, the local system time
            is used as a fallback.
        """
        response = self.client.time()
        if len(response) == 2:
            (seconds, microseconds) = response
            return float(f"{seconds}.{microseconds}")
        return datetime.now().timestamp()

    def now(self) -> datetime:
        """
        Get the current datetime as an aware datetime object.

        Returns:
            datetime: The current datetime with timezone awareness.
        """
        return dtaware_fromtimestamp(self.time())


class TestRedisClient:
    """
    TestRedisClient is a mock implementation of a Redis client for testing purposes.

    Attributes:
        db (dict): An in-memory dictionary used to simulate Redis key-value storage.

    Methods:
        client:
            A property that returns a fake Redis client instance.

        lock(name: str, blocking_timeout: float | int) -> Any:
            Simulates acquiring a lock in Redis. Returns a context manager that does nothing.

        setnx(name: RedisKey, value: RedisValue) -> RedisResponse:
            Sets a value in the database only if the key does not already exist.

        set(name: RedisKey, value: RedisValue) -> RedisResponse:
            Sets a value in the database for the given key.

        get(name: RedisKey) -> RedisResponse:
            Retrieves the value associated with the given key from the database.

        time() -> float:
            Returns the current timestamp as a float.

        now() -> datetime:
            Returns the current datetime as an aware datetime object.
    """

    def __init__(self) -> None:
        self.db: dict[RedisKey, RedisValue] = {}

    @property
    def client(self) -> Redis:
        return FakeRedis()

    def lock(self, name: str, blocking_timeout: float | int) -> Any:
        @contextmanager
        def fake_lock_context():
            yield None

        return fake_lock_context()

    def setnx(self, name: RedisKey, value: RedisValue) -> RedisResponse:
        if name not in self.db:
            self.set(name, value)

    def set(self, name: RedisKey, value: RedisValue) -> RedisResponse:
        self.db[name] = value

    def get(self, name: RedisKey) -> RedisResponse:
        return self.db.get(name, None)

    def time(self) -> float:
        return datetime.now().timestamp()

    def now(self) -> datetime:
        return dtaware_fromtimestamp(self.time())


redis = RedisClient() if not get_settings().is_test else TestRedisClient()
