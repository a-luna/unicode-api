"""
This module provides functionality to retrieve and initialize Unicode API settings
based on the "UNICODE_VERSION" environment variable. It validates the specified
Unicode version against supported versions, ensures required data folders are
initialized, and returns the settings wrapped in a Result object.

Functions:
    get_api_settings() -> Result[UnicodeApiSettings]:
        Retrieves and initializes the Unicode API settings, validating the
        Unicode version from the environment or defaulting to the latest
        supported version.
"""

import os
import re

from unicode_api.config.api_settings import UnicodeApiSettings, get_settings
from unicode_api.constants import SUPPORTED_UNICODE_VERSIONS
from unicode_api.core.result import Result

SEMVER_REGEX = re.compile(r"^(?P<major>(?:[1-9]\d*))\.(?P<minor>(?:[0-9]\d*))(?:\.(?P<patch>(?:[0-9]\d*)))?")


def get_api_settings() -> Result[UnicodeApiSettings]:
    """
    Retrieves and initializes the Unicode API settings.

    Checks the "UNICODE_VERSION" environment variable for a valid Unicode version.
    If not set, defaults to the latest supported version. Validates the version,
    initializes required data folders, and returns the settings wrapped in a Result.

    Returns:
        Result[UnicodeApiSettings]: A Result containing the initialized settings on success,
        or a failure with an error message if the version check fails.
    """
    if version := os.environ.get("UNICODE_VERSION"):
        result = _check_min_version(version)
        if result.failure:
            return Result[UnicodeApiSettings].Fail(result.error)
    else:
        os.environ["UNICODE_VERSION"] = SUPPORTED_UNICODE_VERSIONS[-1]
    settings = get_settings()
    settings.init_data_folders()
    return Result[UnicodeApiSettings].Ok(settings)


def _check_min_version(check_version: str) -> Result[None]:
    result = _parse_semver_string(check_version)
    if result.failure:
        return Result[None].Fail(result.error)
    parsed_version = result.value
    if parsed_version in SUPPORTED_UNICODE_VERSIONS:
        return Result[None].Ok()
    error = (
        "This script parses the XML representation of the Unicode Character Database, which has been distributed "
        f"as part of the Unicode Standard since version {SUPPORTED_UNICODE_VERSIONS[0]}. The XML representation does "
        "not exist for the version of the Unicode Standard specified by the UNICODE_VERSION environment variable "
        f"($UNICODE_VERSION = v{check_version}). Please update the value of the UNICODE_VERSION env var to any of "
        f"the following valid version numbers: {', '.join(SUPPORTED_UNICODE_VERSIONS)}"
    )
    return Result[None].Fail(error)


def _parse_semver_string(input: str) -> Result[str]:
    match = SEMVER_REGEX.match(input)
    if not match:
        return Result[str].Fail(f"'{input}' is not a valid semantic version")
    groups = match.groupdict()
    major, minor, patch = (int(groups.get("major", "0")), int(groups.get("minor", "0")), int(groups.get("patch", "0")))
    return Result[str].Ok(f"{major}.{minor}.{patch}")
