from enum import IntEnum, auto

from app.schemas.util import normalize_string_lm3


class NumericType(IntEnum):
    NONE = auto()
    DECIMAL = auto()
    DIGIT = auto()
    NUMERIC = auto()

    def __str__(self):
        return self.name.replace("_", " ").title()

    @property
    def normalized(self) -> str:
        return normalize_string_lm3(self.code)

    @property
    def display_name(self) -> str:
        return f"{self} ({self.code})"

    @property
    def code(self) -> str:
        code_map = {
            "NONE": "None",
            "DECIMAL": "De",
            "DIGIT": "Di",
            "NUMERIC": "Nu",
        }
        return code_map.get(self.name, "")

    @classmethod
    def from_code(cls, code):  # pragma: no cover
        code_map = {
            "None": cls.NONE,
            "De": cls.DECIMAL,
            "Di": cls.DIGIT,
            "Nu": cls.NUMERIC,
        }
        return code_map.get(code, cls.NONE)

    @classmethod
    def match_loosely(cls, name: str):
        numeric_types_map = {e.normalized: e for e in cls}
        return numeric_types_map.get(normalize_string_lm3(name))
