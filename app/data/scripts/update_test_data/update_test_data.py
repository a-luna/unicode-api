from app.config import get_settings
from app.core.result import Result
from app.data.scripts.update_test_data.update_test_get_unicode_character_details import (
    update_test_get_unicode_character_details,
)
from app.data.scripts.update_test_data.update_test_list_all_unicode_blocks import update_test_list_all_unicode_blocks
from app.data.scripts.update_test_data.update_test_list_all_unicode_planes import update_test_list_all_unicode_planes

UNICODE_VERSION_UNDER_TEST = "15.0.0"


def update_test_data():
    settings = get_settings()
    if settings.UNICODE_VERSION != UNICODE_VERSION_UNDER_TEST:
        error = (
            f"Error! All test cases require Unicode version v{UNICODE_VERSION_UNDER_TEST}, "
            f"the version available in this environment is v{settings.UNICODE_VERSION}. "
            "Update the value in the .env file to UNICODE_VERSION=15.0.0 and re-run this script"
        )
        return Result.Fail(error)
    print(f"Updating test data for Unicode v{settings.UNICODE_VERSION}")

    result = update_test_list_all_unicode_planes(settings)
    if result.failure:
        return result

    result = update_test_list_all_unicode_blocks(settings)
    if result.failure:
        return result

    result = update_test_get_unicode_character_details(settings)
    if result.failure:
        return result

    return Result.Ok()


if __name__ == "__main__":
    update_test_data()
