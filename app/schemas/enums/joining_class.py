from enum import auto, IntEnum


class JoiningClass(IntEnum):

    NONE = auto()
    RIGHT_JOINING = auto()
    LEFT_JOINING = auto()
    DUAL_JOINING = auto()
    JOIN_CAUSING = auto()
    NON_JOINING = auto()
    TRANSPARENT = auto()

    def __str__(self):
        return self.name.replace("_", " ").title()

    @property
    def display_name(self) -> str:
        return f"{self} ({self.code})"

    @property
    def code(self) -> str:
        code_map = {
            "RIGHT_JOINING": "R",
            "LEFT_JOINING": "L",
            "DUAL_JOINING": "D",
            "JOIN_CAUSING": "C",
            "NON_JOINING": "U",
            "TRANSPARENT": "T",
        }
        return code_map.get(self.name, "")

    @classmethod
    def from_code(cls, code):
        code_map = {
            "R": cls.RIGHT_JOINING,
            "L": cls.LEFT_JOINING,
            "D": cls.DUAL_JOINING,
            "C": cls.JOIN_CAUSING,
            "U": cls.NON_JOINING,
            "T": cls.TRANSPARENT,
        }
        return code_map.get(code, cls.NONE)
