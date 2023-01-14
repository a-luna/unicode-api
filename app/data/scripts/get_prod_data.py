from pathlib import Path
from zipfile import ZipFile

from app.core.result import Result
from app.data.scripts.util import download_file

S3_BUCKET_URL = "https://unicode-api.us-southeast-1.linodeobjects.com"
UNICODE_DB_ZIP_FILE = "unicode-api.db.zip"
UNICODE_JSON_ZIP_FILE = "unicode_json.zip"
DATA_FOLDER = Path(__file__).parent.parent
JSON_FOLDER = DATA_FOLDER.joinpath("json")
DB_FOLDER = DATA_FOLDER.joinpath("db")


def get_prod_data():
    get_db_result = get_unicode_db()
    if get_db_result.failure:
        return get_db_result
    get_json_result = get_unicode_json()
    if get_json_result.failure:
        return get_json_result
    return Result.Ok()


def get_unicode_db() -> Result:
    DB_FOLDER.mkdir(parents=True, exist_ok=True)
    download_result = download_unicode_db_zip()
    if download_result.failure:
        return download_result
    unicode_db_zip = download_result.value
    if not unicode_db_zip or not unicode_db_zip.exists():
        return Result.Fail(f"Failed to download {UNICODE_DB_ZIP_FILE}")
    extract_result = extract_unicode_db(unicode_db_zip)
    if extract_result.failure:
        return extract_result
    unicode_db_zip.unlink()
    return Result.Ok()


def download_unicode_db_zip() -> Result[Path]:
    url = f"{S3_BUCKET_URL}/{UNICODE_DB_ZIP_FILE}"
    return download_file(url, DB_FOLDER)


def extract_unicode_db(unicode_db_zip: Path) -> Result[list[Path]]:
    with ZipFile(unicode_db_zip, mode="r") as zip:
        zip.extractall(path=str(DB_FOLDER))
        extracted_files = list(DB_FOLDER.glob("*.db"))
        if not extracted_files:
            return Result.Fail(f"Error occurred extracting Unicode DB from {unicode_db_zip.name}!")
        if len(extracted_files) != 1:
            error = f"{len(extracted_files)} files were extracted from {unicode_db_zip.name}, expected 1:\n"
            for i, file in enumerate(extracted_files, start=1):
                error += f"\tFile #{i}: {file.name}"
            return Result.Fail(error)
        return Result.Ok(extracted_files)


def get_unicode_json() -> Result:
    JSON_FOLDER.mkdir(parents=True, exist_ok=True)
    download_result = download_unicode_json_zip()
    if download_result.failure:
        return download_result
    unicode_json_zip = download_result.value
    if not unicode_json_zip or not unicode_json_zip.exists():
        return Result.Fail(f"Failed to download {UNICODE_JSON_ZIP_FILE}")
    extract_result = extract_unicode_json(unicode_json_zip)
    if extract_result.failure:
        return extract_result
    unicode_json_zip.unlink()
    return Result.Ok()


def download_unicode_json_zip() -> Result[Path]:
    url = f"{S3_BUCKET_URL}/{UNICODE_JSON_ZIP_FILE}"
    return download_file(url, JSON_FOLDER)


def extract_unicode_json(unicode_json_zip: Path) -> Result[list[Path]]:
    with ZipFile(unicode_json_zip, mode="r") as zip:
        zip.extractall(path=str(JSON_FOLDER))
        extracted_files = list(JSON_FOLDER.glob("*.json"))
        if not extracted_files:
            return Result.Fail(f"Error occurred extracting Unicode DB from {unicode_json_zip.name}!")
        if len(extracted_files) != 4:
            error = f"{len(extracted_files)} files were extracted from {unicode_json_zip.name}, expected 4:\n"
            for i, file in enumerate(extracted_files, start=1):
                error += f"\tFile #{i}: {file.name}"
            return Result.Fail(error)
        return Result.Ok(extracted_files)


if __name__ == "__main__":
    get_prod_data()
