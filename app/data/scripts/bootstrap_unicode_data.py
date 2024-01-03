import os
import re

from app.config import UnicodeApiSettings, get_settings
from app.core.result import Result
from app.data.constants import SUPPORTED_UNICODE_VERSIONS

SEMVER_REGEX = re.compile(r"^(?P<major>(?:[1-9]\d*))\.(?P<minor>(?:[0-9]\d*))(?:\.(?P<patch>(?:[0-9]\d*)))?")


def bootstrap_unicode_data() -> Result[UnicodeApiSettings]:
    if os.environ.get("UNICODE_VERSION"):
        result = check_min_version()
        if result.failure:
            return Result.Fail(result.error if result.error else "")
    else:
        os.environ["UNICODE_VERSION"] = SUPPORTED_UNICODE_VERSIONS[-1]

    config = get_settings()
    config.init_data_folders()
    return Result.Ok(config)


def check_min_version() -> Result[None]:
    check_version = os.environ.get("UNICODE_VERSION", "0")
    match = SEMVER_REGEX.match(check_version)
    if not match:
        return Result.Fail(f"'{check_version}' is not a valid semantic version number")
    if check_version in SUPPORTED_UNICODE_VERSIONS:
        return Result.Ok()
    error = (
        "This script parses the XML representation of the Unicode Character Database, which has been distributed "
        f"as part of the Unicode Standard since version {SUPPORTED_UNICODE_VERSIONS[0]}. The XML representation does "
        "not exist for the version of the Unicode Standard specified by the UNICODE_VERSION environment variable "
        f"($UNICODE_VERSION = v{check_version}). Please update the value of the UNICODE_VERSION env var to any of "
        f"the following valid version numbers: {', '.join(SUPPORTED_UNICODE_VERSIONS)}"
    )
    return Result.Fail(error)
