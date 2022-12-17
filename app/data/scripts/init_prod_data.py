from pathlib import Path
from zipfile import ZipFile

from app.core.result import Result
from app.core.util import download_file

S3_BUCKET_URL = "https://unicode-api.us-southeast-1.linodeobjects.com"
UNICODE_ZIP_FILE_NAME = "unicode-api.db.zip"
DATA_FOLDER = Path(__file__).parent.parent
DB_FOLDER = DATA_FOLDER.joinpath("db")


def init_prod_data():
    result = download_unicode_db()
    if result.failure:
        return result
    unicode_db_zip = result.value

    if unicode_db_zip:
        result = extract_unicode_db(unicode_db_zip)
        if result.failure:
            return result
        unicode_db_zip.unlink()
        return Result.Ok()


def download_unicode_db() -> Result[Path]:
    url = f"{S3_BUCKET_URL}/{UNICODE_ZIP_FILE_NAME}"
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


if __name__ == "__main__":
    init_prod_data()
