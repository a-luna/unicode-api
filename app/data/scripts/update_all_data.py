import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from app.core.config import BLOCKS_JSON, CHARACTERS_JSON, JSON_FOLDER, PLANES_JSON, S3_BUCKET_URL
from app.core.result import Result
from app.core.util import run_command
from app.data.scripts.get_unicode_db import get_xml_unicode_database
from app.data.scripts.xml_parser import parse_unicode_data_from_xml


def update_all_data(version: str):
    get_xml_result = get_xml_unicode_database(version)
    if get_xml_result.failure:
        return get_xml_result
    xml_file = get_xml_result.value

    result = parse_unicode_data_from_xml(xml_file)
    if result.failure:
        return result
    (all_planes, all_blocks, all_chars) = result.value

    update_unicode_json_files(all_planes, all_blocks, all_chars)
    zip_file = create_unicode_json_zip_file()
    result = upload_zip_file_to_s3(zip_file)
    if result.failure:
        return result
    return Result.Ok()


def update_unicode_json_files(all_planes, all_blocks, all_chars):
    PLANES_JSON.write_text(json.dumps(all_planes, indent=4))
    BLOCKS_JSON.write_text(json.dumps(all_blocks, indent=4))
    CHARACTERS_JSON.write_text(json.dumps(all_chars, indent=4))


def create_unicode_json_zip_file():
    zip_file = JSON_FOLDER.joinpath("unicode_json.zip")
    with ZipFile(zip_file, "w", ZIP_DEFLATED) as zip:
        zip.write(PLANES_JSON, f"{PLANES_JSON. name}")
        zip.write(BLOCKS_JSON, f"{BLOCKS_JSON.name}")
        zip.write(CHARACTERS_JSON, f"{CHARACTERS_JSON.name}")
    return zip_file


def upload_zip_file_to_s3(zip_file: Path):
    result = run_command(f"s3cmd put {zip_file} {S3_BUCKET_URL} -P")
    if result.failure:
        return result
    zip_file.unlink()
    return Result.Ok()
