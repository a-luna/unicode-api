from zipfile import ZipFile

from unicode_api.config.api_settings import UnicodeApiSettings, load_api_settings
from unicode_api.core.result import Result
from unicode_api.data.util import download_file


def get_prod_data() -> Result[None]:
    settings = load_api_settings()
    result = get_unicode_db(settings)
    if result.failure:
        return result

    result = get_unicode_json(settings)
    if result.failure:
        return result
    return Result[None].Ok()


def get_unicode_db(settings: UnicodeApiSettings) -> Result[None]:
    download_result = download_file(settings.db_zip_url, settings.db_folder)
    if download_result.failure:
        return Result[None].Fail(download_result.error if download_result.error else "")
    if not settings.db_zip_file.exists():
        return Result[None].Fail(f"Failed to download {settings.db_zip_file.name}")

    extract_result = extract_unicode_db(settings)
    if extract_result.failure:
        return Result[None].Fail(extract_result.error if extract_result.error else "")
    settings.db_zip_file.unlink()
    return Result[None].Ok()


def extract_unicode_db(settings: UnicodeApiSettings) -> Result[None]:
    with ZipFile(settings.db_zip_file, mode="r") as zip:
        zip.extractall(path=str(settings.db_folder))
        extracted_files = list(settings.db_folder.glob("*.db"))
        if not extracted_files:
            return Result[None].Fail(f"Error occurred extracting Unicode DB from {settings.db_zip_file.name}!")
        if len(extracted_files) != 1:
            error = f"{len(extracted_files)} files were extracted from {settings.db_zip_file.name}, expected 1:\n"
            for i, file in enumerate(extracted_files, start=1):
                error += f"\tFile #{i}: {file.name}"
            return Result[None].Fail(error)
        return Result[None].Ok()


def get_unicode_json(settings: UnicodeApiSettings) -> Result[None]:
    download_result = download_file(settings.json_zip_url, settings.json_folder)
    if download_result.failure:
        return Result[None].Fail(download_result.error if download_result.error else "")
    if not settings.json_zip_file.exists():
        return Result[None].Fail(f"Failed to download {settings.json_zip_file.name}")

    extract_result = extract_unicode_json(settings)
    if extract_result.failure:
        return Result[None].Fail(extract_result.error if extract_result.error else "")
    settings.json_zip_file.unlink()
    return Result[None].Ok()


def extract_unicode_json(settings: UnicodeApiSettings) -> Result[None]:
    with ZipFile(settings.json_zip_file, mode="r") as zip:
        zip.extractall(path=str(settings.json_folder))
        extracted_files = list(settings.json_folder.glob("*.json"))
        if not extracted_files:
            return Result[None].Fail(f"Error occurred extracting Unicode DB from {settings.json_zip_file.name}!")
        if len(extracted_files) != 3:
            error = f"{len(extracted_files)} files were extracted from {settings.json_zip_file.name}, expected 3:\n"
            for i, file in enumerate(extracted_files, start=1):
                error += f"\tFile #{i}: {file.name}"
            return Result[None].Fail(error)
        return Result[None].Ok()


if __name__ == "__main__":
    get_prod_data()
