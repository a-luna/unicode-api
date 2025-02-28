import json

from fastapi import HTTPException

from app.api.api_v1.dependencies import CharacterSearchParameters
from app.api.api_v1.endpoints.characters import search_unicode_characters_by_name
from app.config.api_settings import UnicodeApiSettings
from app.core.result import Result
from app.data.scripts.update_test_data.util import format_response_property_names, pythonize_that_json
from app.db.session import DBSession


def update_test_search_unicode_characters_by_name(db_ctx: DBSession, settings: UnicodeApiSettings):
    test_data = (
        f"SEARCH_TERM_HOME = {get_search_term_home(db_ctx)}\n"
        f"SEARCH_TERM_HOUSE_PAGE_1_OF_2 = {get_search_term_house_page_1_of_3(db_ctx)}\n"
        f"SEARCH_TERM_HOUSE_PAGE_2_OF_2 = {get_search_term_house_page_2_of_3(db_ctx)}\n"
        f"SEARCH_TERM_HOUSE_PAGE_3_OF_2 = {get_search_term_house_page_3_of_3(db_ctx)}\n"
    )
    test_data_file = (
        settings.TESTS_FOLDER.joinpath("test_character_endpoints")
        .joinpath("test_search_unicode_characters_by_name")
        .joinpath("data.py")
    )
    test_data_file.write_text(test_data, encoding="utf-8")
    return Result.Ok()


def get_search_term_home(db_ctx: DBSession):
    search_parameters = CharacterSearchParameters(name="home")
    return get_formatted_search_results(db_ctx, search_parameters)


def get_search_term_house_page_1_of_3(db_ctx: DBSession):
    search_parameters = CharacterSearchParameters(name="house")
    return get_formatted_search_results(db_ctx, search_parameters)


def get_search_term_house_page_2_of_3(db_ctx: DBSession):
    search_parameters = CharacterSearchParameters(name="house", page=2)
    return get_formatted_search_results(db_ctx, search_parameters)


def get_search_term_house_page_3_of_3(db_ctx: DBSession):
    search_parameters = CharacterSearchParameters(name="house", page=3)
    result = get_error_detail(db_ctx, search_parameters)
    return result.value if result.success and result.value else ""


def get_formatted_search_results(db_ctx: DBSession, search_params: CharacterSearchParameters) -> str:
    response = search_unicode_characters_by_name(db_ctx, search_params)
    return pythonize_that_json(json.dumps(format_response_property_names(response), indent=4, ensure_ascii=False))


def get_error_detail(db_ctx: DBSession, search_params: CharacterSearchParameters) -> Result[str]:
    try:
        _ = search_unicode_characters_by_name(db_ctx, search_params)
        return Result.Fail("Expected an HTTPException to be raised")
    except HTTPException as ex:
        response = pythonize_that_json(json.dumps({"detail": ex.detail}, indent=4, ensure_ascii=False))
        return Result.Ok(response)
