import os
from pathlib import Path
from zipfile import ZipFile, is_zipfile

from app.config.api_settings import UnicodeApiSettings
from app.core.result import Result
from app.data.util import download_file
from app.data.util.spinners import Spinner

UNICODE_ORG_ROOT = "https://www.unicode.org/Public"
UNICODE_XML_FOLDER = "ucdxml"


def download_xml_unicode_database(settings: UnicodeApiSettings) -> Result[Path]:
    spinner = Spinner()
    spinner.start(f"Downloading Unicode XML Database v{settings.UNICODE_VERSION}...")
    if os.environ.get("ENV") != "PROD" and settings.XML_FILE.exists():
        spinner.successful(f"Using existing Unicode XML Database v{settings.UNICODE_VERSION}!")
        return Result.Ok(settings.XML_FILE)
    result = download_unicode_xml_zip(settings)
    if result.failure:
        spinner.failed(result.error)
        return result
    if not (xml_zip := result.value):
        return Result.Fail("Download attempt failed, please check internet connection.")
    result = extract_unicode_xml_from_zip(settings)
    if result.failure:
        spinner.failed(result.error)
        return result
    if not (xml_file := result.value):
        return Result.Fail("Error occurred extracting XML file from zip.")
    xml_zip.unlink()
    spinner.successful(f"Successfully downloaded Unicode XML Database v{settings.UNICODE_VERSION}!")
    return Result.Ok(xml_file)


def download_unicode_xml_zip(settings: UnicodeApiSettings) -> Result[Path]:
    result = download_file(settings.XML_DB_URL, settings.XML_FOLDER)
    if result.failure:
        return result
    if not (xml_zip := result.value):
        return Result.Fail("Download attempt failed, please check internet connection.")
    if not is_zipfile(xml_zip):
        return Result.Fail("Zip file is possibly corrupt, the format cannot be recognized.")
    return Result.Ok(xml_zip)


def extract_unicode_xml_from_zip(settings: UnicodeApiSettings) -> Result[Path]:
    xml_file = None
    with ZipFile(settings.XML_ZIP_FILE, mode="r") as zip:
        zip.extractall(path=settings.XML_FOLDER)
        if not (extracted_xml_files := list(settings.XML_FOLDER.glob("*.xml"))):
            return Result.Fail(f"Error occurred extracting XML file from {settings.XML_ZIP_FILE.name}!")
        if len(extracted_xml_files) != 1:
            return Result.Fail(get_extracted_file_details(settings.XML_ZIP_FILE, extracted_xml_files))
        xml_file = extracted_xml_files[0]
    return Result.Ok(xml_file)


def get_extracted_file_details(xml_zip: Path, extracted_files: list[Path]) -> str:
    error = f"{len(extracted_files)} XML files were extracted from {xml_zip.name}, expected only 1:"
    for i, file in enumerate(extracted_files, start=1):
        error += f"\n\tFile #{i}: {file.name}"
    return error
