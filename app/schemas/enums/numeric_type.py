from enum import auto, IntEnum


class NumericType(IntEnum):

    NONE = auto()
    DECIMAL = auto()
    DIGIT = auto()
    NUMERIC = auto()

    def __str__(self):
        return self.name.replace("_", " ").title()

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
    def from_code(cls, code):
        code_map = {
            "None": cls.NONE,
            "De": cls.DECIMAL,
            "Di": cls.DIGIT,
            "Nu": cls.NUMERIC,
        }
        return code_map.get(code, cls.NONE)
