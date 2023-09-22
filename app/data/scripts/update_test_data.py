import json
from typing import Any

from app.core.config import get_settings
from app.core.result import Result
from app.db.engine import engine
from app.db.get_char_details import get_character_properties
from app.schemas.enums.property_group import CharPropertyGroup
from app.schemas.util import to_lower_camel

TEST_CHARS = ["\x17", "(", "∑", "㑢", "穩", "范", "𑿀", "\uf800", "\ufffe", "🇦", "🐍"]

INT_TO_STR_PROP_NAMES = ["accounting_numeric", "primary_numeric", "other_numeric"]

TEST_DATA_FILE = (
    get_settings()
    .TESTS_FOLDER.joinpath("test_character_endpoints")
    .joinpath("test_get_unicode_character_details")
    .joinpath("data.py")
)

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


def update_test_data():
    data_concise = {}
    data_verbose = {}
    for char in TEST_CHARS:
        concise_details = get_character_properties(engine, ord(char), [CharPropertyGroup.ALL], False)
        data_concise[char] = format_character_properties(concise_details)
        verbose_details = get_character_properties(engine, ord(char), [CharPropertyGroup.ALL], True)
        data_verbose[char] = format_character_properties(verbose_details)

    character_properties = json.dumps(data_concise, indent=4, ensure_ascii=False)
    verbose_character_properties = json.dumps(data_verbose, indent=4, ensure_ascii=False)

    data_py = (
        "from app.schemas.enums import CharPropertyGroup\n\n"
        + f"CHARACTER_PROPERTIES = {pythonize_that_json(character_properties)}\n\n"
        + f"VERBOSE_CHARACTER_PROPERTIES = {pythonize_that_json(verbose_character_properties)}\n\n"
        + STATIC_CONTENT
    )
    TEST_DATA_FILE.write_text(data_py, encoding="utf-8")
    return Result.Ok()


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
        prop_name != "total_strokes"
        and isinstance(prop_value, list)
        and all(isinstance(item, int) for item in prop_value)
    ):
        return [str(item) for item in prop_value]
    return prop_value


def pythonize_that_json(json: str) -> str:
    return json.replace("null", "None").replace("false", "False").replace("true", "True")


if __name__ == "__main__":
    update_test_data()
