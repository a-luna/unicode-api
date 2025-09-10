"""
This module provides functionality to create compressed backup files of the SQLite database and related JSON files,
upload them to an S3 bucket, and remove the local backup files upon successful upload.

Functions:
    backup_db_and_json_files(settings: UnicodeApiSettings) -> Result[None]:
        Creates compressed backup files of the SQLite database and JSON files, uploads them to an S3 bucket,
        and removes local backup files upon successful upload.
"""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from unicode_api.config.api_settings import UnicodeApiSettings
from unicode_api.core.result import Result
from unicode_api.data.util.command import run_command
from unicode_api.data.util.spinner import Spinner


def backup_db_and_json_files(settings: UnicodeApiSettings) -> Result[None]:
    """
    Creates compressed backup files of the SQLite database and JSON files, uploads them to an S3 bucket,
    and removes local backup files upon successful upload.

    Args:
        settings (UnicodeApiSettings): The application settings containing paths and configuration for
        backup and upload.

    Returns:
        Result[None]: A Result object indicating success or failure. On failure, contains an error message.
    """
    spinner = Spinner()
    spinner.start("Creating compressed backup files of SQLite DB and JSON files...")
    _backup_sqlite_db(settings)
    _backup_json_files(settings)
    spinner.successful("Successfully created compressed backup files of SQLite DB and JSON files!")

    spinner = Spinner()
    result = _upload_zip_file_to_s3(settings, settings.db_zip_file)
    if result.failure:
        spinner.start("")
        spinner.failed(result.error)
        return result
    settings.db_zip_file.unlink()

    result = _upload_zip_file_to_s3(settings, settings.json_zip_file)
    if result.failure:
        spinner.start("")
        spinner.failed(result.error)
        return result
    settings.json_zip_file.unlink()
    spinner.start("")
    spinner.successful("Successfully uploaded backup files to S3 bucket!")
    return Result[None].Ok()


def _backup_sqlite_db(settings: UnicodeApiSettings):
    with ZipFile(settings.db_zip_file, "w", ZIP_DEFLATED) as zip:
        zip.write(settings.db_file, f"{settings.db_file.name}")


def _backup_json_files(settings: UnicodeApiSettings):
    zip_file = settings.json_folder.joinpath("unicode_json.zip")
    with ZipFile(zip_file, "w", ZIP_DEFLATED) as zip:
        zip.write(settings.prop_values_json, f"{settings.prop_values_json.name}")
        zip.write(settings.planes_json, f"{settings.planes_json.name}")
        zip.write(settings.blocks_json, f"{settings.blocks_json.name}")
        zip.write(settings.char_name_map, f"{settings.char_name_map.name}")
        zip.write(settings.unihan_chars_json, f"{settings.unihan_chars_json.name}")
        zip.write(settings.tangut_chars_json, f"{settings.tangut_chars_json.name}")


def _upload_zip_file_to_s3(settings: UnicodeApiSettings, local_file: Path) -> Result[None]:
    bucket_path = f"{settings.s3_bucket_url}/{settings.UNICODE_VERSION}/{local_file.name}"
    result = run_command(f's3cmd --no-mime-magic --content-type="application/zip" put {local_file} {bucket_path} -P')
    if result.failure:
        return result
    return Result[None].Ok()
