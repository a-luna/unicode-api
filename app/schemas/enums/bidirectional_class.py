from __future__ import annotations

from enum import IntEnum, auto

from app.schemas.util import normalize_string_lm3


class BidirectionalClass(IntEnum):
    NONE = 0
    LEFT_TO_RIGHT = auto()
    RIGHT_TO_LEFT = auto()
    ARABIC_LETTER = auto()
    EUROPEAN_NUMBER = auto()
    EUROPEAN_SEPARATOR = auto()
    EUROPEAN_TERMINATOR = auto()
    ARABIC_NUMBER = auto()
    COMMON_SEPARATOR = auto()
    NONSPACING_MARK = auto()
    BOUNDARY_NEUTRAL = auto()
    PARAGRAPH_SEPARATOR = auto()
    SEGMENT_SEPARATOR = auto()
    WHITE_SPACE = auto()
    OTHER_NEUTRAL = auto()
    LEFT_TO_RIGHT_EMBEDDING = auto()
    LEFT_TO_RIGHT_OVERRIDE = auto()
    RIGHT_TO_LEFT_EMBEDDING = auto()
    RIGHT_TO_LEFT_OVERRIDE = auto()
    POP_DIRECTIONAL_FORMAT = auto()
    LEFT_TO_RIGHT_ISOLATE = auto()
    RIGHT_TO_LEFT_ISOLATE = auto()
    FIRST_STRONG_ISOLATE = auto()
    POP_DIRECTIONAL_ISOLATE = auto()

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
            "LEFT_TO_RIGHT": "L",
            "RIGHT_TO_LEFT": "R",
            "ARABIC_LETTER": "AL",
            "EUROPEAN_NUMBER": "EN",
            "EUROPEAN_SEPARATOR": "ES",
            "EUROPEAN_TERMINATOR": "ET",
            "ARABIC_NUMBER": "AN",
            "COMMON_SEPARATOR": "CS",
            "NONSPACING_MARK": "NSM",
            "BOUNDARY_NEUTRAL": "BN",
            "PARAGRAPH_SEPARATOR": "B",
            "SEGMENT_SEPARATOR": "S",
            "WHITE_SPACE": "WS",
            "OTHER_NEUTRAL": "ON",
            "LEFT_TO_RIGHT_EMBEDDING": "LRE",
            "LEFT_TO_RIGHT_OVERRIDE": "LRO",
            "RIGHT_TO_LEFT_EMBEDDING": "RLE",
            "RIGHT_TO_LEFT_OVERRIDE": "RLO",
            "POP_DIRECTIONAL_FORMAT": "PDF",
            "LEFT_TO_RIGHT_ISOLATE": "LRI",
            "RIGHT_TO_LEFT_ISOLATE": "RLI",
            "FIRST_STRONG_ISOLATE": "FSI",
            "POP_DIRECTIONAL_ISOLATE": "PDI",
        }
        return code_map.get(self.name, "")

    @classmethod
    def from_code(cls, code):  # pragma: no cover
        code_map = {
            "L": cls.LEFT_TO_RIGHT,
            "R": cls.RIGHT_TO_LEFT,
            "AL": cls.ARABIC_LETTER,
            "EN": cls.EUROPEAN_NUMBER,
            "ES": cls.EUROPEAN_SEPARATOR,
            "ET": cls.EUROPEAN_TERMINATOR,
            "AN": cls.ARABIC_NUMBER,
            "CS": cls.COMMON_SEPARATOR,
            "NSM": cls.NONSPACING_MARK,
            "BN": cls.BOUNDARY_NEUTRAL,
            "B": cls.PARAGRAPH_SEPARATOR,
            "S": cls.SEGMENT_SEPARATOR,
            "WS": cls.WHITE_SPACE,
            "ON": cls.OTHER_NEUTRAL,
            "LRE": cls.LEFT_TO_RIGHT_EMBEDDING,
            "LRO": cls.LEFT_TO_RIGHT_OVERRIDE,
            "RLE": cls.RIGHT_TO_LEFT_EMBEDDING,
            "RLO": cls.RIGHT_TO_LEFT_OVERRIDE,
            "PDF": cls.POP_DIRECTIONAL_FORMAT,
            "LRI": cls.LEFT_TO_RIGHT_ISOLATE,
            "RLI": cls.RIGHT_TO_LEFT_ISOLATE,
            "FSI": cls.FIRST_STRONG_ISOLATE,
            "PDI": cls.POP_DIRECTIONAL_ISOLATE,
        }
        return code_map.get(code, cls.NONE)

    @classmethod
    def match_loosely(cls, name: str) -> BidirectionalClass:
        bidi_class_map = {e.normalized: e for e in cls}
        return bidi_class_map.get(normalize_string_lm3(name), cls.NONE)
