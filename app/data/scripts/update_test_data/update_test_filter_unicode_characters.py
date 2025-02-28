import json

from fastapi import HTTPException

from app.api.api_v1.dependencies import FilterSettings
from app.api.api_v1.endpoints.characters import filter_unicode_characters
from app.config.api_settings import UnicodeApiSettings
from app.core.result import Result
from app.data.scripts.update_test_data.util import format_response_property_names, pythonize_that_json
from app.db.session import DBSession


def update_test_filter_unicode_characters(db_ctx: DBSession, settings: UnicodeApiSettings):
    test_data = (
        f"FILTER_BY_NAME_BY_CATEGORY_BY_SCRIPT = {get_filter_by_name_by_category_by_script(db_ctx)}\n\n"
        + f"FILTER_BY_UNICODE_AGE = {get_filter_by_unicode_age(db_ctx)}\n\n"
        + f"FILTER_BY_BIDIRECTIONAL_CLASS = {get_filter_by_bidi_class(db_ctx)}\n\n"
        + f"FILTER_BY_DECOMPOSITION_TYPE = {get_filter_by_decomposition_type(db_ctx)}\n\n"
        + f"FILTER_BY_LINE_BREAK_TYPE = {get_filter_by_line_break_type(db_ctx)}\n\n"
        + f"FILTER_BY_CCC = {get_filter_by_combining_class_category(db_ctx)}\n\n"
        + f"FILTER_BY_NUMERIC_TYPE = {get_filter_by_numeric_type(db_ctx)}\n\n"
        + f"FILTER_BY_JOINING_TYPE = {get_filter_by_joining_type(db_ctx)}\n\n"
        + f"FILTER_BY_CHAR_FLAG = {get_filter_by_char_flags(db_ctx)}\n\n"
        + f"FILTER_BY_BLOCK_NAME = {get_filter_by_block_name(db_ctx)}\n\n"
        + f"FILTER_BY_COMBINED_CATEGORY = {get_filter_by_combined_category(db_ctx)}\n\n"
        + f"FILTER_BY_SEPARATE_CATEGORIES = {get_filter_by_separate_categories(db_ctx)}\n\n"
        + f"FILTER_BY_CJK_DEFINITION = {get_filter_by_cjk_definition(db_ctx)}\n\n"
        + f"NO_CHARS_MATCH_SETTINGS = {get_test_no_characters_found(db_ctx)}\n\n"
        + f"INVALID_NO_FILTER_SETTINGS = {get_test_no_filter_settings(db_ctx)}\n\n"
        + f"INVALID_PAGE_NUMBER = {get_test_invalid_page_number(db_ctx)}\n\n"
        + f"INVALID_FILTER_PARAM_VALUES = {get_test_test_invalid_filter_param_values(db_ctx)}\n\n"
    )
    test_data_file = (
        settings.TESTS_FOLDER.joinpath("test_character_endpoints")
        .joinpath("test_filter_unicode_characters")
        .joinpath("data.py")
    )
    test_data_file.write_text(test_data, encoding="utf-8")
    return Result.Ok()


def get_filter_by_name_by_category_by_script(db_ctx: DBSession):
    filter_settings = FilterSettings(name="spiritus", category=["mn"], script=["copt"], verbose=False)
    return get_formatted_filter_results(db_ctx, filter_settings)


def get_filter_by_unicode_age(db_ctx: DBSession):
    filter_settings = FilterSettings(category=["sk"], age=["13.0", "14.0", "15.0"])
    return get_formatted_filter_results(db_ctx, filter_settings)


def get_filter_by_bidi_class(db_ctx: DBSession):
    filter_settings = FilterSettings(name="dong", bidi_class=["et"])
    return get_formatted_filter_results(db_ctx, filter_settings)


def get_filter_by_decomposition_type(db_ctx: DBSession):
    filter_settings = FilterSettings(name="seven", decomp_type=["enc"])
    return get_formatted_filter_results(db_ctx, filter_settings)


def get_filter_by_line_break_type(db_ctx: DBSession):
    filter_settings = FilterSettings(line_break=["is"])
    return get_formatted_filter_results(db_ctx, filter_settings)


def get_filter_by_combining_class_category(db_ctx: DBSession):
    filter_settings = FilterSettings(ccc=["214"])
    return get_formatted_filter_results(db_ctx, filter_settings)


def get_filter_by_numeric_type(db_ctx: DBSession):
    filter_settings = FilterSettings(script=["khar"], num_type=["di"])
    return get_formatted_filter_results(db_ctx, filter_settings)


def get_filter_by_joining_type(db_ctx: DBSession):
    filter_settings = FilterSettings(join_type=["l"])
    return get_formatted_filter_results(db_ctx, filter_settings)


def get_filter_by_char_flags(db_ctx: DBSession):
    filter_settings = FilterSettings(flag=["Is Hyphen"], per_page=20)
    return get_formatted_filter_results(db_ctx, filter_settings)


def get_filter_by_block_name(db_ctx: DBSession):
    filter_settings = FilterSettings(block=["Ancient_Symbols"])
    return get_formatted_filter_results(db_ctx, filter_settings)


def get_filter_by_combined_category(db_ctx: DBSession):
    filter_settings = FilterSettings(block=["Basic_Latin"], category=["p"])
    return get_formatted_filter_results(db_ctx, filter_settings)


def get_filter_by_separate_categories(db_ctx: DBSession):
    filter_settings = FilterSettings(block=["Basic_Latin"], category=["pc", "pd", "ps", "pe", "pi", "pf", "po"])
    return get_formatted_filter_results(db_ctx, filter_settings)


def get_filter_by_cjk_definition(db_ctx: DBSession):
    filter_settings = FilterSettings(cjk_definition="dragon")
    return get_formatted_filter_results(db_ctx, filter_settings)


def get_test_no_characters_found(db_ctx: DBSession):
    filter_settings = FilterSettings(name="test", script=["copt"], show_props=["all"])
    return get_formatted_filter_results(db_ctx, filter_settings)


def get_test_no_filter_settings(db_ctx: DBSession):
    filter_settings = FilterSettings()
    result = get_error_detail(db_ctx, filter_settings)
    return result.value if result.success and result.value else ""


def get_test_invalid_page_number(db_ctx: DBSession):
    filter_settings = FilterSettings(name="spiritus", category=["mn"], script=["copt"], page=2)
    result = get_error_detail(db_ctx, filter_settings)
    return result.value if result.success and result.value else ""


def get_test_test_invalid_filter_param_values(db_ctx: DBSession):
    filter_settings = FilterSettings(
        category=["aa", "bb"],
        age=["7.1", "12.97"],
        script=["blar", "blee"],
        bidi_class=["vv", "rr"],
        show_props=["soup", "salad"],
        decomp_type=["gosh"],
        line_break=["ha"],
        ccc=["300"],
        num_type=["dd"],
        join_type=["j"],
        flag=["special", "basic"],
        block=["xxx"],
    )
    result = get_error_detail(db_ctx, filter_settings)
    return result.value if result.success and result.value else ""


def get_formatted_filter_results(db_ctx: DBSession, filter_settings: FilterSettings) -> str:
    response = filter_unicode_characters(db_ctx, filter_settings)
    response["filter_settings"] = response["filter_settings"].model_dump(
        by_alias=True, exclude_unset=True, exclude_defaults=True, exclude_none=True
    )
    return pythonize_that_json(json.dumps(format_response_property_names(response), indent=4, ensure_ascii=False))


def get_error_detail(db_ctx: DBSession, filter_settings: FilterSettings) -> Result[str]:
    try:
        _ = filter_unicode_characters(db_ctx, filter_settings)
        return Result.Fail("Expected an HTTPException to be raised")
    except HTTPException as ex:
        response = pythonize_that_json(json.dumps({"detail": ex.detail}, indent=4, ensure_ascii=False))
        return Result.Ok(response)
