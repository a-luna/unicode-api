import json
import os
import re

from lxml import html

from app.core.config import UnicodeApiSettings
from app.core.result import Result
from app.data.util import request_url_with_retries

MINIMUM_UNICODE_VERSION = 5.1
UNICODE_DIR_LINKS_XPATH = "//tr/td[2]/a/@href"
SEMVER_REGEX = re.compile(r"^(?P<major>(?:[1-9]\d*))\.(?P<minor>(?:[0-9]\d*))(?:\.(?P<patch>(?:[0-9]\d*)))?")
UNICODE_PUBLIC_DIR_URL = "https://www.unicode.org/Public/"


def bootstrap_unicode_data() -> Result[UnicodeApiSettings]:
    result = get_all_unicode_versions()
    if result.failure:
        return Result.Fail(result.error if result.error else "")
    versions = result.value or []

    if not os.environ.get("UNICODE_VERSION"):
        os.environ["UNICODE_VERSION"] = versions[-1]

    result = check_min_version(versions)
    if result.failure:
        return result

    config = UnicodeApiSettings()
    init_data_folders(config)
    if os.environ.get("ENV") == "DEV":
        create_planes_json(config)
    return Result.Ok(config)


def get_all_unicode_versions() -> Result[list[str]]:
    result = request_url_with_retries(UNICODE_PUBLIC_DIR_URL)
    if result.failure:
        return Result.Fail(result.error if result.error else "")
    response = result.value
    if not response:
        return Result.Fail("Error! No response received from request for all Unicode version numbers.")
    return parse_all_unicode_version_numbers(response.text)


def parse_all_unicode_version_numbers(page_source: str) -> Result[list[str]]:
    versions = []
    page_content = html.fromstring(page_source, base_url=UNICODE_PUBLIC_DIR_URL)
    for link in page_content.xpath(UNICODE_DIR_LINKS_XPATH):
        result = parse_semver_string(link)
        if result.failure:
            continue
        (major, minor, patch) = result.value or (0, 0, 0)
        versions.append(f"{major}.{minor}{f'.{patch}' if patch else ''}")
    return (
        Result.Ok(versions)
        if versions
        else Result.Fail("Error! Failed to parse Unicode version numbers from unicode.org")
    )


def parse_semver_string(input: str) -> Result[tuple[int, int, int]]:
    match = SEMVER_REGEX.match(input)
    if not match:
        return Result.Fail(f"'{input}' is not a valid semantic version")
    groups = match.groupdict()
    major = groups.get("major") or "0"
    minor = groups.get("minor") or "0"
    patch = groups.get("patch") or "0"
    return Result.Ok((int(major), int(minor), int(patch)))


def check_min_version(all_versions: list[str]) -> Result:
    check_version = os.environ.get("UNICODE_VERSION", "0")
    result = parse_semver_string(check_version)
    if result.failure:
        return result
    (major, minor, patch) = result.value or (0, 0, 0)
    if float(f"{major}.{minor}") >= MINIMUM_UNICODE_VERSION:
        return Result.Ok()
    error = (
        "This script parses the XML representation of the Unicode Character Database, which has been distributed "
        f"as part of the Unicode Standard since version {MINIMUM_UNICODE_VERSION}.0. The XML representation does "
        "not exist for the version of the Unicode Standard specified by the UNICODE_VERSION environment variable "
        f"(v{major}.{minor}{f'.{patch}' if patch else ''}). Please update the value of UNICODE_VERSION to any of the "
        f"following versions which include the required UCD XML files: "
        f"{', '.join(get_allowed_unicode_versions(all_versions))}"
    )
    return Result.Fail(error)


def get_allowed_unicode_versions(all_versions: list[str]) -> list[str]:
    parsed = sorted(float(f"{v}") for v in all_versions)
    return [f"{v}.0" for v in parsed if v > 5.0]


def init_data_folders(config: UnicodeApiSettings) -> None:
    config.DB_FOLDER.mkdir(parents=True, exist_ok=True)
    if config.DB_FILE.exists():
        config.DB_FILE.unlink()
    config.JSON_FOLDER.mkdir(parents=True, exist_ok=True)
    if config.PLANES_JSON.exists():
        config.PLANES_JSON.unlink()
    if config.BLOCKS_JSON.exists():
        config.BLOCKS_JSON.unlink()
    if config.CHAR_NAME_MAP.exists():
        config.CHAR_NAME_MAP.unlink()

    if os.environ.get("ENV") == "PROD":
        return

    config.CSV_FOLDER.mkdir(parents=True, exist_ok=True)
    if config.BLOCKS_CSV.exists():
        config.BLOCKS_CSV.unlink()
    if config.NAMED_CHARS_CSV.exists():
        config.NAMED_CHARS_CSV.unlink()
    if config.UNIHAN_CHARS_CSV.exists():
        config.UNIHAN_CHARS_CSV.unlink()
    if config.PLANES_CSV.exists():
        config.PLANES_CSV.unlink()


def create_planes_json(config: UnicodeApiSettings) -> None:
    planes = [
        {
            "id": 1,
            "number": 0,
            "name": "Basic Multilingual Plane",
            "abbreviation": "BMP",
            "start": "0000",
            "start_dec": 0,
            "finish": "FFFF",
            "finish_dec": 65535,
            "start_block_id": 0,
            "finish_block_id": 0,
            "total_allocated": 0,
            "total_defined": 0,
        },
        {
            "id": 2,
            "number": 1,
            "name": "Supplementary Multilingual Plane",
            "abbreviation": "SMP",
            "start": "10000",
            "start_dec": 65536,
            "finish": "1FFFF",
            "finish_dec": 131071,
            "start_block_id": 0,
            "finish_block_id": 0,
            "total_allocated": 0,
            "total_defined": 0,
        },
        {
            "id": 3,
            "number": 2,
            "name": "Supplementary Ideographic Plane",
            "abbreviation": "SIP",
            "start": "20000",
            "start_dec": 131072,
            "finish": "2FFFF",
            "finish_dec": 196607,
            "start_block_id": 0,
            "finish_block_id": 0,
            "total_allocated": 0,
            "total_defined": 0,
        },
        {
            "id": 4,
            "number": 3,
            "name": "Tertiary Ideographic Plane",
            "abbreviation": "TIP",
            "start": "30000",
            "start_dec": 196608,
            "finish": "3FFFF",
            "finish_dec": 262143,
            "start_block_id": 0,
            "finish_block_id": 0,
            "total_allocated": 0,
            "total_defined": 0,
        },
        {
            "id": 5,
            "number": 14,
            "name": "Supplementary Special-purpose Plane",
            "abbreviation": "SSP",
            "start": "E0000",
            "start_dec": 917504,
            "finish": "EFFFF",
            "finish_dec": 983039,
            "start_block_id": 0,
            "finish_block_id": 0,
            "total_allocated": 0,
            "total_defined": 0,
        },
        {
            "id": 6,
            "number": 15,
            "name": "Supplementary Private Use Area-A",
            "abbreviation": "SPUA-A",
            "start": "F0000",
            "start_dec": 983040,
            "finish": "FFFFF",
            "finish_dec": 1048575,
            "start_block_id": 0,
            "finish_block_id": 0,
            "total_allocated": 0,
            "total_defined": 0,
        },
        {
            "id": 7,
            "number": 16,
            "name": "Supplementary Private Use Area-B",
            "abbreviation": "SPUA-B",
            "start": "100000",
            "start_dec": 1048576,
            "finish": "10FFFF",
            "finish_dec": 1114111,
            "start_block_id": 0,
            "finish_block_id": 0,
            "total_allocated": 0,
            "total_defined": 0,
        },
    ]
    config.PLANES_JSON.write_text(json.dumps(planes, indent=4))
