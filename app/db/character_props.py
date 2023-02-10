from app.data.cache import cached_data
from app.data.constants import (
    ALL_CJK_IDEOGRAPH_BLOCK_IDS,
    DEFAULT_BC_AL_CODEPOINTS,
    DEFAULT_BC_ET_CODEPOINTS,
    DEFAULT_BC_R_CODEPOINTS,
    DEFAULT_VO_U_BLOCK_IDS,
    DEFAULT_VO_U_PLANE_NUMBERS,
    PRIVATE_USE_BLOCK_IDS,
)
from app.data.encoding import (
    get_codepoint_string,
    get_html_entities,
    get_uri_encoded_value,
    get_utf8_dec_bytes,
    get_utf8_hex_bytes,
    get_utf8_value,
    get_utf16_dec_bytes,
    get_utf16_hex_bytes,
    get_utf16_value,
    get_utf32_dec_bytes,
    get_utf32_hex_bytes,
    get_utf32_value,
)
from app.schemas.enums import (
    BidirectionalBracketType,
    BidirectionalClass,
    CharPropertyGroup,
    CombiningClassCategory,
    DecompositionType,
    EastAsianWidthType,
    GeneralCategory,
    HangulSyllableType,
    JoiningType,
    LineBreakType,
    NumericType,
    ScriptCode,
    TriadicLogic,
    VerticalOrientationType,
)

CHARACTER_PROPERTY_GROUPS = {
    CharPropertyGroup.Minimum: [
        {
            "name_in": "character",
            "name_out": "character",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: chr(char["codepoint_dec"])
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else "",
        },
        {
            "name_in": "name",
            "name_out": "name",
            "char_property": "na",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "codepoint",
            "name_out": "codepoint",
            "char_property": "cp",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: get_codepoint_string(char["codepoint_dec"]),
        },
        {
            "name_in": "uri_encoded",
            "name_out": "uri_encoded",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: get_uri_encoded_value(chr(char["codepoint_dec"]))
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else "",
        },
    ],
    CharPropertyGroup.Basic: [
        {
            "name_in": "block_id",
            "name_out": "block",
            "char_property": "",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: get_block_name_containing_codepoint(char["codepoint_dec"]),
        },
        {
            "name_in": "plane_number",
            "name_out": "plane",
            "char_property": "",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: get_plane_abbreviation_containing_codepoint(char["codepoint_dec"]),
        },
        {
            "name_in": "age",
            "name_out": "age",
            "char_property": "age",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "general_category",
            "name_out": "general_category",
            "char_property": "gc",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: GeneralCategory(char["general_category"]).display_name
            if "general_category" in char
            else GeneralCategory.UNASSIGNED.display_name,
        },
        {
            "name_in": "combining_class",
            "name_out": "combining_class",
            "char_property": "ccc",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: CombiningClassCategory(char["combining_class"]).display_name
            if "combining_class" in char
            else CombiningClassCategory.NOT_REORDERED,
        },
        {
            "name_in": "html_entities",
            "name_out": "html_entities",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: get_html_entities(char["codepoint_dec"]),
        },
    ],
    CharPropertyGroup.UTF8: [
        {
            "name_in": "utf8",
            "name_out": "utf8",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: get_utf8_value(chr(char["codepoint_dec"]))
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else "",
        },
        {
            "name_in": "utf8_hex_bytes",
            "name_out": "utf8_hex_bytes",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: get_utf8_hex_bytes(chr(char["codepoint_dec"]))
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else "",
        },
        {
            "name_in": "utf8_dec_bytes",
            "name_out": "utf8_dec_bytes",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: get_utf8_dec_bytes(chr(char["codepoint_dec"]))
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else "",
        },
    ],
    CharPropertyGroup.UTF16: [
        {
            "name_in": "utf16",
            "name_out": "utf16",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: get_utf16_value(chr(char["codepoint_dec"]))
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else "",
        },
        {
            "name_in": "utf16_hex_bytes",
            "name_out": "utf16_hex_bytes",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: get_utf16_hex_bytes(chr(char["codepoint_dec"]))
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else "",
        },
        {
            "name_in": "utf16_dec_bytes",
            "name_out": "utf16_dec_bytes",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: get_utf16_dec_bytes(chr(char["codepoint_dec"]))
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else "",
        },
    ],
    CharPropertyGroup.UTF32: [
        {
            "name_in": "utf32",
            "name_out": "utf32",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: get_utf32_value(chr(char["codepoint_dec"]))
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else "",
        },
        {
            "name_in": "utf32_hex_bytes",
            "name_out": "utf32_hex_bytes",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: get_utf32_hex_bytes(chr(char["codepoint_dec"]))
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else "",
        },
        {
            "name_in": "utf32_dec_bytes",
            "name_out": "utf32_dec_bytes",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: get_utf32_dec_bytes(chr(char["codepoint_dec"]))
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else "",
        },
    ],
    CharPropertyGroup.Bidirectionality: [
        {
            "name_in": "bidirectional_class",
            "name_out": "bidirectional_class",
            "char_property": "bc",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: BidirectionalClass(char["bidirectional_class"]).display_name
            if "bidirectional_class" in char
            else get_default_bidi_class_display_name(char["codepoint_dec"]),
        },
        {
            "name_in": "bidirectional_is_mirrored",
            "name_out": "bidirectional_is_mirrored",
            "char_property": "Bidi_M",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "bidirectional_mirroring_glyph",
            "name_out": "bidirectional_mirroring_glyph",
            "char_property": "bmg",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: get_mapped_codepoint(char["bidirectional_mirroring_glyph"])
            if "bidirectional_mirroring_glyph" in char
            else "",
        },
        {
            "name_in": "bidirectional_control",
            "name_out": "bidirectional_control",
            "char_property": "Bidi_C",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "paired_bracket_type",
            "name_out": "paired_bracket_type",
            "char_property": "bpt",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: BidirectionalBracketType(char["paired_bracket_type"]).display_name
            if "paired_bracket_type" in char
            else BidirectionalBracketType.NONE.display_name,
        },  # bidirectional paired bracket type, see https://www.unicode.org/Public/15.0.0/ucd/BidiBrackets.txt
        {
            "name_in": "paired_bracket_property",
            "name_out": "paired_bracket_property",
            "char_property": "bpb",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: get_mapped_codepoint(char["paired_bracket_property"])
            if "paired_bracket_property" in char
            else "",
        },  # bidirectional paired bracket property, see https://www.unicode.org/Public/15.0.0/ucd/BidiBrackets.txt
    ],
    CharPropertyGroup.Decomposition: [
        {
            "name_in": "decomposition_type",
            "name_out": "decomposition_type",
            "char_property": "dt",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: DecompositionType(char["decomposition_type"]).display_name
            if "decomposition_type" in char
            else DecompositionType.NONE.display_name,
        },
    ],
    CharPropertyGroup.Quick_Check: [
        {
            "name_in": "NFC_QC",
            "name_out": "NFC_QC",
            "char_property": "NFC_QC",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: str(TriadicLogic(char["NFC_QC"]))
            if "NFC_QC" in char
            else str(TriadicLogic.Y),
        },
        {
            "name_in": "NFD_QC",
            "name_out": "NFD_QC",
            "char_property": "NFD_QC",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: str(TriadicLogic(char["NFD_QC"]))
            if "NFD_QC" in char
            else str(TriadicLogic.Y),
        },
        {
            "name_in": "NFKC_QC",
            "name_out": "NFKC_QC",
            "char_property": "NFKC_QC",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: str(TriadicLogic(char["NFKC_QC"]))
            if "NFKC_QC" in char
            else str(TriadicLogic.Y),
        },
        {
            "name_in": "NFKD_QC",
            "name_out": "NFKD_QC",
            "char_property": "NFKD_QC",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: str(TriadicLogic(char["NFKD_QC"]))
            if "NFKD_QC" in char
            else str(TriadicLogic.Y),
        },
    ],
    CharPropertyGroup.Numeric: [
        {
            "name_in": "numeric_type",
            "name_out": "numeric_type",
            "char_property": "nt",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: NumericType(char["numeric_type"]).display_name
            if "numeric_type" in char
            else NumericType.NONE.display_name,
        },
        {
            "name_in": "numeric_value",
            "name_out": "numeric_value",
            "char_property": "nv",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "numeric_value_parsed",
            "name_out": "numeric_value_parsed",
            "char_property": "",
            "db_column": True,
            "responsify": False,
        },
    ],
    CharPropertyGroup.Joining: [
        {
            "name_in": "joining_type",
            "name_out": "joining_type",
            "char_property": "jt",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: JoiningType(char["joining_type"]).display_name
            if "joining_type" in char
            else JoiningType.NON_JOINING.display_name,
        },
        {
            "name_in": "joining_group",
            "name_out": "joining_group",
            "char_property": "jg",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "joining_control",
            "name_out": "joining_control",
            "char_property": "Join_C",
            "db_column": True,
            "responsify": False,
        },
    ],
    CharPropertyGroup.Linebreak: [
        {
            "name_in": "line_break",
            "name_out": "line_break",
            "char_property": "lb",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: LineBreakType(char["line_break"]).display_name
            if "line_break" in char
            else LineBreakType.UNKNOWN,
        },
    ],
    CharPropertyGroup.East_Asian_Width: [
        {
            "name_in": "east_asian_width",
            "name_out": "east_asian_width",
            "char_property": "ea",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: EastAsianWidthType(char["east_asian_width"]).display_name
            if "east_asian_width" in char
            else get_default_eaw_display_name(char["codepoint_dec"]),
        },
    ],
    CharPropertyGroup.Case: [
        {
            "name_in": "uppercase",
            "name_out": "uppercase",
            "char_property": "Upper",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "lowercase",
            "name_out": "lowercase",
            "char_property": "Lower",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "simple_uppercase_mapping",
            "name_out": "simple_uppercase_mapping",
            "char_property": "suc",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: get_mapped_codepoint(char["simple_uppercase_mapping"])
            if "simple_uppercase_mapping" in char
            else "",
        },
        {
            "name_in": "simple_lowercase_mapping",
            "name_out": "simple_lowercase_mapping",
            "char_property": "slc",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: get_mapped_codepoint(char["simple_lowercase_mapping"])
            if "simple_lowercase_mapping" in char
            else "",
        },
        {
            "name_in": "simple_titlecase_mapping",
            "name_out": "simple_titlecase_mapping",
            "char_property": "stc",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: get_mapped_codepoint(char["simple_titlecase_mapping"])
            if "simple_titlecase_mapping" in char
            else "",
        },
        {
            "name_in": "simple_case_folding",
            "name_out": "simple_case_folding",
            "char_property": "scf",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: get_mapped_codepoint(char["simple_case_folding"])
            if "simple_case_folding" in char
            else "",
        },
    ],
    CharPropertyGroup.Script: [
        {
            "name_in": "script",
            "name_out": "script",
            "char_property": "sc",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: ScriptCode(char["script"]).display_name
            if "script" in char
            else ScriptCode.UNKNOWN.display_name,
        },
        {
            "name_in": "script_extensions",
            "name_out": "script_extensions",
            "char_property": "scx",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: get_script_extensions(char["script_extensions"])
            if "script_extensions" in char
            else [ScriptCode.UNKNOWN.display_name],
        },
    ],
    CharPropertyGroup.Hangul: [
        {
            "name_in": "hangul_syllable_type",
            "name_out": "hangul_syllable_type",
            "char_property": "hst",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: HangulSyllableType(char["hangul_syllable_type"]).display_name
            if "hangul_syllable_type" in char
            else HangulSyllableType.NOT_APPLICABLE.display_name,
        },
    ],
    CharPropertyGroup.Indic: [
        {
            "name_in": "indic_syllabic_category",
            "name_out": "indic_syllabic_category",
            "char_property": "InSC",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "indic_matra_category",
            "name_out": "indic_matra_category",
            "char_property": "NA",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "indic_positional_category",
            "name_out": "indic_positional_category",
            "char_property": "InPC",
            "db_column": True,
            "responsify": False,
        },
    ],
    CharPropertyGroup.Function_and_Graphic: [
        {
            "name_in": "dash",
            "name_out": "dash",
            "char_property": "Dash",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "hyphen",
            "name_out": "hyphen",
            "char_property": "Hyphen",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "quotation_mark",
            "name_out": "quotation_mark",
            "char_property": "QMark",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "terminal_punctuation",
            "name_out": "terminal_punctuation",
            "char_property": "Term",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "sentence_terminal",
            "name_out": "sentence_terminal",
            "char_property": "STerm",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "diacritic",
            "name_out": "diacritic",
            "char_property": "Dia",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "extender",
            "name_out": "extender",
            "char_property": "Ext",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "soft_dotted",
            "name_out": "soft_dotted",
            "char_property": "PCM",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "alphabetic",
            "name_out": "alphabetic",
            "char_property": "SD",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "math",
            "name_out": "math",
            "char_property": "OAlpha",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "hex_digit",
            "name_out": "hex_digit",
            "char_property": "OMath",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "ascii_hex_digit",
            "name_out": "ascii_hex_digit",
            "char_property": "Hex",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "default_ignorable_code_point",
            "name_out": "default_ignorable_code_point",
            "char_property": "AHex",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "logical_order_exception",
            "name_out": "logical_order_exception",
            "char_property": "ODI",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "prepended_concatenation_mark",
            "name_out": "prepended_concatenation_mark",
            "char_property": "LOE",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "white_space",
            "name_out": "white_space",
            "char_property": "WSpace",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "vertical_orientation",
            "name_out": "vertical_orientation",
            "char_property": "vo",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: VerticalOrientationType(char["vertical_orientation"]).display_name
            if "vertical_orientation" in char
            else get_default_vo_display_name(char["codepoint_dec"]),
        },
        {
            "name_in": "regional_indicator",
            "name_out": "regional_indicator",
            "char_property": "RI",
            "db_column": True,
            "responsify": False,
        },
    ],
    CharPropertyGroup.Emoji: [
        {
            "name_in": "emoji",
            "name_out": "emoji",
            "char_property": "Emoji",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "emoji_presentation",
            "name_out": "emoji_presentation",
            "char_property": "EPres",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "emoji_modifier",
            "name_out": "emoji_modifier",
            "char_property": "EMod",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "emoji_modifier_base",
            "name_out": "emoji_modifier_base",
            "char_property": "EBase",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "emoji_component",
            "name_out": "emoji_component",
            "char_property": "EComp",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "extended_pictographic",
            "name_out": "extended_pictographic",
            "char_property": "ExtPict",
            "db_column": True,
            "responsify": False,
        },
    ],
}


def get_block_name_containing_codepoint(codepoint: int) -> str:
    block = cached_data.get_unicode_block_containing_codepoint(codepoint)
    return block.name


def get_plane_abbreviation_containing_codepoint(codepoint: int) -> str:
    block = cached_data.get_unicode_block_containing_codepoint(codepoint)
    return block.plane.abbreviation


def get_default_bidi_class_display_name(codepoint: int) -> str:
    bidi_class = (
        BidirectionalClass.RIGHT_TO_LEFT
        if codepoint in DEFAULT_BC_R_CODEPOINTS
        else BidirectionalClass.ARABIC_LETTER
        if codepoint in DEFAULT_BC_AL_CODEPOINTS
        else BidirectionalClass.EUROPEAN_TERMINATOR
        if codepoint in DEFAULT_BC_ET_CODEPOINTS
        else BidirectionalClass.LEFT_TO_RIGHT
    )
    return bidi_class.display_name


def get_default_eaw_display_name(codepoint: int) -> str:
    block = cached_data.get_unicode_block_containing_codepoint(codepoint)
    eaw = (
        EastAsianWidthType.EAST_ASIAN_AMBIGUOUS
        if block.id in PRIVATE_USE_BLOCK_IDS
        else EastAsianWidthType.EAST_ASIAN_WIDE
        if block.id in ALL_CJK_IDEOGRAPH_BLOCK_IDS
        else EastAsianWidthType.NEUTRAL_NOT_EAST_ASIAN
    )
    return eaw.display_name


def get_default_vo_display_name(codepoint: int) -> str:
    block = cached_data.get_unicode_block_containing_codepoint(codepoint)
    vo_type = (
        VerticalOrientationType.UPRIGHT
        if block.plane.number in DEFAULT_VO_U_PLANE_NUMBERS or block.id in DEFAULT_VO_U_BLOCK_IDS
        else VerticalOrientationType.ROTATED
    )
    return vo_type.display_name


def get_mapped_codepoint(codepoint_hex: str, include_char_name: bool = False) -> str:
    return (
        ""
        if not codepoint_hex
        else f"{chr(int(codepoint_hex, 16))} (U+{int(codepoint_hex, 16):04X} {cached_data.get_character_name(int(codepoint_hex, 16))})"
        if include_char_name
        else f"{chr(int(codepoint_hex, 16))} (U+{int(codepoint_hex, 16):04X})"
    )


def get_script_extensions(value: str) -> list[str]:
    return [ScriptCode.from_code(script).display_name for script in value.split(" ")]
