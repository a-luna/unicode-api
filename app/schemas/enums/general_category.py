from __future__ import annotations

from enum import IntFlag, auto

from app.schemas.util import normalize_string_lm3


class GeneralCategory(IntFlag):
    NONE = 0
    UPPERCASE_LETTER = auto()
    LOWERCASE_LETTER = auto()
    TITLECASE_LETTER = auto()
    CASED_LETTER = UPPERCASE_LETTER | LOWERCASE_LETTER | TITLECASE_LETTER
    MODIFIER_LETTER = auto()
    OTHER_LETTER = auto()
    LETTER = UPPERCASE_LETTER | LOWERCASE_LETTER | TITLECASE_LETTER | MODIFIER_LETTER | OTHER_LETTER
    NONSPACING_MARK = auto()
    SPACING_MARK = auto()
    ENCLOSING_MARK = auto()
    MARK = NONSPACING_MARK | SPACING_MARK | ENCLOSING_MARK
    DECIMAL_NUMBER = auto()
    LETTER_NUMBER = auto()
    OTHER_NUMBER = auto()
    NUMBER = DECIMAL_NUMBER | LETTER_NUMBER | OTHER_NUMBER
    CONNECTOR_PUNCTUATION = auto()
    DASH_PUNCTUATION = auto()
    OPEN_PUNCTUATION = auto()
    CLOSE_PUNCTUATION = auto()
    INITIAL_PUNCTUATION = auto()
    FINAL_PUNCTUATION = auto()
    OTHER_PUNCTUATION = auto()
    PUNCTUATION = (
        CONNECTOR_PUNCTUATION
        | DASH_PUNCTUATION
        | OPEN_PUNCTUATION
        | CLOSE_PUNCTUATION
        | INITIAL_PUNCTUATION
        | FINAL_PUNCTUATION
        | OTHER_PUNCTUATION
    )
    MATH_SYMBOL = auto()
    CURRENCY_SYMBOL = auto()
    MODIFIER_SYMBOL = auto()
    OTHER_SYMBOL = auto()
    SYMBOL = MATH_SYMBOL | CURRENCY_SYMBOL | MODIFIER_SYMBOL | OTHER_SYMBOL
    SPACE_SEPARATOR = auto()
    LINE_SEPARATOR = auto()
    PARAGRAPH_SEPARATOR = auto()
    SEPARATOR = SPACE_SEPARATOR | LINE_SEPARATOR | PARAGRAPH_SEPARATOR
    CONTROL = auto()
    FORMAT = auto()
    SURROGATE = auto()
    PRIVATE_USE = auto()
    UNASSIGNED = auto()
    OTHER = CONTROL | FORMAT | SURROGATE | PRIVATE_USE | UNASSIGNED

    def __str__(self):
        return self.name.replace("_", " ").title()

    @property
    def display_name(self) -> str:
        return f"{self} ({self.code})"

    @property
    def code(self) -> str:
        code_map = {
            "UPPERCASE_LETTER": "Lu",
            "LOWERCASE_LETTER": "Ll",
            "TITLECASE_LETTER": "Lt",
            "CASED_LETTER": "LC",
            "MODIFIER_LETTER": "Lm",
            "OTHER_LETTER": "Lo",
            "LETTER": "L",
            "NONSPACING_MARK": "Mn",
            "SPACING_MARK": "Mc",
            "ENCLOSING_MARK": "Me",
            "MARK": "M",
            "DECIMAL_NUMBER": "Nd",
            "LETTER_NUMBER": "Nl",
            "OTHER_NUMBER": "No",
            "NUMBER": "N",
            "CONNECTOR_PUNCTUATION": "Pc",
            "DASH_PUNCTUATION": "Pd",
            "OPEN_PUNCTUATION": "Ps",
            "CLOSE_PUNCTUATION": "Pe",
            "INITIAL_PUNCTUATION": "Pi",
            "FINAL_PUNCTUATION": "Pf",
            "OTHER_PUNCTUATION": "Po",
            "PUNCTUATION": "P",
            "MATH_SYMBOL": "Sm",
            "CURRENCY_SYMBOL": "Sc",
            "MODIFIER_SYMBOL": "Sk",
            "OTHER_SYMBOL": "So",
            "SYMBOL": "S",
            "SPACE_SEPARATOR": "Zs",
            "LINE_SEPARATOR": "Zl",
            "PARAGRAPH_SEPARATOR": "Zp",
            "SEPARATOR": "Z",
            "CONTROL": "Cc",
            "FORMAT": "Cf",
            "SURROGATE": "Cs",
            "PRIVATE_USE": "Co",
            "UNASSIGNED": "Cn",
            "OTHER": "C",
        }
        return code_map.get(self.name, "")

    @classmethod
    def code_map(cls):  # pragma: no cover
        return {
            "Lu": cls.UPPERCASE_LETTER,
            "Ll": cls.LOWERCASE_LETTER,
            "Lt": cls.TITLECASE_LETTER,
            "LC": cls.CASED_LETTER,
            "Lm": cls.MODIFIER_LETTER,
            "Lo": cls.OTHER_LETTER,
            "L": cls.LETTER,
            "Mn": cls.NONSPACING_MARK,
            "Mc": cls.SPACING_MARK,
            "Me": cls.ENCLOSING_MARK,
            "M": cls.MARK,
            "Nd": cls.DECIMAL_NUMBER,
            "Nl": cls.LETTER_NUMBER,
            "No": cls.OTHER_NUMBER,
            "N": cls.NUMBER,
            "Pc": cls.CONNECTOR_PUNCTUATION,
            "Pd": cls.DASH_PUNCTUATION,
            "Ps": cls.OPEN_PUNCTUATION,
            "Pe": cls.CLOSE_PUNCTUATION,
            "Pi": cls.INITIAL_PUNCTUATION,
            "Pf": cls.FINAL_PUNCTUATION,
            "Po": cls.OTHER_PUNCTUATION,
            "P": cls.PUNCTUATION,
            "Sm": cls.MATH_SYMBOL,
            "Sc": cls.CURRENCY_SYMBOL,
            "Sk": cls.MODIFIER_SYMBOL,
            "So": cls.OTHER_SYMBOL,
            "S": cls.SYMBOL,
            "Zs": cls.SPACE_SEPARATOR,
            "Zl": cls.LINE_SEPARATOR,
            "Zp": cls.PARAGRAPH_SEPARATOR,
            "Z": cls.SEPARATOR,
            "Cc": cls.CONTROL,
            "Cf": cls.FORMAT,
            "Cs": cls.SURROGATE,
            "Co": cls.PRIVATE_USE,
            "Cn": cls.UNASSIGNED,
            "C": cls.OTHER,
        }

    @classmethod
    def from_code(cls, code):  # pragma: no cover
        return cls.code_map().get(code, cls.NONE)

    @property
    def values(self) -> list[str]:
        values = [cat for cat in GeneralCategory if int(self) & cat == cat if cat not in [GeneralCategory.NONE, self]]
        return [v.code for v in values] if values else [self.code]

    @classmethod
    def match_loosely(cls, name: str) -> GeneralCategory:
        gen_category_map = {normalize_string_lm3(code): category for code, category in cls.code_map().items()}
        return gen_category_map.get(normalize_string_lm3(name), cls.NONE)
