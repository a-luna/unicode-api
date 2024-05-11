import json
from pathlib import Path

from app.config.api_settings import UnicodeApiSettings
from app.core.result import Result
from app.data.scripts import (
    backup_db_and_json_files,
    bootstrap_unicode_data,
    download_xml_unicode_database,
    parse_xml_unicode_database,
    populate_sqlite_database,
    save_parsed_data_to_csv,
)
from app.data.scripts.script_types import BlockOrPlaneDetailsDict, CharDetailsDict
from app.data.util.spinners import Spinner


def update_all_data() -> Result[None]:
    result = bootstrap_unicode_data()
    if result.failure or not result.value:
        return Result.Fail(result.error or "")
    config = result.value

    result = get_xml_unicode_database(config)
    if result.failure:
        return Result.Fail(result.error or "")

    result = parse_xml_unicode_database(config)
    if result.failure:
        return Result.Fail(result.error or "")
    (all_planes, all_blocks, all_chars) = result.value or ([], [], [])
    update_json_files(config, all_planes, all_blocks, all_chars)

    result = save_parsed_data_to_csv(config, all_planes, all_blocks, all_chars)
    if result.failure:
        return result

    result = populate_sqlite_database(config)
    if result.failure:
        return result

    if config.is_prod and config.XML_FILE.exists():
        config.XML_FILE.unlink()
    else:
        result = backup_db_and_json_files(config)
        if result.failure:
            return result
    return Result.Ok()


def get_xml_unicode_database(config: UnicodeApiSettings) -> Result[Path]:
    spinner = Spinner()
    result = download_xml_unicode_database(config)
    if result.failure or not result.value:
        spinner.start("")
        spinner.failed("Download failed! Please check the internet connection.")
        return result
    spinner.start("")
    spinner.successful(f"Successfully downloaded Unicode XML Database v{config.UNICODE_VERSION}!")
    xml_file = result.value
    return Result.Ok(xml_file)


def update_json_files(
    config: UnicodeApiSettings,
    all_planes: list[BlockOrPlaneDetailsDict],
    all_blocks: list[BlockOrPlaneDetailsDict],
    all_chars: list[CharDetailsDict],
) -> None:
    spinner = Spinner()
    spinner.start("Creating JSON files for parsed Unicode data...")
    config.PLANES_JSON.write_text(json.dumps(all_planes, indent=4))
    config.BLOCKS_JSON.write_text(json.dumps(all_blocks, indent=4))
    char_name_map = {
        int(char["codepoint_dec"]): char["name"] for char in all_chars if not char["_unihan"] and not char["_tangut"]
    }
    config.CHAR_NAME_MAP.write_text(json.dumps(char_name_map, indent=4))
    unihan_char_block_map = {int(char["codepoint_dec"]): int(char["block_id"]) for char in all_chars if char["_unihan"]}
    config.UNIHAN_CHARS_JSON.write_text(json.dumps(unihan_char_block_map, indent=4))
    tangut_char_block_map = {int(char["codepoint_dec"]): int(char["block_id"]) for char in all_chars if char["_tangut"]}
    config.TANGUT_CHARS_JSON.write_text(json.dumps(tangut_char_block_map, indent=4))
    spinner.successful("Successfully created JSON files for parsed Unicode data")
