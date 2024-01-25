import os
from pathlib import Path
from zipfile import ZipFile, is_zipfile

from app.config.api_settings import UnicodeApiSettings
from app.core.result import Result
from app.data.util import download_file

UNICODE_ORG_ROOT = "https://www.unicode.org/Public"
UNICODE_XML_FOLDER = "ucdxml"


def download_xml_unicode_database(config: UnicodeApiSettings) -> Result[Path]:
    if os.environ.get("ENV") != "PROD" and config.XML_FILE.exists():
        return Result.Ok(config.XML_FILE)
    result = download_unicode_xml_zip(config)
    if result.failure or not result.value:
        return result
    xml_zip = result.value
    result = extract_unicode_xml_from_zip(config)
    if result.failure or not result.value:
        return result
    xml_file = result.value
    xml_zip.unlink()
    return Result.Ok(xml_file)


def download_unicode_xml_zip(config: UnicodeApiSettings) -> Result[Path]:
    result = download_file(config.XML_DB_URL, config.XML_FOLDER)
    if result.failure:
        return result
    xml_zip = result.value
    if not xml_zip:
        return Result.Fail("Download attempt failed, please check internet connection.")
    if not is_zipfile(xml_zip):
        return Result.Fail("Zip file is possibly corrupt, the format cannot be recognized.")
    return Result.Ok(xml_zip)


def extract_unicode_xml_from_zip(config: UnicodeApiSettings) -> Result[Path]:
    xml_file = None
    with ZipFile(config.XML_ZIP_FILE, mode="r") as zip:
        zip.extractall(path=config.XML_FOLDER)
        extracted_xml_files = list(config.XML_FOLDER.glob("*.xml"))
        if not extracted_xml_files:
            return Result.Fail(f"Error occurred extracting XML file from {config.XML_ZIP_FILE.name}!")
        if len(extracted_xml_files) != 1:
            return Result.Fail(get_extracted_file_details(config.XML_ZIP_FILE, extracted_xml_files))
        xml_file = extracted_xml_files[0]
    return Result.Ok(xml_file)


def get_extracted_file_details(xml_zip: Path, extracted_files: list[Path]) -> str:
    error = f"{len(extracted_files)} XML files were extracted from {xml_zip.name}, expected only 1:\n"
    for i, file in enumerate(extracted_files, start=1):
        error += f"\tFile #{i}: {file.name}"
    return error
