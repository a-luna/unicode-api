import re
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from unicode_api.custom_types import UnicodePropertyGroupMap, UnicodePropertyGroupValues

MAX_CODEPOINT = int("10FFFF", 16)
ALL_UNICODE_CODEPOINTS = range(MAX_CODEPOINT + 1)
ASCII_HEX = "0123456789ABCDEFabcdef"
PROP_GROUP_INVALID_FOR_VERSION_ROW_ID = 999999

DATE_MONTH_NAME = "%b %d, %Y"

CP_PREFIX_1_REGEX = re.compile(r"(?:U\+([A-Fa-f0-9]{4,6}))")
CP_PREFIX_1_REGEX_STRICT = re.compile(r"^U\+([A-Fa-f0-9]{4,6})$")
CP_PREFIX_2_REGEX_STRICT = re.compile(r"^0x([A-Fa-f0-9]{2,6})$")
CP_NO_PREFIX_REGEX_STRICT = re.compile(r"^([A-Fa-f0-9]{2,6})$")
CP_NEED_LEADING_ZEROS_REGEX = re.compile(r"^U\+([A-Fa-f0-9]{1,3})$")
CP_OUT_OF_RANGE_REGEX = re.compile(r"^(?:U\+)([A-Fa-f0-9]+)|(?:0x)?([A-Fa-f0-9]{7,})$")

LOCALE_REGEX = re.compile(r"(?P<lang>[a-zA-Z]{2,3})(?:-(?P<variant>[a-zA-Z]{2}))?")

ALL_PROP_GROUPS = [
    "Age",
    "Bidi_Class",
    "Bidi_Paired_Bracket_Type",
    "Canonical_Combining_Class",
    "Decomposition_Type",
    "East_Asian_Width",
    "General_Category",
    "Grapheme_Cluster_Break",
    "Hangul_Syllable_Type",
    "Indic_Conjunct_Break",
    "Indic_Positional_Category",
    "Indic_Syllabic_Category",
    "Jamo_Short_Name",
    "Joining_Group",
    "Joining_Type",
    "Line_Break",
    "NFC_Quick_Check",
    "NFD_Quick_Check",
    "NFKC_Quick_Check",
    "NFKD_Quick_Check",
    "Numeric_Type",
    "Script",
    "Sentence_Break",
    "Vertical_Orientation",
    "Word_Break",
]

CHAR_PROP_DEFAULT_VALUES: "UnicodePropertyGroupValues" = {
    "id": 1,
    "short_name": "",
    "long_name": "",
}

CHAR_PROP_DEFAULT_VALUE_MAP = {"1": CHAR_PROP_DEFAULT_VALUES}

PROP_GROUP_VALUE_MAP_DEFAULT: "UnicodePropertyGroupMap" = {
    "Age": CHAR_PROP_DEFAULT_VALUE_MAP,
    "Bidi_Class": CHAR_PROP_DEFAULT_VALUE_MAP,
    "Bidi_Paired_Bracket_Type": CHAR_PROP_DEFAULT_VALUE_MAP,
    "Canonical_Combining_Class": CHAR_PROP_DEFAULT_VALUE_MAP,
    "Decomposition_Type": CHAR_PROP_DEFAULT_VALUE_MAP,
    "East_Asian_Width": CHAR_PROP_DEFAULT_VALUE_MAP,
    "General_Category": CHAR_PROP_DEFAULT_VALUE_MAP,
    "Grapheme_Cluster_Break": CHAR_PROP_DEFAULT_VALUE_MAP,
    "Hangul_Syllable_Type": CHAR_PROP_DEFAULT_VALUE_MAP,
    "Indic_Conjunct_Break": CHAR_PROP_DEFAULT_VALUE_MAP,
    "Indic_Positional_Category": CHAR_PROP_DEFAULT_VALUE_MAP,
    "Indic_Syllabic_Category": CHAR_PROP_DEFAULT_VALUE_MAP,
    "Jamo_Short_Name": CHAR_PROP_DEFAULT_VALUE_MAP,
    "Joining_Group": CHAR_PROP_DEFAULT_VALUE_MAP,
    "Joining_Type": CHAR_PROP_DEFAULT_VALUE_MAP,
    "Line_Break": CHAR_PROP_DEFAULT_VALUE_MAP,
    "NFC_Quick_Check": CHAR_PROP_DEFAULT_VALUE_MAP,
    "NFD_Quick_Check": CHAR_PROP_DEFAULT_VALUE_MAP,
    "NFKC_Quick_Check": CHAR_PROP_DEFAULT_VALUE_MAP,
    "NFKD_Quick_Check": CHAR_PROP_DEFAULT_VALUE_MAP,
    "Numeric_Type": CHAR_PROP_DEFAULT_VALUE_MAP,
    "Script": CHAR_PROP_DEFAULT_VALUE_MAP,
    "Sentence_Break": CHAR_PROP_DEFAULT_VALUE_MAP,
    "Vertical_Orientation": CHAR_PROP_DEFAULT_VALUE_MAP,
    "Word_Break": CHAR_PROP_DEFAULT_VALUE_MAP,
    "boolean_properties": [],
    "missing_prop_groups": [],
}

UNICODE_PLANES_DEFAULT = [
    {
        "id": 1,
        "number": 0,
        "name": "Basic Multilingual Plane",
        "abbreviation": "BMP",
        "start": "0000",
        "start_dec": int("0000", 16),
        "finish": "FFFF",
        "finish_dec": int("FFFF", 16),
        "start_block_id": 0,
        "finish_block_id": 0,
        "total_allocated": 0,
        "total_defined": 0,
    },
    {
        "id": 2,
        "number": 1,
        "name": "Supplementary Multilingual Plane",
        "abbreviation": "SMP",
        "start": "10000",
        "start_dec": int("10000", 16),
        "finish": "1FFFF",
        "finish_dec": int("1FFFF", 16),
        "start_block_id": 0,
        "finish_block_id": 0,
        "total_allocated": 0,
        "total_defined": 0,
    },
    {
        "id": 3,
        "number": 2,
        "name": "Supplementary Ideographic Plane",
        "abbreviation": "SIP",
        "start": "20000",
        "start_dec": int("20000", 16),
        "finish": "2FFFF",
        "finish_dec": int("2FFFF", 16),
        "start_block_id": 0,
        "finish_block_id": 0,
        "total_allocated": 0,
        "total_defined": 0,
    },
    {
        "id": 4,
        "number": 3,
        "name": "Tertiary Ideographic Plane",
        "abbreviation": "TIP",
        "start": "30000",
        "start_dec": int("30000", 16),
        "finish": "3FFFF",
        "finish_dec": int("3FFFF", 16),
        "start_block_id": 0,
        "finish_block_id": 0,
        "total_allocated": 0,
        "total_defined": 0,
    },
    {
        "id": 5,
        "number": 14,
        "name": "Supplementary Special-purpose Plane",
        "abbreviation": "SSP",
        "start": "E0000",
        "start_dec": int("E0000", 16),
        "finish": "EFFFF",
        "finish_dec": int("EFFFF", 16),
        "start_block_id": 0,
        "finish_block_id": 0,
        "total_allocated": 0,
        "total_defined": 0,
    },
    {
        "id": 6,
        "number": 15,
        "name": "Supplementary Private Use Area-A",
        "abbreviation": "SPUA-A",
        "start": "F0000",
        "start_dec": int("F0000", 16),
        "finish": "FFFFF",
        "finish_dec": int("FFFFF", 16),
        "start_block_id": 0,
        "finish_block_id": 0,
        "total_allocated": 0,
        "total_defined": 0,
    },
    {
        "id": 7,
        "number": 16,
        "name": "Supplementary Private Use Area-B",
        "abbreviation": "SPUA-B",
        "start": "100000",
        "start_dec": int("100000", 16),
        "finish": "10FFFF",
        "finish_dec": int("10FFFF", 16),
        "start_block_id": 0,
        "finish_block_id": 0,
        "total_allocated": 0,
        "total_defined": 0,
    },
]

UNSUPPORTED_UNICODE_VERSION_RELEASE_DATES = {
    "1.0.0": date(1991, 10, 1),
    "1.0.1": date(1992, 6, 1),
    "1.1.0": date(1993, 6, 1),
    "1.1.5": date(1995, 7, 1),
    "2.0.0": date(1996, 7, 1),
    "2.1.2": date(1998, 5, 1),
    "2.1.5": date(1998, 8, 1),
    "2.1.8": date(1998, 12, 1),
    "2.1.9": date(1999, 4, 1),
    "3.0.0": date(1999, 9, 1),
    "3.0.1": date(2000, 8, 1),
    "3.1.0": date(2001, 3, 1),
    "3.1.1": date(2001, 8, 1),
    "3.2.0": date(2002, 3, 1),
    "4.0.0": date(2003, 4, 1),
    "4.0.1": date(2004, 3, 1),
    "4.1.0": date(2005, 3, 31),
    "5.0.0": date(2006, 7, 14),
}


SUPPORTED_UNICODE_VERSION_RELEASE_DATES = {
    "5.1.0": date(2008, 4, 4),
    "5.2.0": date(2009, 10, 1),
    "6.0.0": date(2010, 10, 11),
    "6.1.0": date(2012, 1, 31),
    "6.2.0": date(2012, 9, 26),
    "6.3.0": date(2013, 9, 30),
    "7.0.0": date(2014, 6, 16),
    "8.0.0": date(2015, 6, 17),
    "9.0.0": date(2016, 6, 21),
    "10.0.0": date(2017, 6, 20),
    "11.0.0": date(2018, 6, 5),
    "12.0.0": date(2019, 3, 5),
    "12.1.0": date(2019, 5, 11),
    "13.0.0": date(2020, 3, 10),
    "14.0.0": date(2021, 9, 14),
    "15.0.0": date(2022, 9, 13),
    "15.1.0": date(2023, 9, 12),
    "16.0.0": date(2024, 9, 10),
    "17.0.0": date(2025, 9, 5),
}

UNICODE_VERSION_RELEASE_DATES = UNSUPPORTED_UNICODE_VERSION_RELEASE_DATES | SUPPORTED_UNICODE_VERSION_RELEASE_DATES
SUPPORTED_UNICODE_VERSIONS = list(SUPPORTED_UNICODE_VERSION_RELEASE_DATES.keys())

NON_CHARACTER_CODEPOINTS = (
    list(range(int("FDD0", 16), int("FDEF", 16) + 1))
    + [int("FFFE", 16), int("FFFF", 16)]
    + [int("1FFFE", 16), int("1FFFF", 16)]
    + [int("2FFFE", 16), int("2FFFF", 16)]
    + [int("3FFFE", 16), int("3FFFF", 16)]
    + [int("4FFFE", 16), int("4FFFF", 16)]
    + [int("5FFFE", 16), int("5FFFF", 16)]
    + [int("6FFFE", 16), int("6FFFF", 16)]
    + [int("7FFFE", 16), int("7FFFF", 16)]
    + [int("8FFFE", 16), int("8FFFF", 16)]
    + [int("9FFFE", 16), int("9FFFF", 16)]
    + [int("AFFFE", 16), int("AFFFF", 16)]
    + [int("BFFFE", 16), int("BFFFF", 16)]
    + [int("CFFFE", 16), int("CFFFF", 16)]
    + [int("DFFFE", 16), int("DFFFF", 16)]
    + [int("EFFFE", 16), int("EFFFF", 16)]
    + [int("FFFFE", 16), int("FFFFF", 16)]
    + [int("10FFFE", 16), int("10FFFF", 16)]
)

C0_CONTROL_CHARACTERS = list(range(int("0", 16), int("1F", 16) + 1))
C1_CONTROL_CHARACTERS = list(range(int("7F", 16), int("9F", 16) + 1))
ALL_CONTROL_CHARACTERS = C0_CONTROL_CHARACTERS + C1_CONTROL_CHARACTERS

DEFAULT_BC_R_CODEPOINTS = (
    list(range(int("0590", 16), int("05FF", 16) + 1))
    + list(range(int("07C0", 16), int("085F", 16) + 1))
    + list(range(int("FB1D", 16), int("FB4F", 16) + 1))
    + list(range(int("10800", 16), int("10CFF", 16) + 1))
    + list(range(int("10D40", 16), int("10EBF", 16) + 1))
    + list(range(int("10F00", 16), int("10F2F", 16) + 1))
    + list(range(int("10F70", 16), int("10FFF", 16) + 1))
    + list(range(int("1E800", 16), int("1EC6F", 16) + 1))
    + list(range(int("1E800", 16), int("1EC6F", 16) + 1))
    + list(range(int("1ECC0", 16), int("1ECFF", 16) + 1))
    + list(range(int("1ED50", 16), int("1EDFF", 16) + 1))
    + list(range(int("1EF00", 16), int("1EFFF", 16) + 1))
)

DEFAULT_BC_AL_CODEPOINTS = (
    list(range(int("0600", 16), int("07BF", 16) + 1))
    + list(range(int("0860", 16), int("08FF", 16) + 1))
    + list(range(int("FB50", 16), int("FDCF", 16) + 1))
    + list(range(int("FDF0", 16), int("FDFF", 16) + 1))
    + list(range(int("FE70", 16), int("FEFF", 16) + 1))
    + list(range(int("10D00", 16), int("10D3F", 16) + 1))
    + list(range(int("10EC0", 16), int("10EFF", 16) + 1))
    + list(range(int("10F30", 16), int("10F6F", 16) + 1))
    + list(range(int("1EC70", 16), int("1ECBF", 16) + 1))
    + list(range(int("1ED00", 16), int("1ED4F", 16) + 1))
    + list(range(int("1EE00", 16), int("1EEFF", 16) + 1))
)

DEFAULT_BC_ET_CODEPOINTS = list(range(int("20A0", 16), int("20CF", 16) + 1))

DEFAULT_VO_U_BLOCK_NAMES = [
    "Unified Canadian Aboriginal Syllabics Extended",
    "Number Forms",
    "Control Pictures",
    "Miscellaneous Symbols and Arrows",
    "CJK Radicals Supplement",
    "Kangxi Radicals",
    "Ideographic Description Characters",
    "CJK Symbols and Punctuation",
    "Hiragana",
    "Katakana",
    "Bopomofo",
    "Hangul Compatibility Jamo",
    "Kanbun",
    "Bopomofo Extended",
    "CJK Strokes",
    "Katakana Phonetic Extensions",
    "Enclosed CJK Letters and Months",
    "CJK Compatibility",
    "CJK Unified Ideographs Extension A",
    "Yijing Hexagram Symbols",
    "CJK Unified Ideographs",
    "Yi Syllables",
    "Yi Radicals",
    "Hangul Jamo Extended-A",
    "Meetei Mayek",
    "Hangul Syllables",
    "Hangul Jamo Extended-B",
    "Private Use Area",
    "CJK Compatibility Ideographs",
    "Vertical Forms",
    "Small Form Variants",
    "Specials",
    "Siddham",
    "Zanabazar Square",
    "Soyombo",
    "Egyptian Hieroglyphs",
    "Egyptian Hieroglyph Format Controls",
    "Anatolian Hieroglyphs",
    "Ideographic Symbols and Punctuation",
    "Tangut",
    "Tangut Components",
    "Khitan Small Script",
    "Tangut Supplement",
    "Kana Extended-B",
    "Kana Extended-A",
    "Small Kana Extension",
    "Nushu",
    "Znamenny Musical Notation",
    "Byzantine Musical Symbols",
    "Musical Symbols",
    "Mayan Numerals",
    "Tai Xuan Jing Symbols",
    "Counting Rod Numerals",
    "Sutton SignWriting",
    "Mahjong Tiles",
    "Domino Tiles",
    "Playing Cards",
    "Enclosed Alphanumeric Supplement",
    "Enclosed Ideographic Supplement",
    "Transport and Map Symbols",
    "Alchemical Symbols",
    "Supplemental Symbols and Pictographs",
    "Chess Symbols",
    "Symbols and Pictographs Extended-A",
]

DEFAULT_VO_U_PLANE_NUMBERS = [2, 3, 15, 16]

# fmt: off
DEFAULT_EP_TRUE_CODEPOINTS = (
    list(range(int("1F000", 16), int("1FAFF", 16) + 1))
    + list(range(int("1FC00", 16), int("1FFFD", 16) + 1))
)
# fmt: on
