from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from app.config.api_settings import UnicodeApiSettings
from app.core.result import Result
from app.data.util.command import run_command
from app.data.util.spinners import Spinner


def backup_db_and_json_files(settings: UnicodeApiSettings) -> Result[None]:
    spinner = Spinner()
    spinner.start("Creating compressed backup files of SQLite DB and JSON files...")
    backup_sqlite_db(settings)
    backup_json_files(settings)
    spinner.successful("Successfully created compressed backup files of SQLite DB and JSON files!")

    spinner = Spinner()
    result = upload_zip_file_to_s3(settings, settings.DB_ZIP_FILE)
    if result.failure:
        spinner.start("")
        spinner.failed(result.error)
        return result
    settings.DB_ZIP_FILE.unlink()

    result = upload_zip_file_to_s3(settings, settings.JSON_ZIP_FILE)
    if result.failure:
        spinner.start("")
        spinner.failed(result.error)
        return result
    settings.JSON_ZIP_FILE.unlink()
    spinner.start("")
    spinner.successful("Successfully uploaded backup files to S3 bucket!")
    return Result.Ok()


def backup_sqlite_db(settings: UnicodeApiSettings):
    with ZipFile(settings.DB_ZIP_FILE, "w", ZIP_DEFLATED) as zip:
        zip.write(settings.DB_FILE, f"{settings.DB_FILE.name}")


def backup_json_files(settings: UnicodeApiSettings):
    zip_file = settings.JSON_FOLDER.joinpath("unicode_json.zip")
    with ZipFile(zip_file, "w", ZIP_DEFLATED) as zip:
        zip.write(settings.PROP_VALUES_JSON, f"{settings.PROP_VALUES_JSON.name}")
        zip.write(settings.PLANES_JSON, f"{settings.PLANES_JSON.name}")
        zip.write(settings.BLOCKS_JSON, f"{settings.BLOCKS_JSON.name}")
        zip.write(settings.CHAR_NAME_MAP, f"{settings.CHAR_NAME_MAP.name}")
        zip.write(settings.UNIHAN_CHARS_JSON, f"{settings.UNIHAN_CHARS_JSON.name}")
        zip.write(settings.TANGUT_CHARS_JSON, f"{settings.TANGUT_CHARS_JSON.name}")


def upload_zip_file_to_s3(settings: UnicodeApiSettings, local_file: Path) -> Result[None]:
    bucket_path = f"{settings.S3_BUCKET_URL}/{settings.UNICODE_VERSION}/{local_file.name}"
    result = run_command(f's3cmd --no-mime-magic --content-type="application/zip" put {local_file} {bucket_path} -P')
    if result.failure:
        return result
    return Result.Ok()
