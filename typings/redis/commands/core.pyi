from collections.abc import Awaitable, Iterable, Sequence

from .._parsers import Encoder
from ..redis import Redis
from ..typing import CommandsProtocol, EncodableT, KeyT, ScriptTextT

class ManagementCommands:
    def ping(self, message: str | None = None) -> bool:
        """
        Ping the Redis server

        For more information see https://redis.io/commands/ping
        """

    def time(self) -> tuple[int, int]:
        """
        Returns the server time as a 2-item tuple of ints:
        (seconds since epoch, microseconds into this second).

        For more information see https://redis.io/commands/time
        """

class ScriptCommands(CommandsProtocol):
    def evalsha(self, sha: str, numkeys: int, *keys_and_args: str) -> Awaitable[str] | str:
        """
        Use the ``sha`` to execute a Lua script already registered via EVAL
        or SCRIPT LOAD. Specify the ``numkeys`` the script will touch and the
        key names and argument values in ``keys_and_args``. Returns the result
        of the script.

        In practice, use the object returned by ``register_script``. This
        function exists purely for Redis API completion.

        For more information see  https://redis.io/commands/evalsha
        """

class Script:
    """
    An executable Lua script object returned by ``register_script``
    """

    def __init__(self, registered_client: Redis, script: ScriptTextT): ...
    def __call__(
        self,
        keys: Sequence[KeyT] | None = None,
        args: Iterable[EncodableT] | None = None,
        client: Redis | None = None,
    ) -> Awaitable[str] | str:
        """Execute the script, passing any required ``args``"""

    def get_encoder(self) -> Encoder:
        """Get the encoder to encode string scripts into bytes."""
