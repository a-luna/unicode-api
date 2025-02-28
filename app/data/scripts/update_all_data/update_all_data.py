from app.core.result import Result
from app.data.scripts.update_all_data import (
    backup_db_and_json_files,
    download_xml_unicode_database,
    get_api_settings,
    get_prop_values,
    parse_xml_unicode_database,
    populate_sqlite_database,
    save_parsed_data,
)


def update_all_data() -> Result[None]:
    result = get_api_settings()
    if result.failure or not result.value:
        return Result.Fail(result.error)
    settings = result.value

    result = get_prop_values(settings)
    if result.failure:
        return Result.Fail(result.error)

    result = download_xml_unicode_database(settings)
    if result.failure:
        return Result.Fail(result.error)

    result = parse_xml_unicode_database(settings)
    if result.failure or not result.value:
        return Result.Fail(result.error)
    parsed_data = result.value

    result = save_parsed_data(settings, parsed_data)
    if result.failure:
        return result

    result = populate_sqlite_database(settings, parsed_data)
    if result.failure:
        return result

    if settings.is_prod and settings.XML_FILE.exists():
        settings.XML_FILE.unlink()
    else:
        result = backup_db_and_json_files(settings)
        if result.failure:
            return result
    return Result.Ok()


if __name__ == "__main__":
    update_all_data()
