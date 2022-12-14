import json
import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from app.core.config import (
    BLOCKS_JSON,
    CHAR_NAME_MAP,
    CHAR_NO_NAME_MAP,
    CHARACTERS_JSON,
    DB_FILE,
    DB_FOLDER,
    JSON_FOLDER,
    PLANES_JSON,
    S3_BUCKET_URL,
)
from app.core.result import Result
from app.data.scripts import (
    finish_task,
    get_xml_unicode_database,
    parse_xml_unicode_database,
    populate_sqlite_database,
    run_command,
    start_task,
)


def update_all_data(version: str):
    spinner = start_task(f"Downloading Unicode XML Database v{version} from unicode.org...")
    spinner.stop_and_persist()
    get_xml_result = get_xml_unicode_database(version)
    if get_xml_result.failure:
        finish_task(spinner, False, "Download failed! Please check the internet connection.")
        return get_xml_result
    spinner.start()
    finish_task(spinner, True, f"Successfully downloaded Unicode XML Database v{version}!")
    xml_file = get_xml_result.value
    if xml_file and xml_file.exists():
        result = parse_xml_unicode_database(xml_file)
        if result.failure:
            return result
        if result.value:
            (all_planes, all_blocks, all_chars) = result.value
            update_unicode_json_files(all_planes, all_blocks, all_chars)

            populate_db_result = populate_sqlite_database()
            if populate_db_result.failure:
                return populate_db_result
            if os.environ.get("ENV") == "PROD":
                if xml_file.exists():
                    xml_file.unlink()
                delete_character_json_file()
            else:
                zip_file = backup_sqlite_db()
                result = upload_zip_file_to_s3(zip_file)
                if result.failure:
                    return result
                zip_file = backup_json_files()
                result = upload_zip_file_to_s3(zip_file)
                if result.failure:
                    return result
            return Result.Ok()


def update_unicode_json_files(all_planes, all_blocks, all_chars):
    PLANES_JSON.write_text(json.dumps(all_planes, indent=4))
    BLOCKS_JSON.write_text(json.dumps(all_blocks, indent=4))
    CHARACTERS_JSON.write_text(json.dumps(all_chars, indent=4))

    char_name_map = {int(char["codepoint_dec"]): char["name"] for char in all_chars if not char["no_name"]}
    CHAR_NAME_MAP.write_text(json.dumps(char_name_map, indent=4))

    char_no_name_map = {int(char["codepoint_dec"]): char["name"] for char in all_chars if char["no_name"]}
    CHAR_NO_NAME_MAP.write_text(json.dumps(char_no_name_map, indent=4))


def delete_character_json_file():
    if CHARACTERS_JSON.exists():
        CHARACTERS_JSON.unlink()


def backup_sqlite_db():
    spinner = start_task("Creating compressed backup file of SQLite database...")
    zip_file = DB_FOLDER.joinpath("unicode-api.db.zip")
    with ZipFile(zip_file, "w", ZIP_DEFLATED) as zip:
        zip.write(DB_FILE, f"{DB_FILE. name}")
    finish_task(spinner, True, "Successfully created compressed backup file of SQLite database!")
    return zip_file


def backup_json_files():
    zip_file = JSON_FOLDER.joinpath("unicode_json.zip")
    with ZipFile(zip_file, "w", ZIP_DEFLATED) as zip:
        zip.write(PLANES_JSON, f"{PLANES_JSON. name}")
        zip.write(BLOCKS_JSON, f"{BLOCKS_JSON.name}")
        zip.write(CHAR_NAME_MAP, f"{CHAR_NAME_MAP.name}")
        zip.write(CHAR_NO_NAME_MAP, f"{CHAR_NO_NAME_MAP.name}")
    return zip_file


def upload_zip_file_to_s3(zip_file: Path):
    result = run_command(f"s3cmd put {zip_file} {S3_BUCKET_URL} -P")
    if result.failure:
        return result
    zip_file.unlink()
    return Result.Ok()


if __name__ == "__main__":
    update_all_data("15.0.0")
