from typing import Any

from .commands.core import ManagementCommands
from .redis import Lock

class Redis:
    """
    Implementation of the Redis protocol.

    This abstract class provides a Python interface to all Redis commands
    and an implementation of the Redis protocol.

    Pipelines derive from this, implementing how
    the commands are sent and received to the Redis server. Based on
    configuration, an instance will either use a ConnectionPool, or
    Connection object to talk to redis.

    It is not safe to pass PubSub or Pipeline objects between threads.
    """

    @classmethod
    def from_url(cls, url: str) -> Redis:
        """
        Return a Redis client object configured from the given URL

        For example::

            redis://[[username]:[password]]@localhost:6379/0
            rediss://[[username]:[password]]@localhost:6379/0
            unix://[username@]/path/to/socket.sock?db=0[&password=password]

        Three URL schemes are supported:

        - `redis://` creates a TCP socket connection. See more at:
          <https://www.iana.org/assignments/uri-schemes/prov/redis>
        - `rediss://` creates a SSL wrapped TCP socket connection. See more at:
          <https://www.iana.org/assignments/uri-schemes/prov/rediss>
        - ``unix://``: creates a Unix Domain Socket connection.

        The username, password, hostname, path and all querystring values
        are passed through urllib.parse.unquote in order to replace any
        percent-encoded values with their corresponding characters.

        There are several ways to specify a database number. The first value
        found will be used:

            1. A ``db`` querystring option, e.g. redis://localhost?db=0
            2. If using the redis:// or rediss:// schemes, the path argument
               of the url, e.g. redis://localhost/0
            3. A ``db`` keyword argument to this function.

        If none of these options are specified, the default db=0 is used.

        All querystring options are cast to their appropriate Python types.
        Boolean arguments can be specified with string values "True"/"False"
        or "Yes"/"No". Values that cannot be properly cast cause a
        ``ValueError`` to be raised. Once parsed, the querystring arguments
        and keyword arguments are passed to the ``ConnectionPool``'s
        class initializer. In the case of conflicting arguments, querystring
        arguments always win.

        """

    def ping(self, message: str = "PONG") -> str:
        """
        Ping the Redis server

        The server will respond with a PONG response. This can be used to
        test if a connection is still alive.

        An optional message argument can be provided, in which case the
        server will respond with that message instead of PONG.

        Return value:

        The response from the server, usually "PONG" or the message
        argument if provided.
        """

    def lock(
        self,
        name: str,
        timeout: float | None = None,
        sleep: float = 0.1,
        blocking: bool = True,
        blocking_timeout: float | None = None,
        lock_class: None | Any = None,
        thread_local: bool = True,
        raise_on_release_error: bool = True,
    ) -> Lock:
        """
        Return a new Lock object using key ``name`` that mimics
        the behavior of threading.Lock.

        If specified, ``timeout`` indicates a maximum life for the lock.
        By default, it will remain locked until release() is called.

        ``sleep`` indicates the amount of time to sleep per loop iteration
        when the lock is in blocking mode and another client is currently
        holding the lock.

        ``blocking`` indicates whether calling ``acquire`` should block until
        the lock has been acquired or to fail immediately, causing ``acquire``
        to return False and the lock not being acquired. Defaults to True.
        Note this value can be overridden by passing a ``blocking``
        argument to ``acquire``.

        ``blocking_timeout`` indicates the maximum amount of time in seconds to
        spend trying to acquire the lock. A value of ``None`` indicates
        continue trying forever. ``blocking_timeout`` can be specified as a
        float or integer, both representing the number of seconds to wait.

        ``lock_class`` forces the specified lock implementation. Note that as
        of redis-py 3.0, the only lock class we implement is ``Lock`` (which is
        a Lua-based lock). So, it's unlikely you'll need this parameter, unless
        you have created your own custom lock class.

        ``thread_local`` indicates whether the lock token is placed in
        thread-local storage. By default, the token is placed in thread local
        storage so that a thread only sees its token, not a token set by
        another thread. Consider the following timeline:

            time: 0, thread-1 acquires `my-lock`, with a timeout of 5 seconds.
                     thread-1 sets the token to "abc"
            time: 1, thread-2 blocks trying to acquire `my-lock` using the
                     Lock instance.
            time: 5, thread-1 has not yet completed. redis expires the lock
                     key.
            time: 5, thread-2 acquired `my-lock` now that it's available.
                     thread-2 sets the token to "xyz"
            time: 6, thread-1 finishes its work and calls release(). if the
                     token is *not* stored in thread local storage, then
                     thread-1 would see the token value as "xyz" and would be
                     able to successfully release the thread-2's lock.

        ``raise_on_release_error`` indicates whether to raise an exception when
        the lock is no longer owned when exiting the context manager. By default,
        this is True, meaning an exception will be raised. If False, the warning
        will be logged and the exception will be suppressed.

        In some use cases it's necessary to disable thread local storage. For
        example, if you have code where one thread acquires a lock and passes
        that lock instance to a worker thread to release later. If thread
        local storage isn't disabled in this case, the worker thread won't see
        the token set by the thread that acquired the lock. Our assumption
        is that these cases aren't common and as such default to using
        thread local storage.
        """

    def set(self, name: bytes | str | memoryview, value: Any, ex: int | None = None, px: int | None = None) -> bool:
        """
        Set the value of key ``name`` to ``value``.

        The ``ex`` and ``px`` arguments set an expire flag on the key. ``ex``
        sets the expire time in seconds, while ``px`` sets it in milliseconds.
        Only one of these arguments should be used.

        Return value:

        True if the command was successful.
        """

    def setnx(self, name: bytes | str | memoryview, value: Any, ex: int | None = None, px: int | None = None) -> bool:
        """
        Set the value of key ``name`` to ``value`` if it does not already exist.

        If the key already exists, no operation is performed.

        The ``ex`` and ``px`` arguments set an expire flag on the key. ``ex``
        sets the expire time in seconds, while ``px`` sets it in milliseconds.
        Only one of these arguments should be used.

        Return value:

        True if the key was set, False if it was not set.
        """

    def get(self, name: bytes | str | memoryview) -> Any:
        """
        Return the value at key ``name``, or None if the key doesn't exist.

        Return value:

        The value at key ``name``, or None if the key doesn't exist.
        """

    def time(self) -> tuple[int, int]:
        """
        Return the current server time.

        Return value:

        A tuple of two integers: (seconds, microseconds).
        """
