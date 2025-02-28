import json

from fastapi import HTTPException

from app.api.api_v1.endpoints.codepoints import get_unicode_character_at_codepoint
from app.config.api_settings import UnicodeApiSettings
from app.core.result import Result
from app.data.scripts.update_test_data.util import format_response_property_names, pythonize_that_json
from app.db.session import DBSession


def update_test_get_unicode_character_at_codepoint(db_ctx: DBSession, settings: UnicodeApiSettings):
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
        settings.TESTS_FOLDER.joinpath("test_codepoint_endpoints")
        .joinpath("test_get_unicode_character_at_codepoint")
        .joinpath("data.py")
    )
    test_data_file.write_text(test_data, encoding="utf-8")
    return Result.Ok()


def get_character_at_codepoint_raw_hex(db_ctx: DBSession):
    response = get_unicode_character_at_codepoint(db_ctx, codepoint="24AF", show_props=[], verbose=None)
    return pythonize_that_json(json.dumps(format_response_property_names(response), indent=4, ensure_ascii=False))


def get_character_at_codepoint_with_prefix_1(db_ctx: DBSession):
    response = get_unicode_character_at_codepoint(db_ctx, codepoint="U+24AF", show_props=["basic"], verbose=True)
    return pythonize_that_json(json.dumps(format_response_property_names(response), indent=4, ensure_ascii=False))


def get_character_at_codepoint_with_prefix_2(db_ctx: DBSession):
    response = get_unicode_character_at_codepoint(db_ctx, codepoint="0x24AF", show_props=["all"], verbose=None)
    return pythonize_that_json(json.dumps(format_response_property_names(response), indent=4, ensure_ascii=False))


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
    response = get_unicode_character_at_codepoint(db_ctx, codepoint, show_props, verbose)
    return pythonize_that_json(json.dumps(format_response_property_names(response), indent=4, ensure_ascii=False))


def get_error_detail(
    db_ctx: DBSession, codepoint: str, show_props: list[str], verbose: bool | None = None
) -> Result[str]:
    try:
        _ = get_unicode_character_at_codepoint(db_ctx, codepoint, show_props, verbose)
        return Result.Fail("Expected an HTTPException to be raised")
    except HTTPException as ex:
        response = pythonize_that_json(json.dumps({"detail": ex.detail}, indent=4, ensure_ascii=False))
        return Result.Ok(response)
