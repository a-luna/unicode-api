from collections.abc import Awaitable
from typing import Any

RedisKey = bytes | str | memoryview
RedisValue = bytes | str | memoryview | int | float
RedisResponse = Awaitable[Any] | Any
