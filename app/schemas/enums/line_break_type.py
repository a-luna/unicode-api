from enum import IntEnum, auto
from typing import Self

from app.schemas.util import normalize_string_lm3


class LineBreakType(IntEnum):
    NONE = 0
    ORDINARY_ALPHABETIC_AND_SYMBOL = auto()
    AMBIGUOUS_ALPHABETIC_OR_IDEOGRAPHIC = auto()
    BREAK_OPPORTUNITY_BEFORE_AND_AFTER = auto()
    BREAK_OPPORTUNITY_AFTER = auto()
    BREAK_OPPORTUNITY_BEFORE = auto()
    MANDATORY_BREAK = auto()
    CONTINGENT_BREAK_OPPORTUNITY = auto()
    CLOSING_PUNCTUATION = auto()
    ATTACHED_CHARACTERS_AND_COMBINING_MARKS = auto()
    CARRIAGE_RETURN = auto()
    EXCLAMATION_INTERROGATION = auto()
    NON_BREAKING_GLUE = auto()
    HANGUL_LV_SYLLABLE = auto()
    HANGUL_LVT_SYLLABLE = auto()
    HYPHEN = auto()
    IDEOGRAPHIC = auto()
    INSEPARABLE = auto()
    INFIX_SEPARATOR = auto()
    HANGUL_L_JAMO = auto()
    HANGUL_T_JAMO = auto()
    HANGUL_V_JAMO = auto()
    LINE_FEED = auto()
    NEXT_LINE = auto()
    NON_STARTER = auto()
    NUMERIC = auto()
    OPENING_PUNCTUATION = auto()
    POSTFIX_NUMERIC = auto()
    PREFIX_NUMERIC = auto()
    AMBIGUOUS_QUOTATION = auto()
    COMPLEX_CONTEXT_SOUTH_EAST_ASIAN = auto()
    SURROGATES = auto()
    SPACE = auto()
    SYMBOLS_ALLOWING_BREAKS = auto()
    WORD_JOINER = auto()
    UNKNOWN = auto()
    ZERO_WIDTH_SPACE = auto()

    def __str__(self):
        return (
            self.name.replace("_", " ")
            .title()
            .replace("Alphabetic Or Ideographic", "(Alphabetic Or Ideographic)")
            .replace("Exclamation Interrogation", "Exclamation/Interrogation")
            .replace("Non Breaking Glue", 'Non-breaking ("Glue")')
            .replace("Lv Syllable", "LV Syllable")
            .replace("Lvt Syllable", "LVT Syllable")
            .replace(" Numeric", " (Numeric)")
            .replace("South East Asian", "(South East Asian)")
        )

    @property
    def normalized(self) -> str:
        return normalize_string_lm3(self.code)

    @property
    def display_name(self) -> str:
        return f"{self} ({self.code})"

    @property
    def code(self) -> str:
        code_map = {
            "ORDINARY_ALPHABETIC_AND_SYMBOL": "AL",
            "AMBIGUOUS_ALPHABETIC_OR_IDEOGRAPHIC": "AI",
            "BREAK_OPPORTUNITY_BEFORE_AND_AFTER": "B2",
            "BREAK_OPPORTUNITY_AFTER": "BA",
            "BREAK_OPPORTUNITY_BEFORE": "BB",
            "MANDATORY_BREAK": "BK",
            "CONTINGENT_BREAK_OPPORTUNITY": "CB",
            "CLOSING_PUNCTUATION": "CL",
            "ATTACHED_CHARACTERS_AND_COMBINING_MARKS": "CM",
            "CARRIAGE_RETURN": "CR",
            "EXCLAMATION_INTERROGATION": "EX",
            "NON_BREAKING_GLUE": "GL",
            "HANGUL_LV_SYLLABLE": "H2",
            "HANGUL_LVT_SYLLABLE": "H3",
            "HYPHEN": "HY",
            "IDEOGRAPHIC": "ID",
            "INSEPARABLE": "IN",
            "INFIX_SEPARATOR": "IS",
            "HANGUL_L_JAMO": "JL",
            "HANGUL_T_JAMO": "JT",
            "HANGUL_V_JAMO": "JV",
            "LINE_FEED": "LF",
            "NEXT_LINE": "NL",
            "NON_STARTER": "NS",
            "NUMERIC": "NU",
            "OPENING_PUNCTUATION": "OP",
            "POSTFIX_NUMERIC": "PO",
            "PREFIX_NUMERIC": "PR",
            "AMBIGUOUS_QUOTATION": "QU",
            "COMPLEX_CONTEXT_SOUTH_EAST_ASIAN": "SA",
            "SURROGATES": "SG",
            "SPACE": "SP",
            "SYMBOLS_ALLOWING_BREAKS": "SY",
            "WORD_JOINER": "WJ",
            "UNKNOWN": "XX",
            "ZERO_WIDTH_SPACE": "ZW",
        }
        return code_map.get(self.name, "")

    @classmethod
    def from_code(cls, code):  # pragma: no cover
        code_map = {
            "AL": cls.ORDINARY_ALPHABETIC_AND_SYMBOL,
            "AI": cls.AMBIGUOUS_ALPHABETIC_OR_IDEOGRAPHIC,
            "B2": cls.BREAK_OPPORTUNITY_BEFORE_AND_AFTER,
            "BA": cls.BREAK_OPPORTUNITY_AFTER,
            "BB": cls.BREAK_OPPORTUNITY_BEFORE,
            "BK": cls.MANDATORY_BREAK,
            "CB": cls.CONTINGENT_BREAK_OPPORTUNITY,
            "CL": cls.CLOSING_PUNCTUATION,
            "CM": cls.ATTACHED_CHARACTERS_AND_COMBINING_MARKS,
            "CR": cls.CARRIAGE_RETURN,
            "EX": cls.EXCLAMATION_INTERROGATION,
            "GL": cls.NON_BREAKING_GLUE,
            "H2": cls.HANGUL_LV_SYLLABLE,
            "H3": cls.HANGUL_LVT_SYLLABLE,
            "HY": cls.HYPHEN,
            "ID": cls.IDEOGRAPHIC,
            "IN": cls.INSEPARABLE,
            "IS": cls.INFIX_SEPARATOR,
            "JL": cls.HANGUL_L_JAMO,
            "JT": cls.HANGUL_T_JAMO,
            "JV": cls.HANGUL_V_JAMO,
            "LF": cls.LINE_FEED,
            "NL": cls.NEXT_LINE,
            "NS": cls.NON_STARTER,
            "NU": cls.NUMERIC,
            "OP": cls.OPENING_PUNCTUATION,
            "PO": cls.POSTFIX_NUMERIC,
            "PR": cls.PREFIX_NUMERIC,
            "QU": cls.AMBIGUOUS_QUOTATION,
            "SA": cls.COMPLEX_CONTEXT_SOUTH_EAST_ASIAN,
            "SG": cls.SURROGATES,
            "SP": cls.SPACE,
            "SY": cls.SYMBOLS_ALLOWING_BREAKS,
            "WJ": cls.WORD_JOINER,
            "XX": cls.UNKNOWN,
            "ZW": cls.ZERO_WIDTH_SPACE,
        }
        return code_map.get(code, cls.UNKNOWN)

    @classmethod
    def match_loosely(cls, value: str) -> Self:
        line_break_types_map = {e.normalized: e for e in cls}
        return line_break_types_map.get(normalize_string_lm3(value), cls.NONE)
