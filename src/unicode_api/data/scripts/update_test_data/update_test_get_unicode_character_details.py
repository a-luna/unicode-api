import json
from typing import Any

from unicode_api.api.api_v1.endpoints.codepoints import get_unicode_character_at_codepoint
from unicode_api.config.api_settings import UnicodeApiSettings
from unicode_api.core.result import Result
from unicode_api.data.scripts.update_test_data.util import convert_json_to_python_literals
from unicode_api.db.session import DBSession
from unicode_api.enums.property_group import CharPropertyGroup
from unicode_api.models.util import to_lower_camel

# fmt: off
TEST_CHARS = [
#   Char        Codepoint   Name                                             Test Notes
#   ----------  ----------  -----------------------------------------------  -----------------------------------------------------  # noqa: E501
    "\x17",     # U+0017    END OF TRANSMISSION BLOCK                        (Control Character)
    "(",        # U+0028    LEFT PARENTHESIS                                 (Punctuation)
    "∑",        # U+2211    N-ARY SUMMATION                                  (Math Symbol)
    "二",       # U+7A69    CJK UNIFIED IDEOGRAPH-4E8C                       (CJK Ideograph w/ variants and numeric value)          # noqa: E501
    "范",       # U+8303    CJK UNIFIED IDEOGRAPH-8303                       (CJK Ideograph w/ multiple values for totalStrokes)    # noqa: E501
    "﨑",       # U+FA11    CJK COMPATIBILITY IDEOGRAPH-FA11                 (CJK Compatibility Ideograph)
    "\uf800",   # U+F800    <private-use-F800>                               (Private Use)
    "\ufffe",   # U+FFFE    <noncharacter-FFFE>                              (Noncharacter)
    "𑿀",      # U+11FC0   TAMIL FRACTION ONE THREE-HUNDRED-AND-TWENTIETH   (Numeric with fractional value)
    "𘂾",       # U+180BE   TANGUT IDEOGRAPH-180BE                           (Tangut Ideograph)
    "𘠠",       # U+18820   TANGUT COMPONENT-033                             (Tangut Component)
    "🇦",      # U+1F1E6   REGIONAL INDICATOR SYMBOL LETTER A               (emoji=True, extendedPictographic=False)
    "🐍",      # U+1F40D   SNAKE                                            (emoji=True, extendedPictographic=True)
]
# fmt: on

INT_TO_STR_PROP_NAMES = ["accounting_numeric", "primary_numeric", "other_numeric"]
NUM_ALWAYS_PROP_VALUES = [
    "numeric_value_parsed",
    "total_strokes",
    "utf8_dec_bytes",
    "utf16_dec_bytes",
    "utf32_dec_bytes",
]

STATIC_CONTENT = """
INVALID_PROP_GROUP_NAMES = {
    "detail": "3 values provided for the 'show_props' parameter are invalid: ['foo', 'bar', 'baz']"
}
"""


def update_test_get_unicode_character_details(db_ctx: DBSession, settings: UnicodeApiSettings) -> Result[None]:
    data_concise = {char: get_char_props(db_ctx, char, verbose=False) for char in TEST_CHARS}
    data_verbose = {char: get_char_props(db_ctx, char, verbose=True) for char in TEST_CHARS}
    test_data = construct_test_data_file(data_concise, data_verbose)
    test_data_file = (
        settings.tests_folder.joinpath("test_character_endpoints")
        .joinpath("test_get_unicode_character_details")
        .joinpath("data.py")
    )
    test_data_file.write_text(test_data, encoding="utf-8")
    return Result[None].Ok()


def get_char_props(db_ctx: DBSession, char: str, verbose: bool) -> dict[str, Any]:
    char_props = get_unicode_character_at_codepoint(
        db_ctx=db_ctx,
        codepoint=f"{ord(char):04X}",
        show_props=[str(CharPropertyGroup.ALL)],
        verbose=verbose,
    )
    return format_character_properties(char_props)


def format_character_properties(char_details: dict[str, Any]) -> dict[str, Any]:
    return {
        to_lower_camel(prop_name): format_prop_value(prop_name, prop_value)
        for prop_name, prop_value in char_details.items()
    }


def format_prop_value(
    prop_name: str, prop_value: bool | int | str | list[int]
) -> bool | int | str | list[str] | list[int]:
    if isinstance(prop_value, bool):
        return prop_value
    if prop_name in INT_TO_STR_PROP_NAMES and isinstance(prop_value, int):
        return str(prop_value)
    if prop_name not in NUM_ALWAYS_PROP_VALUES and isinstance(prop_value, list):
        return [str(item) for item in prop_value]
    return prop_value


def construct_test_data_file(data_concise: dict[str, Any], data_verbose: dict[str, Any]) -> str:
    json_concise = json.dumps(data_concise, indent=4, ensure_ascii=False)
    json_verbose = json.dumps(data_verbose, indent=4, ensure_ascii=False)
    return (
        "# fmt: off\n"
        f"CHARACTER_PROPERTIES = {convert_json_to_python_literals(json_concise)}\n\n"
        + f"VERBOSE_CHARACTER_PROPERTIES = {convert_json_to_python_literals(json_verbose)}\n\n"
        + STATIC_CONTENT
        + "# fmt: on\n"
    )
