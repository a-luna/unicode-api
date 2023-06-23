from enum import IntEnum, auto


class EastAsianWidthType(IntEnum):
    EAST_ASIAN_AMBIGUOUS = auto()
    EAST_ASIAN_FULLWIDTH = auto()
    EAST_ASIAN_HALFWIDTH = auto()
    NEUTRAL_NOT_EAST_ASIAN = auto()
    EAST_ASIAN_NARROW = auto()
    EAST_ASIAN_WIDE = auto()

    def __str__(self):
        return self.name.replace("_", " ").title()

    @property
    def display_name(self) -> str:
        return f"{self} ({self.code})"

    @property
    def code(self) -> str:
        code_map = {
            "EAST_ASIAN_AMBIGUOUS": "A",
            "EAST_ASIAN_FULLWIDTH": "F",
            "EAST_ASIAN_HALFWIDTH": "H",
            "NEUTRAL_NOT_EAST_ASIAN": "N",
            "EAST_ASIAN_NARROW": "Na",
            "EAST_ASIAN_WIDE": "W",
        }
        return code_map.get(self.name, "")

    @classmethod
    def from_code(cls, code):  # pragma: no cover
        code_map = {
            "A": cls.EAST_ASIAN_AMBIGUOUS,
            "F": cls.EAST_ASIAN_FULLWIDTH,
            "H": cls.EAST_ASIAN_HALFWIDTH,
            "N": cls.NEUTRAL_NOT_EAST_ASIAN,
            "Na": cls.EAST_ASIAN_NARROW,
            "W": cls.EAST_ASIAN_WIDE,
        }
        return code_map.get(code, cls.NEUTRAL_NOT_EAST_ASIAN)
