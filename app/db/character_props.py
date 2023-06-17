import app.schemas.enums as enum
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

CHARACTER_PROPERTY_GROUPS = {
    enum.CharPropertyGroup.Minimum: [
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
    enum.CharPropertyGroup.Basic: [
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
            "response_value": lambda char: enum.GeneralCategory(char["general_category"]).display_name
            if "general_category" in char
            else get_default_general_category_display_name(char["codepoint_dec"]),
        },
        {
            "name_in": "combining_class",
            "name_out": "combining_class",
            "char_property": "ccc",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: enum.CombiningClassCategory(char["combining_class"]).display_name
            if "combining_class" in char
            else enum.CombiningClassCategory.NOT_REORDERED.display_name,
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
    enum.CharPropertyGroup.UTF8: [
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
    enum.CharPropertyGroup.UTF16: [
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
    enum.CharPropertyGroup.UTF32: [
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
    enum.CharPropertyGroup.Bidirectionality: [
        {
            "name_in": "bidirectional_class",
            "name_out": "bidirectional_class",
            "char_property": "bc",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: enum.BidirectionalClass(char["bidirectional_class"]).display_name
            if "bidirectional_class" in char
            else get_default_bidi_class_display_name(char["codepoint_dec"]),
        },
        {
            "name_in": "bidirectional_is_mirrored",
            "name_out": "bidirectional_is_mirrored",
            "char_property": "Bidi_M",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["bidirectional_is_mirrored"])
            if "bidirectional_is_mirrored" in char
            else False,
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
            "response_value": lambda char: bool(char["bidirectional_control"])
            if "bidirectional_control" in char
            else False,
        },
        {
            "name_in": "paired_bracket_type",
            "name_out": "paired_bracket_type",
            "char_property": "bpt",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: enum.BidirectionalBracketType(char["paired_bracket_type"]).display_name
            if "paired_bracket_type" in char
            else enum.BidirectionalBracketType.NONE.display_name,
        },  # bidirectional paired bracket type, see https://www.unicode.org/Public/15.0.0/ucd/BidiBrackets.txt
        {
            "name_in": "paired_bracket_property",
            "name_out": "paired_bracket_property",
            "char_property": "bpb",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_mapped_codepoint(char["paired_bracket_property"])
            if "paired_bracket_property" in char
            else "",
        },  # bidirectional paired bracket property, see https://www.unicode.org/Public/15.0.0/ucd/BidiBrackets.txt
    ],
    enum.CharPropertyGroup.Decomposition: [
        {
            "name_in": "decomposition_type",
            "name_out": "decomposition_type",
            "char_property": "dt",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: enum.DecompositionType(char["decomposition_type"]).display_name
            if "decomposition_type" in char
            else enum.DecompositionType.NONE.display_name,
        },
    ],
    enum.CharPropertyGroup.Quick_Check: [
        {
            "name_in": "NFC_QC",
            "name_out": "NFC_QC",
            "char_property": "NFC_QC",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: str(enum.TriadicLogic(char["NFC_QC"]))
            if "NFC_QC" in char
            else str(enum.TriadicLogic.Y),
        },
        {
            "name_in": "NFD_QC",
            "name_out": "NFD_QC",
            "char_property": "NFD_QC",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: str(enum.TriadicLogic(char["NFD_QC"]))
            if "NFD_QC" in char
            else str(enum.TriadicLogic.Y),
        },
        {
            "name_in": "NFKC_QC",
            "name_out": "NFKC_QC",
            "char_property": "NFKC_QC",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: str(enum.TriadicLogic(char["NFKC_QC"]))
            if "NFKC_QC" in char
            else str(enum.TriadicLogic.Y),
        },
        {
            "name_in": "NFKD_QC",
            "name_out": "NFKD_QC",
            "char_property": "NFKD_QC",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: str(enum.TriadicLogic(char["NFKD_QC"]))
            if "NFKD_QC" in char
            else str(enum.TriadicLogic.Y),
        },
    ],
    enum.CharPropertyGroup.Numeric: [
        {
            "name_in": "numeric_type",
            "name_out": "numeric_type",
            "char_property": "nt",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: enum.NumericType(char["numeric_type"]).display_name
            if "numeric_type" in char
            else enum.NumericType.NONE.display_name,
        },
        {
            "name_in": "numeric_value",
            "name_out": "numeric_value",
            "char_property": "nv",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: char["numeric_value"] if "numeric_value" in char else "",
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
    enum.CharPropertyGroup.Joining: [
        {
            "name_in": "joining_type",
            "name_out": "joining_type",
            "char_property": "jt",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: enum.JoiningType(char["joining_type"]).display_name
            if "joining_type" in char
            else enum.JoiningType.NON_JOINING.display_name,
        },
        {
            "name_in": "joining_group",
            "name_out": "joining_group",
            "char_property": "jg",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: char["joining_group"] if "joining_group" in char else "",
        },
        {
            "name_in": "joining_control",
            "name_out": "joining_control",
            "char_property": "Join_C",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["joining_control"]) if "joining_control" in char else False,
        },
    ],
    enum.CharPropertyGroup.Linebreak: [
        {
            "name_in": "line_break",
            "name_out": "line_break",
            "char_property": "lb",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: enum.LineBreakType(char["line_break"]).display_name
            if "line_break" in char
            else enum.LineBreakType.UNKNOWN.display_name,
        },
    ],
    enum.CharPropertyGroup.East_Asian_Width: [
        {
            "name_in": "east_asian_width",
            "name_out": "east_asian_width",
            "char_property": "ea",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: enum.EastAsianWidthType(char["east_asian_width"]).display_name
            if "east_asian_width" in char
            else get_default_eaw_display_name(char["codepoint_dec"]),
        },
    ],
    enum.CharPropertyGroup.Case: [
        {
            "name_in": "uppercase",
            "name_out": "uppercase",
            "char_property": "Upper",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["uppercase"]) if "uppercase" in char else False,
        },
        {
            "name_in": "lowercase",
            "name_out": "lowercase",
            "char_property": "Lower",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["lowercase"]) if "lowercase" in char else False,
        },
        {
            "name_in": "simple_uppercase_mapping",
            "name_out": "simple_uppercase_mapping",
            "char_property": "suc",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_mapped_codepoint(char["simple_uppercase_mapping"])
            if "simple_uppercase_mapping" in char
            else "",
        },
        {
            "name_in": "simple_lowercase_mapping",
            "name_out": "simple_lowercase_mapping",
            "char_property": "slc",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_mapped_codepoint(char["simple_lowercase_mapping"])
            if "simple_lowercase_mapping" in char
            else "",
        },
        {
            "name_in": "simple_titlecase_mapping",
            "name_out": "simple_titlecase_mapping",
            "char_property": "stc",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_mapped_codepoint(char["simple_titlecase_mapping"])
            if "simple_titlecase_mapping" in char
            else "",
        },
        {
            "name_in": "simple_case_folding",
            "name_out": "simple_case_folding",
            "char_property": "scf",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_mapped_codepoint(char["simple_case_folding"])
            if "simple_case_folding" in char
            else "",
        },
    ],
    enum.CharPropertyGroup.Script: [
        {
            "name_in": "script",
            "name_out": "script",
            "char_property": "sc",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: enum.ScriptCode(char["script"]).display_name
            if "script" in char
            else enum.ScriptCode.UNKNOWN.display_name,
        },
        {
            "name_in": "script_extensions",
            "name_out": "script_extensions",
            "char_property": "scx",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: get_script_extensions(char["script_extensions"])
            if "script_extensions" in char
            else [enum.ScriptCode.UNKNOWN.display_name],
        },
    ],
    enum.CharPropertyGroup.Hangul: [
        {
            "name_in": "hangul_syllable_type",
            "name_out": "hangul_syllable_type",
            "char_property": "hst",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: enum.HangulSyllableType(char["hangul_syllable_type"]).display_name
            if "hangul_syllable_type" in char
            else enum.HangulSyllableType.NOT_APPLICABLE.display_name,
        },
    ],
    enum.CharPropertyGroup.Indic: [
        {
            "name_in": "indic_syllabic_category",
            "name_out": "indic_syllabic_category",
            "char_property": "InSC",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: char["indic_syllabic_category"] if "indic_syllabic_category" in char else "",
        },
        {
            "name_in": "indic_matra_category",
            "name_out": "indic_matra_category",
            "char_property": "NA",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: char["indic_matra_category"] if "indic_matra_category" in char else "",
        },
        {
            "name_in": "indic_positional_category",
            "name_out": "indic_positional_category",
            "char_property": "InPC",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: char["indic_positional_category"]
            if "indic_positional_category" in char
            else "",
        },
    ],
    enum.CharPropertyGroup.Function_and_Graphic: [
        {
            "name_in": "dash",
            "name_out": "dash",
            "char_property": "Dash",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["dash"]) if "dash" in char else False,
        },
        {
            "name_in": "hyphen",
            "name_out": "hyphen",
            "char_property": "Hyphen",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["hyphen"]) if "hyphen" in char else False,
        },
        {
            "name_in": "quotation_mark",
            "name_out": "quotation_mark",
            "char_property": "QMark",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["quotation_mark"]) if "quotation_mark" in char else False,
        },
        {
            "name_in": "terminal_punctuation",
            "name_out": "terminal_punctuation",
            "char_property": "Term",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["terminal_punctuation"])
            if "terminal_punctuation" in char
            else False,
        },
        {
            "name_in": "sentence_terminal",
            "name_out": "sentence_terminal",
            "char_property": "STerm",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["sentence_terminal"]) if "sentence_terminal" in char else False,
        },
        {
            "name_in": "diacritic",
            "name_out": "diacritic",
            "char_property": "Dia",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["diacritic"]) if "diacritic" in char else False,
        },
        {
            "name_in": "extender",
            "name_out": "extender",
            "char_property": "Ext",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["extender"]) if "extender" in char else False,
        },
        {
            "name_in": "soft_dotted",
            "name_out": "soft_dotted",
            "char_property": "PCM",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["soft_dotted"]) if "soft_dotted" in char else False,
        },
        {
            "name_in": "alphabetic",
            "name_out": "alphabetic",
            "char_property": "SD",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["alphabetic"]) if "alphabetic" in char else False,
        },
        {
            "name_in": "math",
            "name_out": "math",
            "char_property": "OAlpha",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["math"]) if "math" in char else False,
        },
        {
            "name_in": "hex_digit",
            "name_out": "hex_digit",
            "char_property": "OMath",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["hex_digit"]) if "hex_digit" in char else False,
        },
        {
            "name_in": "ascii_hex_digit",
            "name_out": "ascii_hex_digit",
            "char_property": "Hex",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["ascii_hex_digit"]) if "ascii_hex_digit" in char else False,
        },
        {
            "name_in": "default_ignorable_code_point",
            "name_out": "default_ignorable_code_point",
            "char_property": "AHex",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["default_ignorable_code_point"])
            if "default_ignorable_code_point" in char
            else False,
        },
        {
            "name_in": "logical_order_exception",
            "name_out": "logical_order_exception",
            "char_property": "ODI",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["logical_order_exception"])
            if "logical_order_exception" in char
            else False,
        },
        {
            "name_in": "prepended_concatenation_mark",
            "name_out": "prepended_concatenation_mark",
            "char_property": "LOE",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["prepended_concatenation_mark"])
            if "prepended_concatenation_mark" in char
            else False,
        },
        {
            "name_in": "white_space",
            "name_out": "white_space",
            "char_property": "WSpace",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["white_space"]) if "white_space" in char else False,
        },
        {
            "name_in": "vertical_orientation",
            "name_out": "vertical_orientation",
            "char_property": "vo",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: enum.VerticalOrientationType(char["vertical_orientation"]).display_name
            if "vertical_orientation" in char
            else get_default_vo_display_name(char["codepoint_dec"]),
        },
        {
            "name_in": "regional_indicator",
            "name_out": "regional_indicator",
            "char_property": "RI",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["regional_indicator"]) if "regional_indicator" in char else False,
        },
    ],
    enum.CharPropertyGroup.Emoji: [
        {
            "name_in": "emoji",
            "name_out": "emoji",
            "char_property": "Emoji",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["emoji"]) if "emoji" in char else False,
        },
        {
            "name_in": "emoji_presentation",
            "name_out": "emoji_presentation",
            "char_property": "EPres",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["emoji_presentation"]) if "emoji_presentation" in char else False,
        },
        {
            "name_in": "emoji_modifier",
            "name_out": "emoji_modifier",
            "char_property": "EMod",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["emoji_modifier"]) if "emoji_modifier" in char else False,
        },
        {
            "name_in": "emoji_modifier_base",
            "name_out": "emoji_modifier_base",
            "char_property": "EBase",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["emoji_modifier_base"])
            if "emoji_modifier_base" in char
            else False,
        },
        {
            "name_in": "emoji_component",
            "name_out": "emoji_component",
            "char_property": "EComp",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["emoji_component"]) if "emoji_component" in char else False,
        },
        {
            "name_in": "extended_pictographic",
            "name_out": "extended_pictographic",
            "char_property": "ExtPict",
            "db_required": True,
            "db_column": True,
            "response_value": lambda char: bool(char["extended_pictographic"])
            if "extended_pictographic" in char
            else False,
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


def get_default_age(codepoint: int) -> str:
    block = cached_data.get_unicode_block_containing_codepoint(codepoint)
    return "1.1" if block.plane and block.plane.abbreviation == "BMP" else "2.0" if block.plane else ""


def get_default_general_category_display_name(codepoint: int) -> str:
    general_category = (
        enum.GeneralCategory.SURROGATE
        if cached_data.codepoint_is_surrogate(codepoint)
        else enum.GeneralCategory.PRIVATE_USE
        if cached_data.codepoint_is_private_use
        else enum.GeneralCategory.UNASSIGNED
    )
    return general_category.display_name


def get_default_bidi_class_display_name(codepoint: int) -> str:
    bidi_class = (
        enum.BidirectionalClass.RIGHT_TO_LEFT
        if codepoint in DEFAULT_BC_R_CODEPOINTS
        else enum.BidirectionalClass.ARABIC_LETTER
        if codepoint in DEFAULT_BC_AL_CODEPOINTS
        else enum.BidirectionalClass.EUROPEAN_TERMINATOR
        if codepoint in DEFAULT_BC_ET_CODEPOINTS
        else enum.BidirectionalClass.LEFT_TO_RIGHT
    )
    return bidi_class.display_name


def get_default_eaw_display_name(codepoint: int) -> str:
    block = cached_data.get_unicode_block_containing_codepoint(codepoint)
    eaw = (
        enum.EastAsianWidthType.EAST_ASIAN_AMBIGUOUS
        if cached_data.codepoint_is_private_use
        else enum.EastAsianWidthType.EAST_ASIAN_WIDE
        if block.id in ALL_CJK_IDEOGRAPH_BLOCK_IDS
        else enum.EastAsianWidthType.NEUTRAL_NOT_EAST_ASIAN
    )
    return eaw.display_name


def get_default_vo_display_name(codepoint: int) -> str:
    block = cached_data.get_unicode_block_containing_codepoint(codepoint)
    vo_type = (
        enum.VerticalOrientationType.UPRIGHT
        if block.plane and block.plane.number in DEFAULT_VO_U_PLANE_NUMBERS or block.id in DEFAULT_VO_U_BLOCK_IDS
        else enum.VerticalOrientationType.ROTATED
    )
    return vo_type.display_name


def get_mapped_codepoint(codepoint_hex: str) -> str:
    return f"{chr(int(codepoint_hex, 16))} (U+{int(codepoint_hex, 16):04X})" if codepoint_hex else ""


def get_script_extensions(value: str) -> list[str]:
    return [enum.ScriptCode.from_code(script).display_name for script in value.split(" ")]
