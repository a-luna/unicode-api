"""
This module provides functionality to download and extract the Unicode XML Database from the official
Unicode Consortium website. It manages the process of downloading the Unicode XML Database ZIP file,
extracting the XML file, and cleaning up temporary files. The module also provides user feedback via
a spinner and handles errors gracefully, returning results using a custom Result type.

Functions:
    download_xml_unicode_database(settings: UnicodeApiSettings) -> Result[Path]:
        Downloads the Unicode XML Database file if it does not already exist, or uses the existing
        file in non-production environments. Handles downloading, extraction, and cleanup, providing
        user feedback and error handling.

Constants:
    UNICODE_ORG_ROOT (str): Base URL for the Unicode Consortium's public data.
    UNICODE_XML_FOLDER (str): Folder name for the Unicode XML database files.
"""

import os
from pathlib import Path
from zipfile import ZipFile, is_zipfile

from unicode_api.config.api_settings import UnicodeApiSettings
from unicode_api.core.result import Result
from unicode_api.data.util import download_file
from unicode_api.data.util.spinner import Spinner


def download_xml_unicode_database(settings: UnicodeApiSettings) -> Result[Path]:
    """
    Downloads the Unicode XML Database file if it does not already exist, or uses the existing file
    in non-production environments.

    This function manages the process of downloading the Unicode XML Database ZIP file, extracting
    the XML file from it, and cleaning up the ZIP file afterward. It provides user feedback via a
    spinner and handles errors gracefully.

    Args:
        settings (UnicodeApiSettings): The settings object containing configuration such as the
        Unicode version and file paths.

    Returns:
        Result[Path]: A Result object containing the path to the XML file on success, or an error
        message on failure.
    """
    spinner = Spinner()
    spinner.start(f"Downloading Unicode XML Database v{settings.UNICODE_VERSION}...")
    if os.environ.get("ENV") != "PROD" and settings.xml_file.exists():
        spinner.successful(f"Using existing Unicode XML Database v{settings.UNICODE_VERSION}!")
        return Result[Path].Ok(settings.xml_file)
    result = _download_unicode_xml_zip(settings)
    if result.failure:
        spinner.failed(result.error)
        return result
    if not (xml_zip := result.value):
        return Result[Path].Fail("Download attempt failed, please check internet connection.")
    result = _extract_unicode_xml_from_zip(settings)
    if result.failure:
        spinner.failed(result.error)
        return result
    if not (xml_file := result.value):
        return Result[Path].Fail("Error occurred extracting XML file from zip.")
    xml_zip.unlink()
    spinner.successful(f"Successfully downloaded Unicode XML Database v{settings.UNICODE_VERSION}!")
    return Result[Path].Ok(xml_file)


def _download_unicode_xml_zip(settings: UnicodeApiSettings) -> Result[Path]:
    result = download_file(settings.xml_db_url, settings.xml_folder)
    if result.failure:
        return result
    if not (xml_zip := result.value):
        return Result[Path].Fail("Download attempt failed, please check internet connection.")
    if not is_zipfile(xml_zip):
        return Result[Path].Fail("Zip file is possibly corrupt, the format cannot be recognized.")
    return Result[Path].Ok(xml_zip)


def _extract_unicode_xml_from_zip(settings: UnicodeApiSettings) -> Result[Path]:
    xml_file = None
    with ZipFile(settings.xml_zip_file, mode="r") as zip:
        zip.extractall(path=settings.xml_folder)
        if not (extracted_xml_files := list(settings.xml_folder.glob("*.xml"))):
            return Result[Path].Fail(f"Error occurred extracting XML file from {settings.xml_zip_file.name}!")
        if len(extracted_xml_files) != 1:
            return Result[Path].Fail(_get_extracted_file_details(settings.xml_zip_file, extracted_xml_files))
        xml_file = extracted_xml_files[0]
    return Result[Path].Ok(xml_file)


def _get_extracted_file_details(xml_zip: Path, extracted_files: list[Path]) -> str:
    error = f"{len(extracted_files)} XML files were extracted from {xml_zip.name}, expected only 1:"
    for i, file in enumerate(extracted_files, start=1):
        error += f"\n\tFile #{i}: {file.name}"
    return error
