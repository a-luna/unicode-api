import json
from typing import Any

from fastapi import HTTPException

from unicode_api.api.api_v1.dependencies import ListParametersDecimal, UnicodePlaneResolver
from unicode_api.api.api_v1.endpoints.blocks import get_block_list_endpoints, list_all_unicode_blocks
from unicode_api.config.api_settings import UnicodeApiSettings
from unicode_api.core.result import Result
from unicode_api.core.util import convert_keys_to_camel_case
from unicode_api.data.scripts.update_test_data.util import convert_json_to_python_literals

STATIC_CONTENT_2 = """
BOTH_START_AFTER_END_BEFORE_INVALID = {
    "detail": "Request contained values for BOTH 'ending_before' and 'starting_after', you must specify ONLY ONE of these two values."
}

INALID_PLANE_ABBREVIATION = {
    "detail": "BDP does not match any Unicode plane abbreviation: BMP, SMP, SIP, TIP, SSP, SPUA-A, SPUA-B."
}
"""


def update_test_list_all_unicode_blocks(settings: UnicodeApiSettings) -> Result[None]:
    result = get_error_detail()
    if result.failure:
        return Result[None].Fail(result.error)
    data_invalid_request = result.value or ""

    result = get_all_blocks_in_bmp_start_after_57_limit_20()
    if result.failure:
        return Result[None].Fail(result.error)
    data_all_blocks_in_bmp_start_after_57_limit_20 = result.value or ""

    result = get_all_blocks_end_before_171_limit_15()
    if result.failure:
        return Result[None].Fail(result.error)
    data_all_blocks_end_before_171_limit_15 = result.value or ""

    update_test_data_file(
        settings,
        data_all_blocks_in_bmp_start_after_57_limit_20,
        data_all_blocks_end_before_171_limit_15,
        data_invalid_request,
    )
    return Result[None].Ok()


def get_all_blocks_in_bmp_start_after_57_limit_20() -> Result[str]:
    plane = UnicodePlaneResolver(plane="BMP")
    list_params = ListParametersDecimal(starting_after=57, limit=20)
    return get_formatted_block_list(list_params, plane)


def get_all_blocks_end_before_171_limit_15() -> Result[str]:
    plane = UnicodePlaneResolver(plane=None)
    list_params = ListParametersDecimal(ending_before=171, limit=15)
    return get_formatted_block_list(list_params, plane)


def get_formatted_block_list(list_params: ListParametersDecimal, plane: UnicodePlaneResolver) -> Result[str]:
    response = list_all_unicode_blocks(list_params, plane)
    block_data = response.get("data", [])
    if not block_data or not isinstance(block_data, list):
        return Result[str].Fail("Expected 'data' to be a list")
    formatted_data: dict[str, Any] = {
        **response,
        "data": [block.model_dump() for block in block_data],
    }
    formatted_data = convert_keys_to_camel_case(formatted_data)
    converted_data = convert_json_to_python_literals(json.dumps(formatted_data, indent=4, ensure_ascii=False))
    return Result[str].Ok(converted_data)


def get_error_detail() -> Result[str]:
    plane = UnicodePlaneResolver(plane="TIP")
    list_params = ListParametersDecimal(limit=15, starting_after=20)
    try:
        _ = get_block_list_endpoints(list_params, plane)
        return Result[str].Fail("Expected an HTTPException to be raised")
    except HTTPException as ex:
        response = convert_json_to_python_literals(json.dumps({"detail": ex.detail}, indent=4, ensure_ascii=False))
        return Result[str].Ok(response)


def update_test_data_file(
    settings: UnicodeApiSettings,
    data_all_blocks_in_bmp_start_after_57_limit_20: str,
    data_all_blocks_end_before_171_limit_15: str,
    data_invalid_request: str,
):
    test_data = construct_test_data_file(
        data_all_blocks_in_bmp_start_after_57_limit_20,
        data_all_blocks_end_before_171_limit_15,
        data_invalid_request,
    )
    test_data_file = (
        settings.tests_folder.joinpath("test_block_endpoints")
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
