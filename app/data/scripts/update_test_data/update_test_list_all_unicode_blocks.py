import json

from fastapi import HTTPException

from app.api.api_v1.dependencies import ListParametersDecimal, UnicodePlaneResolver
from app.api.api_v1.endpoints.blocks import get_block_list_endpoints, list_all_unicode_blocks
from app.config.api_settings import UnicodeApiSettings
from app.core.result import Result
from app.data.scripts.update_test_data.util import format_response_property_names, pythonize_that_json

STATIC_CONTENT_2 = """
BOTH_START_AFTER_END_BEFORE_INVALID = {
    "detail": "Request contained values for BOTH 'ending_before' and 'starting_after', you must specify ONLY ONE of these two values."
}

INALID_PLANE_ABBREVIATION = {
    "detail": "BDP does not match any Unicode plane abbreviation: BMP, SMP, SIP, TIP, SSP, SPUA-A, SPUA-B."
}
"""


def update_test_list_all_unicode_blocks(settings: UnicodeApiSettings):
    result = get_error_detail()
    if result.failure:
        return result
    data_invalid_request = result.value or ""

    update_test_data_file(
        settings,
        get_all_blocks_in_bmp_start_after_57_limit_20(),
        get_all_blocks_end_before_171_limit_15(),
        data_invalid_request,
    )
    return Result.Ok()


def get_all_blocks_in_bmp_start_after_57_limit_20() -> str:
    plane = UnicodePlaneResolver(plane="BMP")
    list_params = ListParametersDecimal(starting_after=57, limit=20)
    return get_formatted_block_list(plane, list_params)


def get_all_blocks_end_before_171_limit_15() -> str:
    plane = UnicodePlaneResolver(plane=None)
    list_params = ListParametersDecimal(ending_before=171, limit=15)
    return get_formatted_block_list(plane, list_params)


def get_formatted_block_list(plane: UnicodePlaneResolver, list_params: ListParametersDecimal) -> str:
    response = list_all_unicode_blocks(list_params, plane)
    response["data"] = [block.model_dump() for block in response["data"]]
    return pythonize_that_json(json.dumps(format_response_property_names(response), indent=4, ensure_ascii=False))


def get_error_detail() -> Result[str]:
    plane = UnicodePlaneResolver(plane="TIP")
    list_params = ListParametersDecimal(limit=15, starting_after=20)
    try:
        _ = get_block_list_endpoints(list_params, plane)
        return Result.Fail("Expected an HTTPException to be raised")
    except HTTPException as ex:
        response = pythonize_that_json(json.dumps({"detail": ex.detail}, indent=4, ensure_ascii=False))
        return Result.Ok(response)


def update_test_data_file(
    settings: UnicodeApiSettings,
    data_all_blocks_in_bmp_start_after_57_limit_20: str,
    data_all_blocks_end_before_171_limit_15: str,
    data_invalid_request: str,
):
    test_data = construct_test_data_file(
        data_all_blocks_in_bmp_start_after_57_limit_20, data_all_blocks_end_before_171_limit_15, data_invalid_request
    )
    test_data_file = (
        settings.TESTS_FOLDER.joinpath("test_block_endpoints")
        .joinpath("test_list_all_unicode_blocks")
        .joinpath("data.py")
    )
    test_data_file.write_text(test_data, encoding="utf-8")


def construct_test_data_file(
    data_all_blocks_in_bmp_start_after_57_limit_20: str,
    data_all_blocks_end_before_171_limit_15: str,
    data_invalid_request: str,
):
    return (
        f"PLANE_BMP_START_AFTER_57_LIMIT_20 = {data_all_blocks_in_bmp_start_after_57_limit_20}\n\n"
        + f"ALL_BLOCKS_ENDING_BEFORE_171_LIMIT_15 = {data_all_blocks_end_before_171_limit_15}\n\n"
        + f"PLANE_TIP_START_AFTER_20_LIMIT_15 = {data_invalid_request}\n\n"
        + STATIC_CONTENT_2
    )
