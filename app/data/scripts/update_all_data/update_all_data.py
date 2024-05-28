from app.core.result import Result
from app.data.scripts.update_all_data import (
    backup_db_and_json_files,
    download_xml_unicode_database,
    get_api_settings,
    parse_xml_unicode_database,
    populate_sqlite_database,
    save_parsed_data,
)


def update_all_data() -> Result[None]:
    result = get_api_settings()
    if result.failure or not result.value:
        return Result.Fail(result.error)
    settings = result.value

    result = download_xml_unicode_database(settings)
    if result.failure:
        return result

    result = parse_xml_unicode_database(settings)
    if result.failure:
        return Result.Fail(result.error)
    (all_planes, all_blocks, all_chars) = result.value

    result = save_parsed_data(settings, all_planes, all_blocks, all_chars)
    if result.failure:
        return result

    result = populate_sqlite_database(settings)
    if result.failure:
        return result

    if settings.is_prod and settings.XML_FILE.exists():
        settings.XML_FILE.unlink()
    else:
        result = backup_db_and_json_files(settings)
        if result.failure:
            return result
    return Result.Ok()
