from enum import IntEnum, auto


class BidirectionalBracketType(IntEnum):
    NONE = 0
    OPEN = auto()
    CLOSE = auto()

    def __str__(self):
        return self.name.replace("_", " ").title()

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
    def from_code(cls, code):  # pragma: no cover
        code_map = {
            "n": cls.NONE,
            "o": cls.OPEN,
            "c": cls.CLOSE,
        }
        return code_map.get(code, cls.NONE)
