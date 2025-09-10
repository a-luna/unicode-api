import json

from fastapi import HTTPException

from unicode_api.api.api_v1.endpoints.codepoints import get_unicode_character_at_codepoint
from unicode_api.config.api_settings import UnicodeApiSettings
from unicode_api.core.result import Result
from unicode_api.core.util import convert_keys_to_camel_case
from unicode_api.data.scripts.update_test_data.util import convert_json_to_python_literals
from unicode_api.db.session import DBSession


def update_test_get_unicode_character_at_codepoint(db_ctx: DBSession, settings: UnicodeApiSettings) -> Result[None]:
    test_data = (
        f"CODEPOINT_24AF_RAW_HEX = {get_character_at_codepoint_raw_hex(db_ctx)}\n"
        f"CODEPOINT_24AF_WITH_PREFIX_1 = {get_character_at_codepoint_with_prefix_1(db_ctx)}\n"
        f"CODEPOINT_24AF_WITH_PREFIX_2 = {get_character_at_codepoint_with_prefix_2(db_ctx)}\n"
        f"INVALID_HEX_DIGIT_1 = {get_character_at_codepoint_invalid_single_hex_digit(db_ctx)}\n"
        f"INVALID_HEX_DIGIT_2 = {get_character_at_codepoint_invalid_multiple_hex_digits(db_ctx)}\n"
        f"INVALID_LEADING_ZEROS = {get_character_at_codepoint_invalid_leading_zeros(db_ctx)}\n"
        f"INVALID_OUT_OF_RANGE = {get_character_at_codepoint_invalid_out_of_range(db_ctx)}\n"
        f"INVALID_PROP_GROUP_NAME = {get_character_at_codepoint_invalid_prop_name(db_ctx)}\n"
    )
    test_data_file = (
        settings.tests_folder.joinpath("test_codepoint_endpoints")
        .joinpath("test_get_unicode_character_at_codepoint")
        .joinpath("data.py")
    )
    test_data_file.write_text(test_data, encoding="utf-8")
    return Result[None].Ok()


def get_character_at_codepoint_raw_hex(db_ctx: DBSession):
    char_data = get_unicode_character_at_codepoint(db_ctx, codepoint="24AF", show_props=[], verbose=None)
    return convert_json_to_python_literals(
        json.dumps(convert_keys_to_camel_case(char_data), indent=4, ensure_ascii=False)
    )


def get_character_at_codepoint_with_prefix_1(db_ctx: DBSession):
    char_data = get_unicode_character_at_codepoint(db_ctx, codepoint="U+24AF", show_props=["basic"], verbose=True)
    return convert_json_to_python_literals(
        json.dumps(convert_keys_to_camel_case(char_data), indent=4, ensure_ascii=False)
    )


def get_character_at_codepoint_with_prefix_2(db_ctx: DBSession):
    char_data = get_unicode_character_at_codepoint(db_ctx, codepoint="0x24AF", show_props=["all"], verbose=None)
    return convert_json_to_python_literals(
        json.dumps(convert_keys_to_camel_case(char_data), indent=4, ensure_ascii=False)
    )


def get_character_at_codepoint_invalid_single_hex_digit(db_ctx: DBSession):
    result = get_error_detail(db_ctx, codepoint="0x24AZ", show_props=[], verbose=None)
    return result.value if result.success and result.value else ""


def get_character_at_codepoint_invalid_multiple_hex_digits(db_ctx: DBSession):
    result = get_error_detail(db_ctx, codepoint="maccaroni", show_props=[], verbose=None)
    return result.value if result.success and result.value else ""


def get_character_at_codepoint_invalid_leading_zeros(db_ctx: DBSession):
    result = get_error_detail(db_ctx, codepoint="U+72", show_props=[], verbose=None)
    return result.value if result.success and result.value else ""


def get_character_at_codepoint_invalid_out_of_range(db_ctx: DBSession):
    result = get_error_detail(db_ctx, codepoint="U+1234567", show_props=[], verbose=None)
    return result.value if result.success and result.value else ""


def get_character_at_codepoint_invalid_prop_name(db_ctx: DBSession):
    result = get_error_detail(db_ctx, codepoint="U+0072", show_props=["max"], verbose=None)
    return result.value if result.success and result.value else ""


def get_formatted_character_details(
    db_ctx: DBSession, codepoint: str, show_props: list[str], verbose: bool | None = None
):
    char_data = get_unicode_character_at_codepoint(db_ctx, codepoint, show_props, verbose)
    char_data = convert_keys_to_camel_case(char_data)
    return convert_json_to_python_literals(json.dumps(char_data, indent=4, ensure_ascii=False))


def get_error_detail(
    db_ctx: DBSession, codepoint: str, show_props: list[str], verbose: bool | None = None
) -> Result[str]:
    try:
        _ = get_unicode_character_at_codepoint(db_ctx, codepoint, show_props, verbose)
        return Result[str].Fail("Expected an HTTPException to be raised")
    except HTTPException as ex:
        response = convert_json_to_python_literals(json.dumps({"detail": ex.detail}, indent=4, ensure_ascii=False))
        return Result[str].Ok(response)
