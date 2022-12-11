from pathlib import Path
from zipfile import ZipFile
from app.core.result import Result
from app.core.util import download_file

S3_BUCKET_URL = "https://unicode-api.us-southeast-1.linodeobjects.com"
UNICODE_ZIP_FILE_NAME = "unicode_json.zip"
DATA_FOLDER = Path(__file__).parent.parent
JSON_FOLDER = DATA_FOLDER.joinpath("json")


def init_prod_data():
    result = download_unicode_json_zip()
    if result.failure:
        return result
    unicode_json_zip = result.value

    result = extract_unicode_json_files(unicode_json_zip)
    if result.failure:
        return result
    unicode_json_zip.unlink()
    return Result.Ok()


def download_unicode_json_zip() -> Result[Path]:
    url = f"{S3_BUCKET_URL}/{UNICODE_ZIP_FILE_NAME}"
    return download_file(url, JSON_FOLDER)


def extract_unicode_json_files(unicode_json_zip: Path) -> Result[list[Path]]:
    with ZipFile(unicode_json_zip, mode="r") as zip:
        zip.extractall(path=str(JSON_FOLDER))
        extracted_json_files = list(JSON_FOLDER.glob("*.json"))
        if not extracted_json_files:
            return Result.Fail(f"Error occurred extracting JSON files from {unicode_json_zip.name}!")
        if len(extracted_json_files) != 3:
            error = f"{len(extracted_json_files)} XML files were extracted from {unicode_json_zip.name}, expected 3:\n"
            for i, file in enumerate(extracted_json_files, start=1):
                error += f"\tFile #{i}: {file.name}"
            return Result.Fail(error)
        return Result.Ok(extracted_json_files)
