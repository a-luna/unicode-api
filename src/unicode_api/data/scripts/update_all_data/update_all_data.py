"""
This module provides a function to update all Unicode-related data in the SQLite database.
It orchestrates the process of fetching API settings, retrieving Unicode property values,
downloading and parsing the Unicode XML database, saving the parsed data, and populating
the SQLite database. Depending on the environment, it either deletes the XML file (in
production) or backs up the database and JSON files (in non-production environments).

Functions:
    update_all_data() -> Result[None]:
        Executes the full update workflow and returns a Result indicating success or failure.
"""

from unicode_api.core.result import Result
from unicode_api.data.scripts.update_all_data import (
    backup_db_and_json_files,
    download_xml_unicode_database,
    get_api_settings,
    get_prop_values,
    parse_xml_unicode_database,
    populate_sqlite_database,
    save_parsed_data,
)


def update_all_data() -> Result[None]:
    """
    Updates all Unicode-related data by performing a series of operations including fetching API settings,
    retrieving property values, downloading and parsing the Unicode XML database, saving parsed data, and
    populating the SQLite database. Depending on the environment, it either deletes the XML file or back
    up the database and JSON files.

    Returns:
        Result[None]: A Result object indicating success or failure, with error details if any step fails.
    """
    result = get_api_settings()
    if result.failure or not result.value:
        return Result[None].Fail(result.error)
    settings = result.value

    result = get_prop_values(settings)
    if result.failure:
        return Result[None].Fail(result.error)

    result = download_xml_unicode_database(settings)
    if result.failure:
        return Result[None].Fail(result.error)

    result = parse_xml_unicode_database(settings)
    if result.failure or not result.value:
        return Result[None].Fail(result.error)
    parsed_data = result.value

    result = save_parsed_data(settings, parsed_data)
    if result.failure:
        return result

    result = populate_sqlite_database(settings, parsed_data)
    if result.failure:
        return result

    if settings.is_prod and settings.xml_file.exists():
        settings.xml_file.unlink()
    else:
        result = backup_db_and_json_files(settings)
        if result.failure:
            return result
    return Result[None].Ok()


if __name__ == "__main__":
    update_all_data()
