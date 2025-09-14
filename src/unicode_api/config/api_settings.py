import json
import os
import re
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import TYPE_CHECKING

from unicode_api.config.dotenv_file import load_dotenv_file
from unicode_api.constants import (
    ENV_DEV,
    ENV_PROD,
    ENV_TEST,
    PROP_GROUP_VALUE_MAP_DEFAULT,
    SUPPORTED_UNICODE_VERSION_RELEASE_DATES,
    UNICODE_PLANES_DEFAULT,
)
from unicode_api.core.util import s

if TYPE_CHECKING:  # pragma: no cover
    from unicode_api.custom_types import UnicodePropertyGroupMap


UNICODE_ORG_ROOT = "https://www.unicode.org/Public"
UNICODE_TXT_FOLDER = "ucd"
UNICODE_XML_FOLDER = "ucdxml"
HTTP_BUCKET_URL = "https://unicode-api.us-southeast-1.linodeobjects.com"
S3_BUCKET_URL = "s3://unicode-api"

PROP_VALUES_FILE_NAME = "PropertyValueAliases.txt"
XML_FILE_NAME = "ucd.all.flat.xml"
XML_ZIP_FILE_NAME = "ucd.all.flat.zip"
DB_FILE_NAME = "unicode-api.db"
DB_ZIP_FILE_NAME = "unicode-api.db.zip"
JSON_ZIP_FILE_NAME = "unicode_json.zip"

APP_FOLDER = Path(__file__).parent.parent
ROOT_FOLDER = APP_FOLDER.parent.parent
DOTENV_FILE = ROOT_FOLDER.joinpath(".env")


def get_latest_unicode_version() -> str:  # pragma: no cover
    all_versions = (
        (released, version)
        for version, released in SUPPORTED_UNICODE_VERSION_RELEASE_DATES.items()
        if released <= date.today()
    )
    (_, latest_version) = sorted(all_versions)[-1]
    return latest_version


@dataclass
class UnicodeApiSettings:
    """
    Configuration settings for the Unicode API application.

    Manages environment-specific settings, file paths, database connections,
    and rate limiting configuration.

    Key responsibilities:
    - Environment detection (dev/prod/test)
    - Path management for Unicode data files
    - Database and Redis connection settings
    - Rate limiting configuration
    """

    ENV: str
    HOSTNAME: str
    API_VERSION: str
    UNICODE_VERSION: str
    REDIS_PW: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    RATE_LIMIT_PER_PERIOD: int
    RATE_LIMIT_PERIOD_SECONDS: timedelta
    RATE_LIMIT_BURST: int
    UMAMI_WEBSITE_ID: str
    UMAMI_API_URL: str
    DOCKER_IP_OCTET_1: int
    DOCKER_IP_OCTET_2: int
    DOCKER_IP_OCTET_3: int
    api_root: str = field(init=False, default="")
    project_name: str = field(init=False, default="")
    root_folder: Path = field(init=False)
    app_folder: Path = field(init=False)
    data_folder: Path = field(init=False)
    tests_folder: Path = field(init=False)
    version_folder: Path = field(init=False)
    txt_folder: Path = field(init=False)
    prop_values_url: str = field(init=False, default="")
    prop_values_file: Path = field(init=False)
    xml_folder: Path = field(init=False)
    xml_file: Path = field(init=False)
    xml_zip_file: Path = field(init=False)
    xml_db_url: str = field(init=False, default="")
    db_folder: Path = field(init=False)
    db_file: Path = field(init=False)
    db_zip_file: Path = field(init=False)
    db_zip_url: str = field(init=False, default="")
    db_url: str = field(init=False, default="")
    db_uri: str = field(init=False, default="")
    s3_bucket_url: str = field(init=False, default="")
    json_folder: Path = field(init=False)
    prop_values_json: Path = field(init=False)
    planes_json: Path = field(init=False)
    blocks_json: Path = field(init=False)
    char_name_map: Path = field(init=False)
    unihan_chars_json: Path = field(init=False)
    tangut_chars_json: Path = field(init=False)
    json_zip_file: Path = field(init=False)
    json_zip_url: str = field(init=False, default="")

    def __post_init__(self) -> None:
        data_folder = APP_FOLDER.joinpath("data")
        version_folder = data_folder.joinpath("unicode_versions").joinpath(self.UNICODE_VERSION)
        txt_folder = version_folder.joinpath("txt")
        xml_folder = version_folder.joinpath("xml")
        db_folder = version_folder.joinpath("db")
        json_folder = version_folder.joinpath("json")
        http = "https" if "PROD" in self.ENV else "http"
        port = "" if "PROD" in self.ENV else ":3507"

        self.api_root = f"{http}://{self.HOSTNAME}{port}"
        self.project_name = f"Unicode API{'' if 'PROD' in self.ENV else f' ({self.ENV})'}"
        self.root_folder = ROOT_FOLDER
        self.app_folder = APP_FOLDER
        self.data_folder = data_folder
        self.tests_folder = ROOT_FOLDER.joinpath("tests")
        self.version_folder = version_folder
        self.txt_folder = txt_folder
        self.prop_values_url = f"{UNICODE_ORG_ROOT}/{self.UNICODE_VERSION}/{UNICODE_TXT_FOLDER}/{PROP_VALUES_FILE_NAME}"
        self.prop_values_file = txt_folder.joinpath(PROP_VALUES_FILE_NAME)
        self.xml_folder = xml_folder
        self.xml_file = xml_folder.joinpath(XML_FILE_NAME)
        self.xml_zip_file = xml_folder.joinpath(XML_ZIP_FILE_NAME)
        self.xml_db_url = f"{UNICODE_ORG_ROOT}/{self.UNICODE_VERSION}/{UNICODE_XML_FOLDER}/{self.xml_zip_file.name}"
        self.db_folder = db_folder
        self.db_file = db_folder.joinpath(DB_FILE_NAME)
        self.db_zip_file = db_folder.joinpath(DB_ZIP_FILE_NAME)
        self.db_zip_url = f"{HTTP_BUCKET_URL}/{self.UNICODE_VERSION}/{DB_ZIP_FILE_NAME}"
        self.db_url = f"sqlite:///{db_folder.joinpath(DB_FILE_NAME).absolute()}"
        self.db_uri = f"file:///{db_folder.joinpath(DB_FILE_NAME).absolute()}"
        self.s3_bucket_url = S3_BUCKET_URL
        self.json_folder = json_folder
        self.prop_values_json = json_folder.joinpath("prop_values.json")
        self.planes_json = json_folder.joinpath("planes.json")
        self.blocks_json = json_folder.joinpath("blocks.json")
        self.char_name_map = json_folder.joinpath("char_name_map.json")
        self.unihan_chars_json = json_folder.joinpath("unihan_chars.json")
        self.tangut_chars_json = json_folder.joinpath("tangut_chars.json")
        self.json_zip_file = json_folder.joinpath(JSON_ZIP_FILE_NAME)
        self.json_zip_url = f"{HTTP_BUCKET_URL}/{self.UNICODE_VERSION}/{JSON_ZIP_FILE_NAME}"

    @property
    def is_dev(self):  # pragma: no cover
        return ENV_DEV in self.ENV

    @property
    def is_prod(self):  # pragma: no cover
        return ENV_PROD in self.ENV

    @property
    def is_test(self):  # pragma: no cover
        return ENV_TEST in self.ENV

    @property
    def rate_limit_settings_report(self) -> str:
        rate = f"{self.RATE_LIMIT_PER_PERIOD} request{s(self.RATE_LIMIT_PER_PERIOD)}"
        interval = f"{self.RATE_LIMIT_PERIOD_SECONDS.total_seconds()}"
        period = f"{'' if interval == '1.0' else f'{interval} '}second{s(interval)}"
        rate_limit_settings = f"Rate Limit Settings: {rate} per {period}"
        burst_enabled = self.RATE_LIMIT_BURST > 1
        if burst_enabled:  # pragma: no cover
            rate_limit_settings += f" (+{self.RATE_LIMIT_BURST} request burst allowance)"
        return rate_limit_settings

    @property
    def docker_ip_regex(self) -> re.Pattern[str]:
        return re.compile(rf"{self.DOCKER_IP_OCTET_1}\.{self.DOCKER_IP_OCTET_2}\.{self.DOCKER_IP_OCTET_3}\.\d{1, 3}")

    @property
    def non_unihan_character_name_map(self) -> dict[int, str]:
        if not self.char_name_map.exists():  # pragma: no cover
            return {}
        json_map = json.loads(self.char_name_map.read_text())
        return {int(codepoint): name for (codepoint, name) in json_map.items()}

    @property
    def unihan_character_name_map(self) -> dict[int, int]:
        if not self.unihan_chars_json.exists():  # pragma: no cover
            return {}
        json_map = json.loads(self.unihan_chars_json.read_text())
        return {int(codepoint): int(block_id) for (codepoint, block_id) in json_map.items()}

    @property
    def tangut_character_name_map(self) -> dict[int, int]:
        if not self.tangut_chars_json.exists():  # pragma: no cover
            return {}
        json_map = json.loads(self.tangut_chars_json.read_text())
        return {int(codepoint): int(block_id) for (codepoint, block_id) in json_map.items()}

    @property
    def property_value_id_map(self) -> "UnicodePropertyGroupMap":
        if not self.prop_values_json.exists():  # pragma: no cover
            return PROP_GROUP_VALUE_MAP_DEFAULT
        return json.loads(self.prop_values_json.read_text())

    @property
    def boolean_character_property_names(self) -> list[str]:
        if not self.prop_values_json.exists():  # pragma: no cover
            return []
        prop_values_map = json.loads(self.prop_values_json.read_text())
        return prop_values_map["boolean_properties"]

    @property
    def missing_property_group_names(self) -> list[str]:
        if not self.prop_values_json.exists():  # pragma: no cover
            return []
        prop_values_map = json.loads(self.prop_values_json.read_text())
        return prop_values_map["missing_prop_groups"]

    def init_data_folders(self) -> None:  # pragma: no cover
        self.txt_folder.mkdir(parents=True, exist_ok=True)
        self.db_folder.mkdir(parents=True, exist_ok=True)
        self.json_folder.mkdir(parents=True, exist_ok=True)

        if self.db_file.exists():
            self.db_file.unlink()

        if self.prop_values_json.exists():
            self.prop_values_json.unlink()

        if self.planes_json.exists():
            self.planes_json.unlink()
        self.planes_json.write_text(json.dumps(UNICODE_PLANES_DEFAULT, indent=4))

        if self.blocks_json.exists():
            self.blocks_json.unlink()

        if self.char_name_map.exists():
            self.char_name_map.unlink()

        if self.unihan_chars_json.exists():
            self.unihan_chars_json.unlink()

        if self.tangut_chars_json.exists():
            self.tangut_chars_json.unlink()


def load_api_settings() -> UnicodeApiSettings:  # pragma: no cover
    result = load_dotenv_file()
    if result.failure:
        raise ValueError(f"Failed to load .env file: {result.failure}")
    return UnicodeApiSettings(
        ENV=os.getenv("ENV", default=ENV_DEV),
        HOSTNAME=os.getenv("HOSTNAME", default="localhost"),
        API_VERSION="/v1",
        UNICODE_VERSION=os.getenv("UNICODE_VERSION", default=get_latest_unicode_version()),
        REDIS_PW=os.getenv("REDIS_PW", default=""),
        REDIS_HOST=os.getenv("REDIS_HOST", default=""),
        REDIS_PORT=int(os.getenv("REDIS_PORT", default="6379")),
        REDIS_DB=int(os.getenv("REDIS_DB", default="0")),
        RATE_LIMIT_PER_PERIOD=int(os.getenv("RATE_LIMIT_PER_PERIOD", default="1")),
        RATE_LIMIT_PERIOD_SECONDS=timedelta(seconds=int(os.getenv("RATE_LIMIT_PERIOD_SECONDS", default="100"))),
        RATE_LIMIT_BURST=int(os.getenv("RATE_LIMIT_BURST", default="10")),
        UMAMI_WEBSITE_ID=os.getenv("UMAMI_WEBSITE_ID", default=""),
        UMAMI_API_URL=os.getenv("UMAMI_API_URL", default=""),
        DOCKER_IP_OCTET_1=int(os.getenv("DOCKER_IP_OCTET_1", default="0")),
        DOCKER_IP_OCTET_2=int(os.getenv("DOCKER_IP_OCTET_2", default="0")),
        DOCKER_IP_OCTET_3=int(os.getenv("DOCKER_IP_OCTET_3", default="0")),
    )


def create_test_settings() -> UnicodeApiSettings:
    return UnicodeApiSettings(
        ENV=ENV_TEST,
        HOSTNAME="localhost",
        API_VERSION="/v1",
        UNICODE_VERSION="15.0.0",
        REDIS_PW="",
        REDIS_HOST="",
        REDIS_PORT=0,
        REDIS_DB=0,
        RATE_LIMIT_PER_PERIOD=2,
        RATE_LIMIT_PERIOD_SECONDS=timedelta(seconds=1),
        RATE_LIMIT_BURST=1,
        UMAMI_WEBSITE_ID="",
        UMAMI_API_URL="",
        DOCKER_IP_OCTET_1=0,
        DOCKER_IP_OCTET_2=0,
        DOCKER_IP_OCTET_3=0,
    )


def get_settings() -> UnicodeApiSettings:
    return create_test_settings() if ENV_TEST in os.environ.get("ENV", ENV_DEV) else load_api_settings()
