from enum import IntEnum, auto
from typing import Self

from app.schemas.util import normalize_string_lm3


class BidirectionalBracketType(IntEnum):
    NONE = 0
    OPEN = auto()
    CLOSE = auto()

    def __str__(self) -> str:
        return self.name.title()

    @property
    def display_name(self) -> str:
        return f"{self} ({self.code})"

    @property
    def code(self) -> str:
        code_map = {
            "NONE": "n",
            "OPEN": "o",
            "CLOSE": "c",
        }
        return code_map.get(self.name, "")

    @classmethod
    def from_code(cls, code: str) -> Self:  # pragma: no cover
        code_map = {
            "n": cls.NONE,
            "o": cls.OPEN,
            "c": cls.CLOSE,
        }
        return code_map.get(code, cls.NONE)

    @classmethod
    def match_loosely(cls, value: str) -> Self:
        code_map = {e.code: e for e in cls}
        return code_map.get(normalize_string_lm3(value), cls.NONE)
