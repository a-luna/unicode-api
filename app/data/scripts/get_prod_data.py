from pathlib import Path
from zipfile import ZipFile

from app.core.result import Result
from app.core.util import download_file

S3_BUCKET_URL = "https://unicode-api.us-southeast-1.linodeobjects.com"
UNICODE_DB_ZIP_FILE = "unicode-api.db.zip"
UNICODE_JSON_ZIP_FILE = "unicode_json.zip"
DATA_FOLDER = Path(__file__).parent.parent
JSON_FOLDER = DATA_FOLDER.joinpath("json")
DB_FOLDER = DATA_FOLDER.joinpath("db")


def init_prod_data():
    DB_FOLDER.mkdir(parents=True, exist_ok=True)
    result = download_unicode_db()
    if result.failure:
        return result
    unicode_db_zip = result.value

    JSON_FOLDER.mkdir(parents=True, exist_ok=True)
    result = download_unicode_json()
    if result.failure:
        return result
    unicode_json_zip = result.value

    if unicode_db_zip and unicode_db_zip.exists():
        result = extract_unicode_db(unicode_db_zip)
        if result.failure:
            return result
        unicode_db_zip.unlink()

    if unicode_json_zip and unicode_json_zip.exists():
        result = extract_unicode_json(unicode_json_zip)
        if result.failure:
            return result
        unicode_json_zip.unlink()

    return Result.Ok()


def download_unicode_db() -> Result[Path]:
    url = f"{S3_BUCKET_URL}/{UNICODE_DB_ZIP_FILE}"
    return download_file(url, DB_FOLDER)


def download_unicode_json() -> Result[Path]:
    url = f"{S3_BUCKET_URL}/{UNICODE_JSON_ZIP_FILE}"
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
    init_prod_data()
