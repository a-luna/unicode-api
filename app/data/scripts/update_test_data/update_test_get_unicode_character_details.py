import json
from typing import Any

from app.config.api_settings import UnicodeApiSettings
from app.core.result import Result
from app.data.scripts.update_test_data.util import pythonize_that_json
from app.db.engine import engine
from app.db.procs.get_char_details import get_character_properties
from app.schemas.enums import CharPropertyGroup
from app.schemas.util import to_lower_camel

# fmt: off
TEST_CHARS = [
#   Char        Codepoint   Name                                             Test Notes
    "\x17",     # U+0017    END OF TRANSMISSION BLOCK                        (Control Character)
    "(",        # U+0028    LEFT PARENTHESIS                                 (Punctuation)
    "∑",        # U+2211    N-ARY SUMMATION                                  (Math Symbol)
    "㑢",       # U+3462    CJK UNIFIED IDEOGRAPH-3462                       (CJK Ideograph)
    "穩",       # U+7A69    CJK UNIFIED IDEOGRAPH-7A69                       (CJK Ideograph w/ variants)
    "范",       # U+8303    CJK UNIFIED IDEOGRAPH-8303                       (CJK Ideograph w/ multiple values for totalStrokes)     # noqa: E501
    # "\uda92",   # U+DA92    <surrogate-DA92>                                 (High-Surrogate)                                     # noqa: ERA001, E501
    # "\udddd",   # U+DDDD    <surrogate-DDDD>                                 (Low Surrogate)                                      # noqa: ERA001, E501
    "﨑",       # U+FA11    CJK COMPATIBILITY IDEOGRAPH-FA11                 (CJK Compatibility Ideograph)
    "\uf800",   # U+F800    <private-use-F800>                               (Private Use)
    "\ufffe",   # U+FFFE    <noncharacter-FFFE>                              (Noncharacter)
    "𑿀",      # U+11FC0   TAMIL FRACTION ONE THREE-HUNDRED-AND-TWENTIETH   (Numeric with fractional value)
    "𘂾",        # U+180BE   TANGUT IDEOGRAPH-180BE                           (Tangut Ideograph)
    "𘠠",       # U+18820   TANGUT COMPONENT-033                             (Tangut Component)
    "🇦",      # U+1F1E6   REGIONAL INDICATOR SYMBOL LETTER A               (emoji=True, extendedPictographic=False)
    "🐍",      # U+1F40D   SNAKE                                            (emoji=True, extendedPictographic=True)
]
# fmt: on

INT_TO_STR_PROP_NAMES = ["accounting_numeric", "primary_numeric", "other_numeric"]
INT_ALWAYS_PROP_VALUES = ["total_strokes", "total_strokes", "utf8_dec_bytes", "utf16_dec_bytes", "utf32_dec_bytes"]

IMPORT_STATEMENT = "from app.schemas.enums import CharPropertyGroup\n\n"

STATIC_CONTENT = """
def get_all_prop_names():
    prop_names = [prop_group.normalized for prop_group in CharPropertyGroup if prop_group != CharPropertyGroup.NONE]
    prop_aliases = [prop_group.short_alias for prop_group in CharPropertyGroup if prop_group.has_alias]
    return list(set(prop_names + prop_aliases))


ALL_PROP_GROUP_NAMES = get_all_prop_names()

INVALID_PROP_GROUP_NAMES = {
    "detail": "3 values provided for the 'show_props' parameter are invalid: ['foo', 'bar', 'baz']"
}
"""


def update_test_get_unicode_character_details(settings: UnicodeApiSettings):
    data_concise = {char: get_char_props(char, verbose=False) for char in TEST_CHARS}
    data_verbose = {char: get_char_props(char, verbose=True) for char in TEST_CHARS}
    update_test_data_file(settings, data_concise, data_verbose)
    return Result.Ok()


def get_char_props(char: str, verbose: bool) -> dict[str, Any]:
    char_props = get_character_properties(engine, ord(char), [CharPropertyGroup.ALL], verbose)
    return format_character_properties(char_props)


def format_character_properties(char_details: dict[str, Any]) -> dict[str, Any]:
    return {
        to_lower_camel(prop_name): format_prop_value(prop_name, prop_value)
        for prop_name, prop_value in char_details.items()
    }


def format_prop_value(prop_name: str, prop_value: Any) -> Any:
    if isinstance(prop_value, bool):
        return prop_value
    if prop_name in INT_TO_STR_PROP_NAMES and isinstance(prop_value, int):
        return str(prop_value)
    if (
        prop_name not in INT_ALWAYS_PROP_VALUES
        and isinstance(prop_value, list)
        and all(isinstance(item, int) for item in prop_value)
    ):
        return [str(item) for item in prop_value]
    return prop_value


def update_test_data_file(
    settings: UnicodeApiSettings, data_concise: dict[str, Any], data_verbose: dict[str, Any]
) -> str:
    test_data = construct_test_data_file(data_concise, data_verbose)
    test_data_file = (
        settings.TESTS_FOLDER.joinpath("test_character_endpoints")
        .joinpath("test_get_unicode_character_details")
        .joinpath("data.py")
    )
    test_data_file.write_text(test_data, encoding="utf-8")


def construct_test_data_file(data_concise: dict[str, Any], data_verbose: dict[str, Any]) -> str:
    json_concise = json.dumps(data_concise, indent=4, ensure_ascii=False)
    json_verbose = json.dumps(data_verbose, indent=4, ensure_ascii=False)
    return (
        IMPORT_STATEMENT
        + f"CHARACTER_PROPERTIES = {pythonize_that_json(json_concise)}\n\n"
        + f"VERBOSE_CHARACTER_PROPERTIES = {pythonize_that_json(json_verbose)}\n\n"
        + STATIC_CONTENT
    )
