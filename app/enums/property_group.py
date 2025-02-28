from enum import IntEnum, auto

from app.models.util import normalize_string_lm3


class CharPropertyGroup(IntEnum):
    NONE = 0
    ALL = auto()
    MINIMUM = auto()
    BASIC = auto()
    UTF8 = auto()
    UTF16 = auto()
    UTF32 = auto()
    BIDIRECTIONALITY = auto()
    DECOMPOSITION = auto()
    QUICK_CHECK = auto()
    NUMERIC = auto()
    JOINING = auto()
    LINEBREAK = auto()
    EAST_ASIAN_WIDTH = auto()
    CASE = auto()
    SCRIPT = auto()
    HANGUL = auto()
    INDIC = auto()
    CJK_MINIMUM = auto()
    CJK_BASIC = auto()
    CJK_VARIANTS = auto()
    CJK_NUMERIC = auto()
    CJK_READINGS = auto()
    FUNCTION_AND_GRAPHIC = auto()
    EMOJI = auto()

    def __str__(self) -> str:
        match self:
            case CharPropertyGroup.UTF8:
                return "UTF-8"
            case CharPropertyGroup.UTF16:
                return "UTF-16"
            case CharPropertyGroup.UTF32:
                return "UTF-32"
            case _:
                return self.name.replace("_", " ").title().replace("Cjk", "CJK").replace("And", "and")

    @property
    def index_name(self) -> str:  # pragma: no cover
        match self:
            case CharPropertyGroup.CJK_MINIMUM:
                return "cjk_m"
            case CharPropertyGroup.CJK_BASIC:
                return "cjk_b"
            case CharPropertyGroup.CJK_VARIANTS:
                return "cjk_v"
            case CharPropertyGroup.CJK_NUMERIC:
                return "cjk_n"
            case CharPropertyGroup.CJK_READINGS:
                return "cjk_r"
            case _:
                return (
                    "".join([s[0] for s in self.name.split("_") if s.upper() != "AND"]).lower()
                    if "_" in self.name
                    else self.name.lower()
                )

    @property
    def normalized(self) -> str:
        return normalize_string_lm3(self.name)

    @property
    def short_alias(self) -> str:
        prop_aliases = {
            "BIDIRECTIONALITY": "bidi",
            "DECOMPOSITION": "decomp",
            "QUICK_CHECK": "qc",
            "NUMERIC": "num",
            "JOINING": "join",
            "LINEBREAK": "lb",
            "EAST_ASIAN_WIDTH": "eaw",
            "FUNCTION_AND_GRAPHIC": "function",
            "CJK_MINIMUM": "cjk_m",
            "CJK_BASIC": "cjk_b",
            "CJK_VARIANTS": "cjk_v",
            "CJK_NUMERIC": "cjk_n",
            "CJK_READINGS": "cjk_r",
        }
        return prop_aliases.get(self.name, self.normalized)

    @property
    def has_alias(self) -> bool:
        return self.normalized != self.short_alias

    @classmethod
    def get_all_non_unihan_character_prop_groups(cls) -> list["CharPropertyGroup"]:
        return [
            prop_group
            for prop_group in cls
            if prop_group
            not in [
                cls.ALL,
                cls.NONE,
                cls.CJK_MINIMUM,
                cls.CJK_BASIC,
                cls.CJK_NUMERIC,
                cls.CJK_READINGS,
                cls.CJK_VARIANTS,
            ]
        ]

    @classmethod
    def get_all_unihan_character_prop_groups(cls) -> list["CharPropertyGroup"]:
        return [prop_group for prop_group in cls if prop_group not in [cls.ALL, cls.NONE, cls.MINIMUM, cls.BASIC]]

    @classmethod
    def match_loosely(cls, value: str) -> "CharPropertyGroup | None":
        prop_names = {e.normalized: e for e in cls if e != cls.NONE}
        prop_aliases = {normalize_string_lm3(e.short_alias): e for e in cls}
        prop_names.update(prop_aliases)
        return prop_names.get(normalize_string_lm3(value), None)
