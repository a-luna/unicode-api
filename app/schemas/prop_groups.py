from app.core.config import settings
from app.data.cache import cached_data
from app.data.encoding import (
    get_html_entities,
    get_uri_encoded_value,
    get_utf8_hex_bytes,
    get_utf8_value,
    get_utf16_hex_bytes,
    get_utf16_value,
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
    JoiningClass,
    LineBreakType,
    NumericType,
    ScriptCode,
    VerticalOrientationType,
)

CHARACTER_PROPERTY_GROUPS = {
    CharPropertyGroup.BASIC: [
        {
            "name_in": "character",
            "name_out": "character",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: chr(char["codepoint_dec"]),
        },
        {
            "name_in": "codepoint_dec",
            "name_out": "codepoint_dec",
            "char_property": "",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "codepoint",
            "name_out": "codepoint",
            "char_property": "cp",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: f'U+{char["codepoint_dec"]:04X}',
        },
        {
            "name_in": "name",
            "name_out": "name",
            "char_property": "na",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "block_id",
            "name_out": "block",
            "char_property": "",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: cached_data.block_id_map[char["block_id"]]["name"],
        },
        {
            "name_in": "plane_number",
            "name_out": "plane",
            "char_property": "",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: cached_data.plane_number_map[char["plane_number"]]["abbreviation"],
        },
        {
            "name_in": "age",
            "name_out": "age",
            "char_property": "age",
            "db_column": True,
            "responsify": False,
        },  # version in which the codepoint was assigned
        {
            "name_in": "general_category",
            "name_out": "general_category",
            "char_property": "gc",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: GeneralCategory(char["general_category"]).display_name
            # "response_value": lambda char: char.general_category.display_name,
        },  # general category, see https://www.unicode.org/reports/tr44/#General_Category_Values
        {
            "name_in": "link",
            "name_out": "link",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: f'{settings.API_VERSION}/characters/{get_uri_encoded_value(chr(char["codepoint_dec"]))}',
        },
    ],
    CharPropertyGroup.COMBINING: [
        {
            "name_in": "combining_class",
            "name_out": "combining_class",
            "char_property": "ccc",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: CombiningClassCategory(char["combining_class"]).display_name,
        },  # combining class, see https://www.unicode.org/reports/tr44/#Canonical_Combining_Class_Values. Specifies, with a numeric code, how a diacritic mark is positioned with respect to the base character. This is used in the Canonical Ordering Algorithm and in normalization. The order of the numbers is significant, but not the absolute values.
    ],
    CharPropertyGroup.BIDIRECTIONALITY: [
        {
            "name_in": "bidirectional_class",
            "name_out": "bidirectional_class",
            "char_property": "bc",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: BidirectionalClass(char["bidirectional_class"]).display_name,
        },  # bidirectional class, see https://www.unicode.org/reports/tr44/#Bidi_Class_Values
        {
            "name_in": "bidirectional_is_mirrored",
            "name_out": "bidirectional_is_mirrored",
            "char_property": "Bidi_M",
            "db_column": True,
            "responsify": False,
        },  # bidirectional mirrored, boolean value
        {
            "name_in": "bidirectional_mirroring_glyph",
            "name_out": "bidirectional_mirroring_glyph",
            "char_property": "bmg",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: display_mapped_codepoint(char["bidirectional_mirroring_glyph"]),
        },  # bidirectional mirroring glyph, the codepoint of the character whose glyph is typically a mirrored image of the glyph for the current character
        {
            "name_in": "bidirectional_control",
            "name_out": "bidirectional_control",
            "char_property": "Bidi_C",
            "db_column": True,
            "responsify": False,
        },  # bidirectional control, indicates whether the character has a special function in the bidirectional algorithm
        {
            "name_in": "paired_bracket_type",
            "name_out": "paired_bracket_type",
            "char_property": "bpt",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: BidirectionalBracketType(char["paired_bracket_type"]).display_name,
        },  # bidirectional paired bracket type, see https://www.unicode.org/Public/15.0.0/ucd/BidiBrackets.txt
        {
            "name_in": "paired_bracket_property",
            "name_out": "paired_bracket_property",
            "char_property": "bpb",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: display_mapped_codepoint(char["paired_bracket_property"]),
        },  # bidirectional paired bracket property, see https://www.unicode.org/Public/15.0.0/ucd/BidiBrackets.txt
    ],
    CharPropertyGroup.DECOMPOSITION: [
        {
            "name_in": "decomposition_type",
            "name_out": "decomposition_type",
            "char_property": "dt",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: DecompositionType(char["decomposition_type"]).display_name,
        },
        {
            "name_in": "decomposition_mapping",
            "name_out": "decomposition_mapping",
            "char_property": "dm",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: get_decomposition_mapping(char["decomposition_mapping"]),
        },
        {
            "name_in": "composition_exclusion",
            "name_out": "composition_exclusion",
            "char_property": "CE",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "full_composition_exclusion",
            "name_out": "full_composition_exclusion",
            "char_property": "Comp_Ex",
            "db_column": True,
            "responsify": False,
        },
    ],
    CharPropertyGroup.NUMERIC: [
        {
            "name_in": "numeric_type",
            "name_out": "numeric_type",
            "char_property": "nt",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: NumericType(char["numeric_type"]).display_name,
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
    CharPropertyGroup.JOINING: [
        {
            "name_in": "joining_class",
            "name_out": "joining_class",
            "char_property": "jt",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: JoiningClass(char["joining_class"]).display_name,
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
    CharPropertyGroup.LINEBREAK: [
        {
            "name_in": "line_break",
            "name_out": "line_break",
            "char_property": "lb",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: LineBreakType(char["line_break"]).display_name,
        },
    ],
    CharPropertyGroup.EAST_ASIAN_WIDTH: [
        {
            "name_in": "east_asian_width",
            "name_out": "east_asian_width",
            "char_property": "ea",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: EastAsianWidthType(char["east_asian_width"]).display_name,
        },
    ],
    CharPropertyGroup.CASE: [
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
            "response_value": lambda char: display_mapped_codepoint(char["simple_uppercase_mapping"]),
        },
        {
            "name_in": "simple_lowercase_mapping",
            "name_out": "simple_lowercase_mapping",
            "char_property": "slc",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: display_mapped_codepoint(char["simple_lowercase_mapping"]),
        },
        {
            "name_in": "simple_titlecase_mapping",
            "name_out": "simple_titlecase_mapping",
            "char_property": "stc",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: display_mapped_codepoint(char["simple_titlecase_mapping"]),
        },
        {
            "name_in": "simple_case_folding",
            "name_out": "simple_case_folding",
            "char_property": "scf",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: display_mapped_codepoint(char["simple_case_folding"]),
        },
        {
            "name_in": "other_uppercase",
            "name_out": "other_uppercase",
            "char_property": "OUpper",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "other_lowercase",
            "name_out": "other_lowercase",
            "char_property": "OLower",
            "db_column": True,
            "responsify": False,
        },
        {
            "name_in": "other_uppercase_mapping",
            "name_out": "other_uppercase_mapping",
            "char_property": "uc",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: display_mapped_codepoint(char["other_uppercase_mapping"]),
        },
        {
            "name_in": "other_lowercase_mapping",
            "name_out": "other_lowercase_mapping",
            "char_property": "lc",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: display_mapped_codepoint(char["other_lowercase_mapping"]),
        },
        {
            "name_in": "other_titlecase_mapping",
            "name_out": "other_titlecase_mapping",
            "char_property": "tc",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: display_mapped_codepoint(char["other_titlecase_mapping"]),
        },
        {
            "name_in": "other_case_folding",
            "name_out": "other_case_folding",
            "char_property": "cf",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: display_mapped_codepoint(char["other_case_folding"]),
        },
    ],
    CharPropertyGroup.SCRIPT: [
        {
            "name_in": "script",
            "name_out": "script",
            "char_property": "sc",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: ScriptCode(char["script"]).display_name,
        },
        {
            "name_in": "script_extension",
            "name_out": "script_extension",
            "char_property": "scx",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: get_script_extension(char["script_extension"]),
        },
    ],
    CharPropertyGroup.HANGUL: [
        {
            "name_in": "hangul_syllable_type",
            "name_out": "hangul_syllable_type",
            "char_property": "hst",
            "db_column": True,
            "responsify": True,
            "response_value": lambda char: HangulSyllableType(char["hangul_syllable_type"]).display_name,
        },
        {
            "name_in": "jamo_short_name",
            "name_out": "jamo_short_name",
            "char_property": "JSN",
            "db_column": True,
            "responsify": False,
        },
    ],
    CharPropertyGroup.INDIC: [
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
    CharPropertyGroup.FUNCTION_AND_GRAPHIC: [
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
            "name_in": "other_alphabetic",
            "name_out": "other_alphabetic",
            "char_property": "Alpha",
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
            "name_in": "other_math",
            "name_out": "other_math",
            "char_property": "Math",
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
            "name_in": "other_default_ignorable_code_point",
            "name_out": "other_default_ignorable_code_point",
            "char_property": "DI",
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
            "response_value": lambda char: VerticalOrientationType(char["vertical_orientation"]).display_name,
        },
        {
            "name_in": "regional_indicator",
            "name_out": "regional_indicator",
            "char_property": "RI",
            "db_column": True,
            "responsify": False,
        },
    ],
    CharPropertyGroup.EMOJI: [
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
    CharPropertyGroup.ENCODED_STRINGS: [
        {
            "name_in": "utf8",
            "name_out": "utf8",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: get_utf8_value(chr(char["codepoint_dec"])),
        },
        {
            "name_in": "utf16",
            "name_out": "utf16",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: get_utf16_value(chr(char["codepoint_dec"])),
        },
        {
            "name_in": "utf32",
            "name_out": "utf32",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: get_utf32_value(chr(char["codepoint_dec"])),
        },
        {
            "name_in": "uri_encoded",
            "name_out": "uri_encoded",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: get_uri_encoded_value(chr(char["codepoint_dec"])),
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
    CharPropertyGroup.ENCODED_BYTES: [
        {
            "name_in": "utf8_bytes",
            "name_out": "utf8_bytes",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: get_utf8_hex_bytes(chr(char["codepoint_dec"])),
        },
        {
            "name_in": "utf16_bytes",
            "name_out": "utf16_bytes",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: get_utf16_hex_bytes(chr(char["codepoint_dec"])),
        },
        {
            "name_in": "utf32_bytes",
            "name_out": "utf32_bytes",
            "char_property": "",
            "db_column": False,
            "responsify": True,
            "response_value": lambda char: get_utf32_hex_bytes(chr(char["codepoint_dec"])),
        },
    ],
}


def display_mapped_codepoint(codepoint_hex: str) -> str:
    return f"{chr(int(codepoint_hex, 16))} (U+{int(codepoint_hex, 16):04X})" if codepoint_hex else ""


def get_decomposition_mapping(value: str) -> list[str]:
    return (
        [display_mapped_codepoint(codepoint_hex) for codepoint_hex in value.split(" ")]
        if " " in value
        else [display_mapped_codepoint(value)]
    )


def get_script_extension(value: str) -> list[str]:
    return [ScriptCode.from_code(script).display_name for script in value.split(" ")]


def get_all_db_columns_in_group(prop_group: CharPropertyGroup) -> list[str]:
    return [prop["name_in"] for prop in CHARACTER_PROPERTY_GROUPS[prop_group] if prop["db_column"]]


def update_character_properties(char_dict: dict[str, bool | int | str], prop_group: CharPropertyGroup):
    updated_dict = {}
    all_prop_names = [prop_map["name_in"] for prop_map in CHARACTER_PROPERTY_GROUPS[prop_group]]
    for prop_name in all_prop_names:
        prop_map = [map for map in CHARACTER_PROPERTY_GROUPS[prop_group] if map["name_in"] == prop_name][0]
        updated_dict[prop_map["name_out"]] = (
            prop_map["response_value"](char_dict)
            if prop_map["responsify"]
            else char_dict[prop_name]
            if prop_name in char_dict
            else None
        )
    return updated_dict
