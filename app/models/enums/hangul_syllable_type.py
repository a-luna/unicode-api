from enum import IntEnum, auto


class HangulSyllableType(IntEnum):

    NOT_APPLICABLE = auto()
    LEADING_JAMO = auto()
    VOWEL_JAMO = auto()
    TRAILING_JAMO = auto()
    LV_SYLLABLE = auto()
    LVT_SYLLABLE = auto()

    def __str__(self):
        return self.name.replace("_", " ").title()

    @property
    def display_name(self) -> str:
        return f"{self} ({self.code})"

    @property
    def code(self) -> str:
        code_map = {
            "NOT_APPLICABLE": "NA",
            "LEADING_JAMO": "L",
            "VOWEL_JAMO": "V",
            "TRAILING_JAMO": "T",
            "LV_SYLLABLE": "LV",
            "LVT_SYLLABLE": "LVT",
        }
        return code_map.get(self.name, "")

    @classmethod
    def from_code(cls, code):
        code_map = {
            "NA": cls.NOT_APPLICABLE,
            "L": cls.LEADING_JAMO,
            "V": cls.VOWEL_JAMO,
            "T": cls.TRAILING_JAMO,
            "LV": cls.LV_SYLLABLE,
            "LVT": cls.LVT_SYLLABLE,
        }
        return code_map.get(code, cls.NOT_APPLICABLE)
