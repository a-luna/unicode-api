from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from app.config.api_settings import UnicodeApiSettings
from app.core.result import Result
from app.data.util.command import run_command
from app.data.util.spinners import Spinner


def backup_db_and_json_files(config: UnicodeApiSettings) -> Result[None]:
    spinner = Spinner()
    spinner.start("Creating compressed backup files of SQLite DB and JSON files...")
    backup_sqlite_db(config)
    backup_json_files(config)
    spinner.successful("Successfully created compressed backup files of SQLite DB and JSON files!")

    spinner = Spinner()
    result = upload_zip_file_to_s3(config, config.DB_ZIP_FILE)
    if result.failure:
        spinner.start("")
        spinner.failed(result.error)
        return result
    config.DB_ZIP_FILE.unlink()

    result = upload_zip_file_to_s3(config, config.JSON_ZIP_FILE)
    if result.failure:
        spinner.start("")
        spinner.failed(result.error)
        return result
    config.JSON_ZIP_FILE.unlink()
    spinner.start("")
    spinner.successful("Successfully uploaded backup files to S3 bucket!")
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
        zip.write(config.UNIHAN_CHARS_JSON, f"{config.UNIHAN_CHARS_JSON.name}")
        zip.write(config.TANGUT_CHARS_JSON, f"{config.TANGUT_CHARS_JSON.name}")


def upload_zip_file_to_s3(config: UnicodeApiSettings, local_file: Path) -> Result[None]:
    result = run_command(f"s3cmd put {local_file} {config.S3_BUCKET_URL}/{config.UNICODE_VERSION}/{local_file.name} -P")
    if result.failure:
        return result
    return Result.Ok()
