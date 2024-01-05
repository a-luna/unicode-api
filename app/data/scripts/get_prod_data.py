import logging
from pathlib import Path
from zipfile import ZipFile

from app.config import UnicodeApiSettings
from app.core.result import Result
from app.data.scripts.bootstrap_unicode_data import bootstrap_unicode_data
from app.data.util import download_file


def get_prod_data() -> Result[None]:
    result = bootstrap_unicode_data()
    if result.failure or not result.value:
        return Result.Fail(result.error if result.error else "")
    settings = result.value

    logger = logging.getLogger("app.api")
    logger.info(
        "Begin Process: Bootstrap Unicode Data (ENV: ${settings.ENV}, UNICODE_VERSION: ${settings.UNICODE_VERSION})"
    )

    result = get_unicode_db(settings)
    if result.failure:
        return result

    result = get_unicode_json(settings)
    if result.failure:
        return result
    return Result.Ok()


def get_unicode_db(settings: UnicodeApiSettings) -> Result[None]:
    result = download_file(settings.DB_ZIP_URL, settings.DB_FOLDER)
    if result.failure:
        return Result.Fail(result.error if result.error else "")
    if not settings.DB_ZIP_FILE.exists():
        return Result.Fail(f"Failed to download {settings.DB_ZIP_FILE.name}")

    result = extract_unicode_db(settings)
    if result.failure:
        return Result.Fail(result.error if result.error else "")
    settings.DB_ZIP_FILE.unlink()
    return Result.Ok()


def extract_unicode_db(settings: UnicodeApiSettings) -> Result[list[Path]]:
    with ZipFile(settings.DB_ZIP_FILE, mode="r") as zip:
        zip.extractall(path=str(settings.DB_FOLDER))
        extracted_files = list(settings.DB_FOLDER.glob("*.db"))
        if not extracted_files:
            return Result.Fail(f"Error occurred extracting Unicode DB from {settings.DB_ZIP_FILE.name}!")
        if len(extracted_files) != 1:
            error = f"{len(extracted_files)} files were extracted from {settings.DB_ZIP_FILE.name}, expected 1:\n"
            for i, file in enumerate(extracted_files, start=1):
                error += f"\tFile #{i}: {file.name}"
            return Result.Fail(error)
        return Result.Ok(extracted_files)


def get_unicode_json(settings: UnicodeApiSettings) -> Result[None]:
    result = download_file(settings.JSON_ZIP_URL, settings.JSON_FOLDER)
    if result.failure:
        return Result.Fail(result.error if result.error else "")
    if not settings.JSON_ZIP_FILE.exists():
        return Result.Fail(f"Failed to download {settings.JSON_ZIP_FILE.name}")
    result = extract_unicode_json(settings)
    if result.failure:
        return Result.Fail(result.error if result.error else "")
    settings.JSON_ZIP_FILE.unlink()
    return Result.Ok()


def extract_unicode_json(settings: UnicodeApiSettings) -> Result[list[Path]]:
    with ZipFile(settings.JSON_ZIP_FILE, mode="r") as zip:
        zip.extractall(path=str(settings.JSON_FOLDER))
        extracted_files = list(settings.JSON_FOLDER.glob("*.json"))
        if not extracted_files:
            return Result.Fail(f"Error occurred extracting Unicode DB from {settings.JSON_ZIP_FILE.name}!")
        if len(extracted_files) != 3:
            error = f"{len(extracted_files)} files were extracted from {settings.JSON_ZIP_FILE.name}, expected 3:\n"
            for i, file in enumerate(extracted_files, start=1):
                error += f"\tFile #{i}: {file.name}"
            return Result.Fail(error)
        return Result.Ok(extracted_files)


if __name__ == "__main__":
    get_prod_data()
