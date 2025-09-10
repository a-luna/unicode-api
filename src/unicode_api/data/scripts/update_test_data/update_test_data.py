from sqlmodel import Session

from unicode_api.config.api_settings import UnicodeApiSettings, get_settings
from unicode_api.core.result import Result
from unicode_api.data.scripts.update_test_data import (
    update_test_filter_unicode_characters,
    update_test_get_unicode_character_at_codepoint,
    update_test_get_unicode_character_details,
    update_test_list_all_unicode_blocks,
    update_test_list_all_unicode_planes,
    update_test_search_unicode_blocks_by_name,
    update_test_search_unicode_characters_by_name,
)
from unicode_api.db.engine import ro_db_engine as engine
from unicode_api.db.session import DBSession

UNICODE_VERSION_UNDER_TEST = "15.0.0"


def update_test_data() -> Result[None]:
    settings = get_settings()
    if settings.UNICODE_VERSION != UNICODE_VERSION_UNDER_TEST:
        error = (
            f"Error! All test cases require Unicode version v{UNICODE_VERSION_UNDER_TEST}, "
            f"the version available in this environment is v{settings.UNICODE_VERSION}. "
            "Update the value in the .env file to UNICODE_VERSION=15.0.0 and re-run this script"
        )
        return Result[None].Fail(error)
    print(f"Updating test data for Unicode v{settings.UNICODE_VERSION}")

    with Session(engine) as session:
        return update_all_test_data(DBSession(session, engine), settings)


def update_all_test_data(db_ctx: DBSession, settings: UnicodeApiSettings) -> Result[None]:
    result = update_test_filter_unicode_characters(db_ctx, settings)
    if result.failure:
        return result

    result = update_test_get_unicode_character_details(db_ctx, settings)
    if result.failure:
        return result

    result = update_test_get_unicode_character_at_codepoint(db_ctx, settings)
    if result.failure:
        return result

    result = update_test_list_all_unicode_blocks(settings)
    if result.failure:
        return result

    result = update_test_list_all_unicode_planes(settings)
    if result.failure:
        return result

    result = update_test_search_unicode_blocks_by_name(settings)
    if result.failure:
        return result

    result = update_test_search_unicode_characters_by_name(db_ctx, settings)
    if result.failure:
        return result

    return Result[None].Ok()


if __name__ == "__main__":
    result = update_test_data()
    if result.failure:
        print(f"Failed to update test data: {result.error}")
    else:
        print("Test data updated successfully.")
