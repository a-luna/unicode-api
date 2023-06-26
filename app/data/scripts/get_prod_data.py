from pathlib import Path
from zipfile import ZipFile

from app.core.config import UnicodeApiSettings
from app.core.result import Result
from app.data.scripts import bootstrap_unicode_data
from app.data.util import download_file


def get_prod_data():
    result = bootstrap_unicode_data()
    if result.failure or not result.value:
        return result
    config = result.value

    result = get_unicode_db(config)
    if result.failure:
        return result

    result = get_unicode_json(config)
    if result.failure:
        return result
    return Result.Ok()


def get_unicode_db(config: UnicodeApiSettings) -> Result:
    result = download_file(config.DB_ZIP_URL, config.DB_FOLDER)
    if result.failure:
        return result
    if not config.DB_ZIP_FILE.exists():
        return Result.Fail(f"Failed to download {config.DB_ZIP_FILE.name}")

    result = extract_unicode_db(config)
    if result.failure:
        return result
    config.DB_ZIP_FILE.unlink()
    return Result.Ok()


def extract_unicode_db(config: UnicodeApiSettings) -> Result[list[Path]]:
    with ZipFile(config.DB_ZIP_FILE, mode="r") as zip:
        zip.extractall(path=str(config.DB_FOLDER))
        extracted_files = list(config.DB_FOLDER.glob("*.db"))
        if not extracted_files:
            return Result.Fail(f"Error occurred extracting Unicode DB from {config.DB_ZIP_FILE.name}!")
        if len(extracted_files) != 1:
            error = f"{len(extracted_files)} files were extracted from {config.DB_ZIP_FILE.name}, expected 1:\n"
            for i, file in enumerate(extracted_files, start=1):
                error += f"\tFile #{i}: {file.name}"
            return Result.Fail(error)
        return Result.Ok(extracted_files)


def get_unicode_json(config: UnicodeApiSettings) -> Result:
    result = download_file(config.JSON_ZIP_URL, config.JSON_FOLDER)
    if result.failure:
        return result
    if not config.JSON_ZIP_FILE.exists():
        return Result.Fail(f"Failed to download {config.JSON_ZIP_FILE.name}")
    result = extract_unicode_json(config)
    if result.failure:
        return result
    config.JSON_ZIP_FILE.unlink()
    return Result.Ok()


def extract_unicode_json(config: UnicodeApiSettings) -> Result[list[Path]]:
    with ZipFile(config.JSON_ZIP_FILE, mode="r") as zip:
        zip.extractall(path=str(config.JSON_FOLDER))
        extracted_files = list(config.JSON_FOLDER.glob("*.json"))
        if not extracted_files:
            return Result.Fail(f"Error occurred extracting Unicode DB from {config.JSON_ZIP_FILE.name}!")
        if len(extracted_files) != 4:
            error = f"{len(extracted_files)} files were extracted from {config.JSON_ZIP_FILE.name}, expected 4:\n"
            for i, file in enumerate(extracted_files, start=1):
                error += f"\tFile #{i}: {file.name}"
            return Result.Fail(error)
        return Result.Ok(extracted_files)


if __name__ == "__main__":
    get_prod_data()
