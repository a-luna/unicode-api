import os
import re

from app.config.api_settings import UnicodeApiSettings, get_settings
from app.constants import SUPPORTED_UNICODE_VERSIONS
from app.core.result import Result

SEMVER_REGEX = re.compile(r"^(?P<major>(?:[1-9]\d*))\.(?P<minor>(?:[0-9]\d*))(?:\.(?P<patch>(?:[0-9]\d*)))?")


def get_api_settings() -> Result[UnicodeApiSettings]:
    if version := os.environ.get("UNICODE_VERSION"):
        result = check_min_version(version)
        if result.failure:
            return Result.Fail(result.error)
    else:
        os.environ["UNICODE_VERSION"] = SUPPORTED_UNICODE_VERSIONS[-1]
    settings = get_settings()
    settings.init_data_folders()
    return Result.Ok(settings)


def check_min_version(check_version: str) -> Result[None]:
    result = parse_semver_string(check_version)
    if result.failure:
        return Result.Fail(result.error)
    parsed_version = result.value
    if parsed_version in SUPPORTED_UNICODE_VERSIONS:
        return Result.Ok()
    error = (
        "This script parses the XML representation of the Unicode Character Database, which has been distributed "
        f"as part of the Unicode Standard since version {SUPPORTED_UNICODE_VERSIONS[0]}. The XML representation does "
        "not exist for the version of the Unicode Standard specified by the UNICODE_VERSION environment variable "
        f"($UNICODE_VERSION = v{check_version}). Please update the value of the UNICODE_VERSION env var to any of "
        f"the following valid version numbers: {', '.join(SUPPORTED_UNICODE_VERSIONS)}"
    )
    return Result.Fail(error)


def parse_semver_string(input: str) -> Result[str]:
    match = SEMVER_REGEX.match(input)
    if not match:
        return Result.Fail(f"'{input}' is not a valid semantic version")
    groups = match.groupdict()
    major, minor, patch = (int(groups.get("major", "0")), int(groups.get("minor", "0")), int(groups.get("patch", "0")))
    return Result.Ok(f"{major}.{minor}.{patch}")
