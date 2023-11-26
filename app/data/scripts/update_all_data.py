import json
import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from app.core.config import UnicodeApiSettings
from app.core.result import Result
from app.data.scripts import (
    bootstrap_unicode_data,
    download_xml_unicode_database,
    parse_xml_unicode_database,
    populate_sqlite_database,
    save_parsed_data_to_csv,
)
from app.data.util import finish_task, run_command, start_task

CharDetailsDict = dict[str, bool | int | str]
BlockOrPlaneDetailsDict = dict[str, int | str]


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

    if os.environ.get("ENV") == "PROD":
        if config.XML_FILE.exists():
            config.XML_FILE.unlink()
    else:
        result = backup_db_and_json_files(config)
        if result.failure:
            return result
    return Result.Ok()


def get_xml_unicode_database(config: UnicodeApiSettings) -> Result[Path]:
    spinner = start_task(f"Downloading Unicode XML Database v{config.UNICODE_VERSION} from unicode.org...")
    spinner.stop_and_persist()
    get_xml_result = download_xml_unicode_database(config)
    if get_xml_result.failure or not get_xml_result.value:
        finish_task(spinner, False, "Download failed! Please check the internet connection.")
        return get_xml_result
    spinner.start()
    finish_task(spinner, True, f"Successfully downloaded Unicode XML Database v{config.UNICODE_VERSION}!")
    xml_file = get_xml_result.value
    return Result.Ok(xml_file)


def update_json_files(
    config: UnicodeApiSettings,
    all_planes: list[BlockOrPlaneDetailsDict],
    all_blocks: list[BlockOrPlaneDetailsDict],
    all_chars: list[CharDetailsDict],
):
    spinner = start_task("Creating JSON files for parsed Unicode data...")
    config.PLANES_JSON.write_text(json.dumps(all_planes, indent=4))
    config.BLOCKS_JSON.write_text(json.dumps(all_blocks, indent=4))
    char_name_map = {int(char["codepoint_dec"]): char["name"] for char in all_chars if not char["_unihan"]}
    config.CHAR_NAME_MAP.write_text(json.dumps(char_name_map, indent=4))
    finish_task(spinner, True, "Successfully created JSON files for parsed Unicode data")


def backup_db_and_json_files(config: UnicodeApiSettings) -> Result[None]:
    spinner = start_task("Creating compressed backup files of SQLite DB and JSON files...")
    backup_sqlite_db(config)
    backup_json_files(config)
    finish_task(spinner, True, "Successfully created compressed backup files of SQLite DB and JSON files!")

    spinner = start_task("")
    spinner.stop_and_persist("Uploading backup files to S3 bucket...")
    result = upload_zip_file_to_s3(config, config.DB_ZIP_FILE)
    if result.failure:
        return result
    config.DB_ZIP_FILE.unlink()

    result = upload_zip_file_to_s3(config, config.JSON_ZIP_FILE)
    if result.failure:
        return result
    config.JSON_ZIP_FILE.unlink()
    finish_task(spinner, True, "Successfully uploaded backup files to S3 bucket!")
    return Result.Ok()


def backup_sqlite_db(config: UnicodeApiSettings):
    with ZipFile(config.DB_ZIP_FILE, "w", ZIP_DEFLATED) as zip:
        zip.write(config.DB_FILE, f"{config.DB_FILE.name}")


def backup_json_files(config: UnicodeApiSettings):
    zip_file = config.JSON_FOLDER.joinpath("unicode_json.zip")
    with ZipFile(zip_file, "w", ZIP_DEFLATED) as zip:
        zip.write(config.PLANES_JSON, f"{config.PLANES_JSON.name}")
        zip.write(config.BLOCKS_JSON, f"{config.BLOCKS_JSON.name}")
        zip.write(config.CHAR_NAME_MAP, f"{config.CHAR_NAME_MAP.name}")


def upload_zip_file_to_s3(config: UnicodeApiSettings, local_file: Path) -> Result[None]:
    result = run_command(f"s3cmd put {local_file} {config.S3_BUCKET_URL}/{config.UNICODE_VERSION}/{local_file.name} -P")
    if result.failure:
        return result
    return Result.Ok()
