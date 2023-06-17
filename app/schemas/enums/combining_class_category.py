from __future__ import annotations

from enum import IntEnum


class CombiningClassCategory(IntEnum):
    NOT_REORDERED = 0
    OVERLAY = 1
    HAN_READING = 6
    NUKTA = 7
    KANA_VOICING = 8
    VIRAMA = 9
    CCC10 = 10  # Hebrew start
    CCC11 = 11
    CCC12 = 12
    CCC13 = 13
    CCC14 = 14
    CCC15 = 15
    CCC16 = 16
    CCC17 = 17
    CCC18 = 18
    CCC19 = 19
    CCC20 = 20
    CCC21 = 21
    CCC22 = 22
    CCC23 = 23
    CCC24 = 24
    CCC25 = 25
    CCC26 = 26  # Hebrew end
    CCC27 = 27  # Arabic start
    CCC28 = 28
    CCC29 = 29
    CCC30 = 30
    CCC31 = 31
    CCC32 = 32
    CCC33 = 33
    CCC34 = 34
    CCC35 = 35  # Arabic end
    CCC36 = 36  # Syriac
    CCC84 = 84  # Telegu start
    CCC91 = 91  # Telegu end
    CCC103 = 103  # Thai start
    CCC107 = 107  # Thai end
    CCC118 = 118  # Lao start
    CCC122 = 122  # Lao end
    CCC129 = 129  # Tibetan start
    CCC130 = 130
    CCC132 = 132
    CCC133 = 133  # Tibetan end
    ATTACHED_BELOW_LEFT = 200
    ATTACHED_BELOW = 202
    ATTACHED_BELOW_RIGHT = 204
    ATTACHED_LEFT = 208
    ATTACHED_RIGHT = 210
    ATTACHED_ABOVE_LEFT = 212
    ATTACHED_ABOVE = 214
    ATTACHED_ABOVE_RIGHT = 216
    BELOW_LEFT = 218
    BELOW = 220
    BELOW_RIGHT = 222
    LEFT = 224
    RIGHT = 226
    ABOVE_LEFT = 228
    ABOVE = 230
    ABOVE_RIGHT = 232
    DOUBLE_BELOW = 233
    DOUBLE_ABOVE = 234
    IOTA_SUBSCRIPT = 240

    def __str__(self):
        return self.name.replace("_", " ").title() if not self.name.startswith("CCC") else self.name

    @property
    def display_name(self) -> str:
        return f"{self} ({self.code})"

    @property
    def code(self) -> str:
        return f"{int(self)}"

    @classmethod
    def match_loosely(cls, code: str) -> CombiningClassCategory:
        ccc_map = {e.code: e for e in cls}
        return ccc_map.get(code, cls.NOT_REORDERED)
