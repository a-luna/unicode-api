from typing import Any

from app.data.cache import cached_data
from app.data.constants import (
    ALL_CJK_IDEOGRAPH_BLOCK_IDS,
    DEFAULT_BC_AL_CODEPOINTS,
    DEFAULT_BC_ET_CODEPOINTS,
    DEFAULT_BC_R_CODEPOINTS,
    DEFAULT_VO_U_BLOCK_IDS,
    DEFAULT_VO_U_PLANE_NUMBERS,
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

PROPERTY_GROUPS = {
    CharPropertyGroup.MINIMUM: [
        {
            "name_in": "character",
            "name_out": "character",
            "char_property": "",
            "db_required": False,
            "db_column": False,
            "response_value": lambda char: get_glyph_for_codepoint(char["codepoint_dec"]),
        },
        {
            "name_in": "name",
            "name_out": "name",
            "char_property": "na",
            "db_required": False,
            "db_column": False,
            "response_value": lambda char: cached_data.get_character_name(char["codepoint_dec"]),
        },
        {
            "name_in": "codepoint",
            "name_out": "codepoint",
            "char_property": "cp",
            "db_required": False,
            "db_column": False,
            "response_value": lambda char: get_codepoint_string(char["codepoint_dec"]),
        },
        {
            "name_in": "uri_encoded",
            "name_out": "uri_encoded",
            "char_property": "",
            "db_required": False,
            "db_column": False,
            "response_value": lambda char: get_uri_encoded_value(chr(char["codepoint_dec"])) or ""
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else "",
        },
    ],
    CharPropertyGroup.BASIC: [
        {
            "name_in": "block_id",
            "name_out": "block",
            "char_property": "",
            "db_required": False,
            "db_column": True,
            "response_value": lambda char: get_block_name_containing_codepoint(char["codepoint_dec"]),
        },
        {
            "name_in": "plane_number",
            "name_out": "plane",
            "char_property": "",
            "db_required": False,
            "db_column": True,
            "response_value": lambda char: get_plane_abbreviation_containing_codepoint(char["codepoint_dec"]),
        },
        {
            "name_in": "age",
            "name_out": "age",
            "char_property": "age",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: char["age"] if "age" in char else get_default_age(char["codepoint_dec"]),
        },
        {
            "name_in": "general_category",
            "name_out": "general_category",
            "char_property": "gc",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: GeneralCategory(char["general_category"]).display_name
            if "general_category" in char
            else get_default_general_category_display_name(char["codepoint_dec"]),
        },
        {
            "name_in": "combining_class",
            "name_out": "combining_class",
            "char_property": "ccc",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: CombiningClassCategory(char["combining_class"]).display_name
            if "combining_class" in char
            else CombiningClassCategory.NOT_REORDERED.display_name,
        },
        {
            "name_in": "html_entities",
            "name_out": "html_entities",
            "char_property": "",
            "db_required": False,
            "db_column": False,
            "response_value": lambda char: get_html_entities(char["codepoint_dec"]),
        },
    ],
    CharPropertyGroup.UTF8: [
        {
            "name_in": "utf8",
            "name_out": "utf8",
            "char_property": "",
            "db_required": False,
            "db_column": False,
            "response_value": lambda char: get_utf8_value(chr(char["codepoint_dec"]))
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else "",
        },
        {
            "name_in": "utf8_hex_bytes",
            "name_out": "utf8_hex_bytes",
            "char_property": "",
            "db_required": False,
            "db_column": False,
            "response_value": lambda char: get_utf8_hex_bytes(chr(char["codepoint_dec"]))
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else [],
        },
        {
            "name_in": "utf8_dec_bytes",
            "name_out": "utf8_dec_bytes",
            "char_property": "",
            "db_required": False,
            "db_column": False,
            "response_value": lambda char: get_utf8_dec_bytes(chr(char["codepoint_dec"]))
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else [],
        },
    ],
    CharPropertyGroup.UTF16: [
        {
            "name_in": "utf16",
            "name_out": "utf16",
            "char_property": "",
            "db_required": False,
            "db_column": False,
            "response_value": lambda char: get_utf16_value(chr(char["codepoint_dec"]))
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else "",
        },
        {
            "name_in": "utf16_hex_bytes",
            "name_out": "utf16_hex_bytes",
            "char_property": "",
            "db_required": False,
            "db_column": False,
            "response_value": lambda char: get_utf16_hex_bytes(chr(char["codepoint_dec"]))
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else [],
        },
        {
            "name_in": "utf16_dec_bytes",
            "name_out": "utf16_dec_bytes",
            "char_property": "",
            "db_required": False,
            "db_column": False,
            "response_value": lambda char: get_utf16_dec_bytes(chr(char["codepoint_dec"]))
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else [],
        },
    ],
    CharPropertyGroup.UTF32: [
        {
            "name_in": "utf32",
            "name_out": "utf32",
            "char_property": "",
            "db_required": False,
            "db_column": False,
            "response_value": lambda char: get_utf32_value(chr(char["codepoint_dec"]))
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else "",
        },
        {
            "name_in": "utf32_hex_bytes",
            "name_out": "utf32_hex_bytes",
            "char_property": "",
            "db_required": False,
            "db_column": False,
            "response_value": lambda char: get_utf32_hex_bytes(chr(char["codepoint_dec"]))
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else [],
        },
        {
            "name_in": "utf32_dec_bytes",
            "name_out": "utf32_dec_bytes",
            "char_property": "",
            "db_required": False,
            "db_column": False,
            "response_value": lambda char: get_utf32_dec_bytes(chr(char["codepoint_dec"]))
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else [],
        },
    ],
    CharPropertyGroup.BIDIRECTIONALITY: [
        {
            "name_in": "bidirectional_class",
            "name_out": "bidirectional_class",
            "char_property": "bc",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: BidirectionalClass(char["bidirectional_class"]).display_name
            if "bidirectional_class" in char
            else get_default_bidi_class_display_name(char["codepoint_dec"]),
        },
        {
            "name_in": "bidirectional_is_mirrored",
            "name_out": "bidirectional_is_mirrored",
            "char_property": "Bidi_M",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "bidirectional_is_mirrored"),
        },
        {
            "name_in": "bidirectional_mirroring_glyph",
            "name_out": "bidirectional_mirroring_glyph",
            "char_property": "bmg",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_mapped_codepoint(char["bidirectional_mirroring_glyph"])
            if "bidirectional_mirroring_glyph" in char and cached_data.codepoint_is_assigned(char["codepoint_dec"])
            else get_mapped_codepoint(f'{char["codepoint_dec"]:04X}'),
        },
        {
            "name_in": "bidirectional_control",
            "name_out": "bidirectional_control",
            "char_property": "Bidi_C",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "bidirectional_control"),
        },
        {
            "name_in": "paired_bracket_type",
            "name_out": "paired_bracket_type",
            "char_property": "bpt",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: BidirectionalBracketType(char["paired_bracket_type"]).display_name
            if "paired_bracket_type" in char
            else BidirectionalBracketType.NONE.display_name,
        },
        {
            "name_in": "paired_bracket_property",
            "name_out": "paired_bracket_property",
            "char_property": "bpb",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_char_and_unicode_hex_value(char, "paired_bracket_property"),
        },
    ],
    CharPropertyGroup.DECOMPOSITION: [
        {
            "name_in": "decomposition_type",
            "name_out": "decomposition_type",
            "char_property": "dt",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: DecompositionType(char["decomposition_type"]).display_name
            if "decomposition_type" in char
            else DecompositionType.NONE.display_name,
        },
    ],
    CharPropertyGroup.QUICK_CHECK: [
        {
            "name_in": "NFC_QC",
            "name_out": "NFC_QC",
            "char_property": "NFC_QC",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: str(TriadicLogic(char["NFC_QC"]))
            if "NFC_QC" in char
            else str(TriadicLogic.Y),
        },
        {
            "name_in": "NFD_QC",
            "name_out": "NFD_QC",
            "char_property": "NFD_QC",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: str(TriadicLogic(char["NFD_QC"]))
            if "NFD_QC" in char
            else str(TriadicLogic.Y),
        },
        {
            "name_in": "NFKC_QC",
            "name_out": "NFKC_QC",
            "char_property": "NFKC_QC",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: str(TriadicLogic(char["NFKC_QC"]))
            if "NFKC_QC" in char
            else str(TriadicLogic.Y),
        },
        {
            "name_in": "NFKD_QC",
            "name_out": "NFKD_QC",
            "char_property": "NFKD_QC",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: str(TriadicLogic(char["NFKD_QC"]))
            if "NFKD_QC" in char
            else str(TriadicLogic.Y),
        },
    ],
    CharPropertyGroup.NUMERIC: [
        {
            "name_in": "numeric_type",
            "name_out": "numeric_type",
            "char_property": "nt",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: NumericType(char["numeric_type"]).display_name
            if "numeric_type" in char
            else NumericType.NONE.display_name,
        },
        {
            "name_in": "numeric_value",
            "name_out": "numeric_value",
            "char_property": "nv",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "numeric_value"),
        },
        {
            "name_in": "numeric_value_parsed",
            "name_out": "numeric_value_parsed",
            "char_property": "",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: char["numeric_value_parsed"] if "numeric_value_parsed" in char else 0.0,
        },
    ],
    CharPropertyGroup.JOINING: [
        {
            "name_in": "joining_type",
            "name_out": "joining_type",
            "char_property": "jt",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: JoiningType(char["joining_type"]).display_name
            if "joining_type" in char
            else JoiningType.NON_JOINING.display_name,
        },
        {
            "name_in": "joining_group",
            "name_out": "joining_group",
            "char_property": "jg",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "joining_group"),
        },
        {
            "name_in": "joining_control",
            "name_out": "joining_control",
            "char_property": "Join_C",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "joining_control"),
        },
    ],
    CharPropertyGroup.LINEBREAK: [
        {
            "name_in": "line_break",
            "name_out": "line_break",
            "char_property": "lb",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: LineBreakType(char["line_break"]).display_name
            if "line_break" in char
            else LineBreakType.UNKNOWN.display_name,
        },
    ],
    CharPropertyGroup.EAST_ASIAN_WIDTH: [
        {
            "name_in": "east_asian_width",
            "name_out": "east_asian_width",
            "char_property": "ea",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: EastAsianWidthType(char["east_asian_width"]).display_name
            if "east_asian_width" in char
            else get_default_eaw_display_name(char["codepoint_dec"]),
        },
    ],
    CharPropertyGroup.CASE: [
        {
            "name_in": "uppercase",
            "name_out": "uppercase",
            "char_property": "Upper",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "uppercase"),
        },
        {
            "name_in": "lowercase",
            "name_out": "lowercase",
            "char_property": "Lower",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "lowercase"),
        },
        {
            "name_in": "simple_uppercase_mapping",
            "name_out": "simple_uppercase_mapping",
            "char_property": "suc",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_char_and_unicode_hex_value(char, "simple_uppercase_mapping"),
        },
        {
            "name_in": "simple_lowercase_mapping",
            "name_out": "simple_lowercase_mapping",
            "char_property": "slc",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_char_and_unicode_hex_value(char, "simple_lowercase_mapping"),
        },
        {
            "name_in": "simple_titlecase_mapping",
            "name_out": "simple_titlecase_mapping",
            "char_property": "stc",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_char_and_unicode_hex_value(char, "simple_titlecase_mapping"),
        },
        {
            "name_in": "simple_case_folding",
            "name_out": "simple_case_folding",
            "char_property": "scf",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_char_and_unicode_hex_value(char, "simple_case_folding"),
        },
    ],
    CharPropertyGroup.SCRIPT: [
        {
            "name_in": "script",
            "name_out": "script",
            "char_property": "sc",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: ScriptCode(char["script"]).display_name
            if "script" in char
            else ScriptCode.UNKNOWN.display_name,
        },
        {
            "name_in": "script_extensions",
            "name_out": "script_extensions",
            "char_property": "scx",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_script_extensions(char["script_extensions"])
            if "script_extensions" in char
            else [ScriptCode.UNKNOWN.display_name],
        },
    ],
    CharPropertyGroup.HANGUL: [
        {
            "name_in": "hangul_syllable_type",
            "name_out": "hangul_syllable_type",
            "char_property": "hst",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: HangulSyllableType(char["hangul_syllable_type"]).display_name
            if "hangul_syllable_type" in char
            else HangulSyllableType.NOT_APPLICABLE.display_name,
        },
    ],
    CharPropertyGroup.INDIC: [
        {
            "name_in": "indic_syllabic_category",
            "name_out": "indic_syllabic_category",
            "char_property": "InSC",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "indic_syllabic_category"),
        },
        {
            "name_in": "indic_matra_category",
            "name_out": "indic_matra_category",
            "char_property": "NA",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "indic_matra_category"),
        },
        {
            "name_in": "indic_positional_category",
            "name_out": "indic_positional_category",
            "char_property": "InPC",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "indic_positional_category"),
        },
    ],
    CharPropertyGroup.CJK_MINIMUM: [
        {
            "name_in": "character",
            "name_out": "character",
            "char_property": "",
            "db_required": False,
            "db_column": False,
            "response_value": lambda char: get_glyph_for_codepoint(char["codepoint_dec"]),
        },
        {
            "name_in": "name",
            "name_out": "name",
            "char_property": "na",
            "db_required": False,
            "db_column": False,
            "response_value": lambda char: cached_data.get_character_name(char["codepoint_dec"]),
        },
        {
            "name_in": "description",
            "name_out": "description",
            "char_property": "kDefinition",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "description"),
        },
        {
            "name_in": "codepoint",
            "name_out": "codepoint",
            "char_property": "cp",
            "db_required": False,
            "db_column": False,
            "response_value": lambda char: get_codepoint_string(char["codepoint_dec"]),
        },
        {
            "name_in": "uri_encoded",
            "name_out": "uri_encoded",
            "char_property": "",
            "db_required": False,
            "db_column": False,
            "response_value": lambda char: get_uri_encoded_value(chr(char["codepoint_dec"])) or ""
            if not cached_data.codepoint_is_surrogate(char["codepoint_dec"])
            else "",
        },
    ],
    CharPropertyGroup.CJK_BASIC: [
        {
            "name_in": "ideo_frequency",
            "name_out": "ideo_frequency",
            "char_property": "kFrequency",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_int_prop_value(char, "ideo_frequency"),
        },
        {
            "name_in": "ideo_grade_level",
            "name_out": "ideo_grade_level",
            "char_property": "kGradeLevel",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_int_prop_value(char, "ideo_grade_level"),
        },
        {
            "name_in": "rs_count_unicode",
            "name_out": "rs_count_unicode",
            "char_property": "kRSUnicode",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "rs_count_unicode"),
        },
        {
            "name_in": "rs_count_kangxi",
            "name_out": "rs_count_kangxi",
            "char_property": "kRSKangXi",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "rs_count_kangxi"),
        },
        {
            "name_in": "total_strokes",
            "name_out": "total_strokes",
            "char_property": "kTotalStrokes",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "total_strokes"),
        },
    ],
    CharPropertyGroup.CJK_VARIANTS: [
        {
            "name_in": "traditional_variant",
            "name_out": "traditional_variant",
            "char_property": "kTraditionalVariant",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "traditional_variant"),
        },
        {
            "name_in": "simplified_variant",
            "name_out": "simplified_variant",
            "char_property": "kSimplifiedVariant",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "simplified_variant"),
        },
        {
            "name_in": "z_variant",
            "name_out": "z_variant",
            "char_property": "kZVariant",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "z_variant"),
        },
        {
            "name_in": "compatibility_variant",
            "name_out": "compatibility_variant",
            "char_property": "kCompatibilityVariant",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "compatibility_variant"),
        },
        {
            "name_in": "semantic_variant",
            "name_out": "semantic_variant",
            "char_property": "kSemanticVariant",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "semantic_variant"),
        },
        {
            "name_in": "specialized_semantic_variant",
            "name_out": "specialized_semantic_variant",
            "char_property": "kSpecializedSemanticVariant",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "specialized_semantic_variant"),
        },
        {
            "name_in": "spoofing_variant",
            "name_out": "spoofing_variant",
            "char_property": "kSpoofingVariant",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "spoofing_variant"),
        },
    ],
    CharPropertyGroup.CJK_NUMERIC: [
        {
            "name_in": "accounting_numeric",
            "name_out": "accounting_numeric",
            "char_property": "kAccountingNumeric",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_int_prop_value(char, "accounting_numeric"),
        },
        {
            "name_in": "primary_numeric",
            "name_out": "primary_numeric",
            "char_property": "kPrimaryNumeric",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_int_prop_value(char, "primary_numeric"),
        },
        {
            "name_in": "other_numeric",
            "name_out": "other_numeric",
            "char_property": "kOtherNumeric",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_int_prop_value(char, "other_numeric"),
        },
    ],
    CharPropertyGroup.CJK_READINGS: [
        {
            "name_in": "hangul",
            "name_out": "hangul",
            "char_property": "kHangul",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "hangul"),
        },
        {
            "name_in": "cantonese",
            "name_out": "cantonese",
            "char_property": "kCantonese",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "cantonese"),
        },
        {
            "name_in": "mandarin",
            "name_out": "mandarin",
            "char_property": "kMandarin",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "mandarin"),
        },
        {
            "name_in": "japanese_kun",
            "name_out": "japanese_kun",
            "char_property": "kJapaneseKun",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "japanese_kun"),
        },
        {
            "name_in": "japanese_on",
            "name_out": "japanese_on",
            "char_property": "kJapaneseOn",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "japanese_on"),
        },
        {
            "name_in": "vietnamese",
            "name_out": "vietnamese",
            "char_property": "kVietnamese",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_string_prop_value(char, "vietnamese"),
        },
    ],
    CharPropertyGroup.FUNCTION_AND_GRAPHIC: [
        {
            "name_in": "dash",
            "name_out": "dash",
            "char_property": "Dash",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "dash"),
        },
        {
            "name_in": "hyphen",
            "name_out": "hyphen",
            "char_property": "Hyphen",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "hyphen"),
        },
        {
            "name_in": "quotation_mark",
            "name_out": "quotation_mark",
            "char_property": "QMark",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "quotation_mark"),
        },
        {
            "name_in": "terminal_punctuation",
            "name_out": "terminal_punctuation",
            "char_property": "Term",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "terminal_punctuation"),
        },
        {
            "name_in": "sentence_terminal",
            "name_out": "sentence_terminal",
            "char_property": "STerm",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "sentence_terminal"),
        },
        {
            "name_in": "diacritic",
            "name_out": "diacritic",
            "char_property": "Dia",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "diacritic"),
        },
        {
            "name_in": "extender",
            "name_out": "extender",
            "char_property": "Ext",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "extender"),
        },
        {
            "name_in": "soft_dotted",
            "name_out": "soft_dotted",
            "char_property": "PCM",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "soft_dotted"),
        },
        {
            "name_in": "alphabetic",
            "name_out": "alphabetic",
            "char_property": "SD",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "alphabetic"),
        },
        {
            "name_in": "math",
            "name_out": "math",
            "char_property": "OAlpha",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "math"),
        },
        {
            "name_in": "hex_digit",
            "name_out": "hex_digit",
            "char_property": "OMath",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "hex_digit"),
        },
        {
            "name_in": "ascii_hex_digit",
            "name_out": "ascii_hex_digit",
            "char_property": "Hex",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "ascii_hex_digit"),
        },
        {
            "name_in": "default_ignorable_code_point",
            "name_out": "default_ignorable_code_point",
            "char_property": "AHex",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "default_ignorable_code_point"),
        },
        {
            "name_in": "logical_order_exception",
            "name_out": "logical_order_exception",
            "char_property": "ODI",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "logical_order_exception"),
        },
        {
            "name_in": "prepended_concatenation_mark",
            "name_out": "prepended_concatenation_mark",
            "char_property": "LOE",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "prepended_concatenation_mark"),
        },
        {
            "name_in": "white_space",
            "name_out": "white_space",
            "char_property": "WSpace",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "white_space"),
        },
        {
            "name_in": "vertical_orientation",
            "name_out": "vertical_orientation",
            "char_property": "vo",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: VerticalOrientationType(char["vertical_orientation"]).display_name
            if "vertical_orientation" in char
            else get_default_vo_display_name(char["codepoint_dec"]),
        },
        {
            "name_in": "regional_indicator",
            "name_out": "regional_indicator",
            "char_property": "RI",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "regional_indicator"),
        },
    ],
    CharPropertyGroup.EMOJI: [
        {
            "name_in": "emoji",
            "name_out": "emoji",
            "char_property": "Emoji",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "emoji"),
        },
        {
            "name_in": "emoji_presentation",
            "name_out": "emoji_presentation",
            "char_property": "EPres",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "emoji_presentation"),
        },
        {
            "name_in": "emoji_modifier",
            "name_out": "emoji_modifier",
            "char_property": "EMod",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "emoji_modifier"),
        },
        {
            "name_in": "emoji_modifier_base",
            "name_out": "emoji_modifier_base",
            "char_property": "EBase",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "emoji_modifier_base"),
        },
        {
            "name_in": "emoji_component",
            "name_out": "emoji_component",
            "char_property": "EComp",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "emoji_component"),
        },
        {
            "name_in": "extended_pictographic",
            "name_out": "extended_pictographic",
            "char_property": "ExtPict",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_bool_prop_value(char, "extended_pictographic"),
        },
    ],
}


def get_glyph_for_codepoint(codepoint: int) -> str:
    return (
        chr(9249)
        if codepoint == 127
        else get_control_character_glyph(codepoint)
        if cached_data.codepoint_is_ascii_control_character(codepoint)
        else chr(codepoint) or ""
        if not cached_data.codepoint_is_surrogate(codepoint)
        else ""
    )


def get_control_character_glyph(codepoint: int) -> str:
    return chr(int(f"24{codepoint:02X}", 16))


def get_block_name_containing_codepoint(codepoint: int) -> str:
    block = cached_data.get_unicode_block_containing_codepoint(codepoint)
    return block.name


def get_plane_abbreviation_containing_codepoint(codepoint: int) -> str:
    block = cached_data.get_unicode_block_containing_codepoint(codepoint)
    return block.plane.abbreviation if block.plane else "None"


def get_string_prop_value(char_props: dict[str, Any], prop_name: str) -> str:
    return char_props.get(prop_name, "")


def get_bool_prop_value(char_props: dict[str, Any], prop_name: str) -> bool:
    return True if char_props.get(prop_name, False) else False


def get_int_prop_value(char_props: dict[str, Any], prop_name: str) -> int:
    if prop_value := char_props.get(prop_name, 0):
        return int(prop_value)
    return 0


def get_mapped_codepoint(codepoint_hex: str) -> str:
    return f"{chr(int(codepoint_hex, 16))} (U+{int(codepoint_hex, 16):04X})" if codepoint_hex else ""


def get_char_and_unicode_hex_value(char_props: dict[str, Any], prop_name: str) -> str:
    return get_mapped_codepoint(get_string_prop_value(char_props, prop_name))


def get_default_age(codepoint: int) -> str:
    block = cached_data.get_unicode_block_containing_codepoint(codepoint)
    return "1.1" if block.plane and block.plane.abbreviation == "BMP" else "2.0" if block.plane else ""


def get_default_general_category_display_name(codepoint: int) -> str:
    general_category = (
        GeneralCategory.SURROGATE
        if cached_data.codepoint_is_surrogate(codepoint)
        else GeneralCategory.PRIVATE_USE
        if cached_data.codepoint_is_private_use
        else GeneralCategory.UNASSIGNED
    )
    return general_category.display_name


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
        if cached_data.codepoint_is_private_use
        else EastAsianWidthType.EAST_ASIAN_WIDE
        if block.id in ALL_CJK_IDEOGRAPH_BLOCK_IDS
        else EastAsianWidthType.NEUTRAL_NOT_EAST_ASIAN
    )
    return eaw.display_name


def get_default_vo_display_name(codepoint: int) -> str:
    block = cached_data.get_unicode_block_containing_codepoint(codepoint)
    vo_type = (
        VerticalOrientationType.UPRIGHT
        if block.plane and block.plane.number in DEFAULT_VO_U_PLANE_NUMBERS or block.id in DEFAULT_VO_U_BLOCK_IDS
        else VerticalOrientationType.ROTATED
    )
    return vo_type.display_name


def get_script_extensions(value: str) -> list[str]:
    return [ScriptCode.from_code(script).display_name for script in value.split(" ")]
