import json

from fastapi import HTTPException

from unicode_api.api.api_v1.dependencies import BlockSearchParameters
from unicode_api.api.api_v1.endpoints.blocks import search_unicode_blocks_by_name
from unicode_api.config.api_settings import UnicodeApiSettings
from unicode_api.core.result import Result
from unicode_api.core.util import convert_keys_to_camel_case
from unicode_api.data.scripts.update_test_data.util import convert_json_to_python_literals


def update_test_search_unicode_blocks_by_name(settings: UnicodeApiSettings) -> Result[None]:
    test_data = (
        f"SEARCH_TERM_OLD_PER_PAGE_5_PAGE_1_OF_2 = {get_search_term_old_page_1_of_2()}\n"
        f"SEARCH_TERM_OLD_PER_PAGE_5_PAGE_2_OF_2 = {get_search_term_old_page_2_of_2()}\n"
        f"SEARCH_TERM_OLD_PER_PAGE_5_PAGE_3_OF_2 = {get_search_term_old_page_3_of_2()}\n"
        f"SEARCH_TERM_CAP = {get_search_term_cap()}\n"
        f"SEARCH_TERM_BLAH = {get_search_term_blah()}\n"
    )
    test_data_file = (
        settings.tests_folder.joinpath("test_block_endpoints")
        .joinpath("test_search_unicode_blocks_by_name")
        .joinpath("data.py")
    )
    test_data_file.write_text(test_data, encoding="utf-8")
    return Result[None].Ok()


def get_search_term_old_page_1_of_2():
    search_parameters = BlockSearchParameters(name="old", per_page=5)
    return get_formatted_search_results(search_parameters)


def get_search_term_old_page_2_of_2():
    search_parameters = BlockSearchParameters(name="old", per_page=5, page=2)
    return get_formatted_search_results(search_parameters)


def get_search_term_old_page_3_of_2():
    search_parameters = BlockSearchParameters(name="old", per_page=5, page=3)
    result = get_error_detail(search_parameters)
    return result.value if result.success and result.value else ""


def get_search_term_cap():
    search_parameters = BlockSearchParameters(name="cap")
    return get_formatted_search_results(search_parameters)


def get_search_term_blah():
    search_parameters = BlockSearchParameters(name="blah")
    return get_formatted_search_results(search_parameters)


def get_formatted_search_results(search_params: BlockSearchParameters) -> str:
    response = search_unicode_blocks_by_name(search_params)
    response["results"] = [block.model_dump() for block in response["results"]]
    response = convert_keys_to_camel_case(response)
    return convert_json_to_python_literals(json.dumps(response, indent=4, ensure_ascii=False))


def get_error_detail(search_params: BlockSearchParameters) -> Result[str]:
    try:
        _ = search_unicode_blocks_by_name(search_params)
        return Result[str].Fail("Expected an HTTPException to be raised")
    except HTTPException as ex:
        response = convert_json_to_python_literals(json.dumps({"detail": ex.detail}, indent=4, ensure_ascii=False))
        return Result[str].Ok(response)
