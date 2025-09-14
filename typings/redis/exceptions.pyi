"""
Global Redis exception classes.
"""

class RedisError(Exception):
    """
    Base class for all Redis-related errors.
    """

class LockError(RedisError, ValueError):
    "Errors acquiring or releasing a lock"

    # NOTE: For backwards compatibility, this class derives from ValueError.
    # This was originally chosen to behave like threading.Lock.

    def __init__(self, message: str | None = None, lock_name: str | None = None): ...

class LockNotOwnedError(LockError):
    "Error trying to extend or release a lock that is not owned (anymore)"

class ResponseError(RedisError):
    """
    An error returned by the Redis server indicating a problem with the
    command issued.
    """

class NoScriptError(ResponseError):
    """
    An error to indicate that the script does not exist in the script cache
    """
