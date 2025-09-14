from collections.abc import Awaitable
from typing import Any, Protocol

Number = int | float
EncodedT = bytes | bytearray | memoryview
DecodedT = str | int | float
EncodableT = EncodedT | DecodedT
_StringLikeT = bytes | str | memoryview
KeyT = _StringLikeT  # Main redis key space
ResponseT = Awaitable[Any] | Any
ScriptTextT = _StringLikeT

class CommandsProtocol(Protocol):
    def execute_command(self, *args, **options) -> ResponseT: ...
