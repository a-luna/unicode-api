from enum import IntFlag, auto
from typing import Self

from app.constants import CHAR_FLAG_MAP
from app.schemas.util import normalize_string_lm3


class CharacterFilterFlags(IntFlag):
    NONE = 0
    MIRRORED = auto()
    BIDIRECTIONAL_CONTROL = auto()
    JOINING_CONTROL = auto()
    UPPERCASE = auto()
    LOWERCASE = auto()
    DASH = auto()
    HYPHEN = auto()
    QUOTATION_MARK = auto()
    TERMINAL_PUNCTUATION = auto()
    SENTENCE_TERMINAL = auto()
    DIACRITIC = auto()
    EXTENDER = auto()
    SOFT_DOTTED = auto()
    ALPHABETIC = auto()
    MATHEMATICAL = auto()
    HEX_DIGIT = auto()
    ASCII_HEX_DIGIT = auto()
    DEFAULT_IGNORABLE_CODE_POINT = auto()
    LOGICAL_ORDER_EXCEPTION = auto()
    PREPENDED_CONCATENATION_MARK = auto()
    WHITE_SPACE = auto()
    REGIONAL_INDICATOR = auto()
    EMOJI = auto()
    EMOJI_PRESENTATION = auto()
    EMOJI_MODIFIER = auto()
    EMOJI_MODIFIER_BASE = auto()
    EMOJI_COMPONENT = auto()
    EXTENDED_PICTOGRAPHIC = auto()
    IDEOGRAPHIC = auto()
    UNIFIED_IDEOGRAPH = auto()
    RADICAL = auto()

    EMOJI_GROUP = (
        EMOJI | EMOJI_PRESENTATION | EMOJI_MODIFIER | EMOJI_MODIFIER_BASE | EMOJI_COMPONENT | EXTENDED_PICTOGRAPHIC
    )

    def __str__(self) -> str:
        return self.display_name

    def __repr__(self) -> str:
        return (
            f"<CharacterFilterFlags>.{self.name}: "
            f'(value={int(self)}, alias="{self.short_alias}", '
            f'display _name="{self.display_name}", db_column_name="{self.db_column_name})"'
        )

    @property
    def normalized(self) -> str:
        return normalize_string_lm3(str(self.name))

    @property
    def flag_name(self) -> str:
        flag = CHAR_FLAG_MAP.get(int(self), None)
        return flag.name.replace("_", " ").title().replace("Ascii", "ASCII").replace(" ", "_") if flag else ""

    @property
    def display_name(self) -> str:
        flag = CHAR_FLAG_MAP.get(int(self), None)
        return f"Is_{self.flag_name}" if flag and self.flag_name else ""

    @property
    def short_alias(self) -> str:
        flag = CHAR_FLAG_MAP.get(int(self), None)
        return flag.alias if flag else ""

    @property
    def has_alias(self) -> bool:  # pragma: no cover
        return True

    @property
    def db_column_name(self) -> str:
        flag = CHAR_FLAG_MAP.get(int(self), None)
        return flag.db_column if flag else ""

    @classmethod
    def is_emoji_flag(cls, flag) -> bool:
        return flag in cls.EMOJI_GROUP

    @classmethod
    def match_loosely(cls, value: str) -> Self:
        flag_name_map = {flag.normalized: flag for flag in cls if flag != cls.NONE}
        flag_name_alias_map = {normalize_string_lm3(flag.short_alias): flag for flag in cls if flag != cls.NONE}
        flag_name_map.update(flag_name_alias_map)
        return flag_name_map.get(normalize_string_lm3(value), cls.NONE)
