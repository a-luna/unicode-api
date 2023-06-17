from enum import IntEnum, auto


class VerticalOrientationType(IntEnum):
    NONE = 0
    UPRIGHT = auto()
    ROTATED = auto()
    TRANSFORMED_UPRIGHT = auto()
    TRANSFORMED_ROTATED = auto()

    def __str__(self):
        name_map = {
            "UPRIGHT": "Upright",
            "ROTATED": "Rotated 90 degrees clockwise",
            "TRANSFORMED_UPRIGHT": "Transformed typographically, with fallback to Upright",
            "TRANSFORMED_ROTATED": "Transformed typographically, with fallback to Rotated",
        }
        return name_map.get(self.name, "None")

    @property
    def display_name(self) -> str:
        return f"{self} ({self.code})"

    @property
    def code(self) -> str:
        code_map = {
            "UPRIGHT": "U",
            "ROTATED": "R",
            "TRANSFORMED_UPRIGHT": "Tu",
            "TRANSFORMED_ROTATED": "Tr",
        }
        return code_map.get(self.name, "None")

    @classmethod
    def from_code(cls, code):  # pragma: no cover
        code_map = {
            "U": cls.UPRIGHT,
            "R": cls.ROTATED,
            "Tu": cls.TRANSFORMED_UPRIGHT,
            "Tr": cls.TRANSFORMED_ROTATED,
        }
        return code_map.get(code, cls.NONE)
