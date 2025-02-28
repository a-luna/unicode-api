import json

from fastapi import HTTPException

from app.api.api_v1.dependencies import BlockSearchParameters
from app.api.api_v1.endpoints.blocks import search_unicode_blocks_by_name
from app.config.api_settings import UnicodeApiSettings
from app.core.result import Result
from app.data.scripts.update_test_data.util import format_response_property_names, pythonize_that_json


def update_test_search_unicode_blocks_by_name(settings: UnicodeApiSettings):
    test_data = (
        f"SEARCH_TERM_OLD_PER_PAGE_5_PAGE_1_OF_2 = {get_search_term_old_page_1_of_2()}\n"
        f"SEARCH_TERM_OLD_PER_PAGE_5_PAGE_2_OF_2 = {get_search_term_old_page_2_of_2()}\n"
        f"SEARCH_TERM_OLD_PER_PAGE_5_PAGE_3_OF_2 = {get_search_term_old_page_3_of_2()}\n"
        f"SEARCH_TERM_CAP = {get_search_term_cap()}\n"
        f"SEARCH_TERM_BLAH = {get_search_term_blah()}\n"
    )
    test_data_file = (
        settings.TESTS_FOLDER.joinpath("test_block_endpoints")
        .joinpath("test_search_unicode_blocks_by_name")
        .joinpath("data.py")
    )
    test_data_file.write_text(test_data, encoding="utf-8")
    return Result.Ok()


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
    return pythonize_that_json(json.dumps(format_response_property_names(response), indent=4, ensure_ascii=False))


def get_error_detail(search_params: BlockSearchParameters) -> Result[str]:
    try:
        _ = search_unicode_blocks_by_name(search_params)
        return Result.Fail("Expected an HTTPException to be raised")
    except HTTPException as ex:
        response = pythonize_that_json(json.dumps({"detail": ex.detail}, indent=4, ensure_ascii=False))
        return Result.Ok(response)
