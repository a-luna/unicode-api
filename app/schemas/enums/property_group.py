from __future__ import annotations

from enum import IntEnum, auto

from app.schemas.util import normalize_string_lm3


class CharPropertyGroup(IntEnum):
    NONE = 0
    All = auto()
    Minimum = auto()
    Basic = auto()
    UTF8 = auto()
    UTF16 = auto()
    UTF32 = auto()
    Bidirectionality = auto()
    Decomposition = auto()
    Quick_Check = auto()
    Numeric = auto()
    Joining = auto()
    Linebreak = auto()
    East_Asian_Width = auto()
    Case = auto()
    Script = auto()
    Hangul = auto()
    Indic = auto()
    Function_and_Graphic = auto()
    Emoji = auto()

    @property
    def index_name(self) -> str:  # pragma: no cover
        if "_" in self.name:
            return "".join([s[0] for s in self.name.split("_") if s.upper() != "AND"]).lower()
        return self.name.lower()

    @property
    def normalized(self) -> str:
        return normalize_string_lm3(self.name)

    @property
    def short_alias(self) -> str:
        prop_aliases = {
            "Bidirectionality": "bidi",
            "Decomposition": "decomp",
            "Quick_Check": "qc",
            "Numeric": "num",
            "Linebreak": "lb",
            "East_Asian_Width": "eaw",
            "Function_and_Graphic": "function",
        }
        return prop_aliases.get(self.name, self.normalized)

    @property
    def has_alias(self) -> bool:
        return self.normalized != self.short_alias

    @classmethod
    def match_loosely(cls, name: str) -> CharPropertyGroup:
        prop_names = {e.normalized: e for e in cls}
        prop_aliases = {e.short_alias: e for e in cls}
        prop_names.update(prop_aliases)
        return prop_names.get(normalize_string_lm3(name), cls.NONE)
