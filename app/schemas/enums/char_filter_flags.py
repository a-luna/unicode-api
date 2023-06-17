from __future__ import annotations

from enum import IntFlag, auto

from app.data.constants import CHAR_FLAG_MAP
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
        return normalize_string_lm3(self.name)

    @property
    def display_name(self) -> str:
        (name, _, _) = CHAR_FLAG_MAP.get(int(self), ("", "", ""))
        return f'Is_{name.replace("_", " ").title().replace("Ascii", "ASCII").replace(" ", "_")}'

    @property
    def short_alias(self) -> str:
        (_, alias, _) = CHAR_FLAG_MAP.get(int(self), ("", "", ""))
        return alias

    @property
    def has_alias(self) -> bool:  # pragma: no cover
        return True

    @property
    def db_column_name(self) -> str:
        (_, _, db_column) = CHAR_FLAG_MAP.get(int(self), ("", "", ""))
        return db_column

    @classmethod
    def get_char_flags_from_int(cls, char_flags) -> list[CharacterFilterFlags]:
        return [flag for flag in cls if char_flags & flag == flag and flag != cls.NONE]

    @classmethod
    def match_loosely(cls, name: str) -> CharacterFilterFlags:
        flag_name_map = {flag.normalized: flag for flag in cls if flag != cls.NONE}
        flag_name_alias_map = {normalize_string_lm3(flag.short_alias): flag for flag in cls if flag != cls.NONE}
        flag_name_map.update(flag_name_alias_map)
        return flag_name_map.get(normalize_string_lm3(name), cls.NONE)
