import json
import os
from dataclasses import dataclass, field
from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING, TypedDict

from app.config.dotenv_file import read_dotenv_file
from app.constants import PROP_GROUP_VALUE_MAP_DEFAULT, UNICODE_PLANES_DEFAULT, UNICODE_VERSION_RELEASE_DATES
from app.core.util import s

if TYPE_CHECKING:  # pragma: no cover
    from app.custom_types import UnicodePropertyGroupMap


class ApiSettingsDict(TypedDict):
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
ROOT_FOLDER = APP_FOLDER.parent
DOTENV_FILE = ROOT_FOLDER.joinpath(".env")


def get_latest_unicode_version() -> str:  # pragma: no cover
    all_versions = {float(ver[:-2]): ver for ver in list(UNICODE_VERSION_RELEASE_DATES.keys())}
    sorted_versions = sorted(all_versions.keys(), reverse=True)
    return all_versions[sorted_versions[0]]


@dataclass
class UnicodeApiSettings:
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
    API_ROOT: str = field(init=False, default="")
    PROJECT_NAME: str = field(init=False, default="")
    ROOT_FOLDER: Path = field(init=False)
    APP_FOLDER: Path = field(init=False)
    DATA_FOLDER: Path = field(init=False)
    TESTS_FOLDER: Path = field(init=False)
    VERSION_FOLDER: Path = field(init=False)
    TXT_FOLDER: Path = field(init=False)
    PROP_VALUES_URL: str = field(init=False, default="")
    PROP_VALUES_FILE: Path = field(init=False)
    XML_FOLDER: Path = field(init=False)
    XML_FILE: Path = field(init=False)
    XML_ZIP_FILE: Path = field(init=False)
    XML_DB_URL: str = field(init=False, default="")
    DB_FOLDER: Path = field(init=False)
    DB_FILE: Path = field(init=False)
    DB_ZIP_FILE: Path = field(init=False)
    DB_ZIP_URL: str = field(init=False, default="")
    DB_URL: str = field(init=False, default="")
    DB_URI: str = field(init=False, default="")
    S3_BUCKET_URL: str = field(init=False, default="")
    JSON_FOLDER: Path = field(init=False)
    PROP_VALUES_JSON: Path = field(init=False)
    PROP_VALUE_ID_MAP: Path = field(init=False)
    PLANES_JSON: Path = field(init=False)
    BLOCKS_JSON: Path = field(init=False)
    CHAR_NAME_MAP: Path = field(init=False)
    UNIHAN_CHARS_JSON: Path = field(init=False)
    TANGUT_CHARS_JSON: Path = field(init=False)
    JSON_ZIP_FILE: Path = field(init=False)
    JSON_ZIP_URL: str = field(init=False, default="")

    def __post_init__(self) -> None:
        data_folder = APP_FOLDER.joinpath("data")
        version_folder = data_folder.joinpath("unicode_versions").joinpath(self.UNICODE_VERSION)
        txt_folder = version_folder.joinpath("txt")
        xml_folder = version_folder.joinpath("xml")
        db_folder = version_folder.joinpath("db")
        json_folder = version_folder.joinpath("json")
        http = "https" if "PROD" in self.ENV else "http"
        port = "" if "PROD" in self.ENV else ":3507"

        self.API_ROOT = f"{http}://{self.HOSTNAME}{port}"
        self.PROJECT_NAME = f"Unicode API{'' if 'PROD' in self.ENV else f' ({self.ENV})'}"
        self.ROOT_FOLDER = ROOT_FOLDER
        self.APP_FOLDER = ROOT_FOLDER.joinpath("app")
        self.DATA_FOLDER = data_folder
        self.TESTS_FOLDER = APP_FOLDER.joinpath("tests")
        self.VERSION_FOLDER = version_folder
        self.TXT_FOLDER = txt_folder
        self.PROP_VALUES_URL = f"{UNICODE_ORG_ROOT}/{self.UNICODE_VERSION}/{UNICODE_TXT_FOLDER}/{PROP_VALUES_FILE_NAME}"
        self.PROP_VALUES_FILE = txt_folder.joinpath(PROP_VALUES_FILE_NAME)
        self.XML_FOLDER = xml_folder
        self.XML_FILE = xml_folder.joinpath(XML_FILE_NAME)
        self.XML_ZIP_FILE = xml_folder.joinpath(XML_ZIP_FILE_NAME)
        self.XML_DB_URL = f"{UNICODE_ORG_ROOT}/{self.UNICODE_VERSION}/{UNICODE_XML_FOLDER}/{self.XML_ZIP_FILE.name}"
        self.DB_FOLDER = db_folder
        self.DB_FILE = db_folder.joinpath(DB_FILE_NAME)
        self.DB_ZIP_FILE = db_folder.joinpath(DB_ZIP_FILE_NAME)
        self.DB_ZIP_URL = f"{HTTP_BUCKET_URL}/{self.UNICODE_VERSION}/{DB_ZIP_FILE_NAME}"
        self.DB_URL = f"sqlite:///{db_folder.joinpath(DB_FILE_NAME).absolute()}"
        self.DB_URI = f"file:///{db_folder.joinpath(DB_FILE_NAME).absolute()}"
        self.S3_BUCKET_URL = S3_BUCKET_URL
        self.JSON_FOLDER = json_folder
        self.PROP_VALUES_JSON = json_folder.joinpath("prop_values.json")
        self.PLANES_JSON = json_folder.joinpath("planes.json")
        self.BLOCKS_JSON = json_folder.joinpath("blocks.json")
        self.CHAR_NAME_MAP = json_folder.joinpath("char_name_map.json")
        self.UNIHAN_CHARS_JSON = json_folder.joinpath("unihan_chars.json")
        self.TANGUT_CHARS_JSON = json_folder.joinpath("tangut_chars.json")
        self.JSON_ZIP_FILE = json_folder.joinpath(JSON_ZIP_FILE_NAME)
        self.JSON_ZIP_URL = f"{HTTP_BUCKET_URL}/{self.UNICODE_VERSION}/{JSON_ZIP_FILE_NAME}"

    @property
    def is_dev(self):  # pragma: no cover
        return "DEV" in self.ENV

    @property
    def is_prod(self):  # pragma: no cover
        return "PROD" in self.ENV

    @property
    def is_test(self):  # pragma: no cover
        return "TEST" in self.ENV

    @property
    def rate_limit_settings_report(self) -> str:
        rate = f"{self.RATE_LIMIT_PER_PERIOD} request{s(self.RATE_LIMIT_PER_PERIOD)}"
        interval = f"{self.RATE_LIMIT_PERIOD_SECONDS.total_seconds()}"
        period = f"{'' if interval == '1.0' else f'{interval} '}second{s(interval)}"
        rate_limit_settings = f"Rate Limit Settings: {rate} per {period}"
        burst_enabled = self.RATE_LIMIT_BURST > 1
        if burst_enabled:
            rate_limit_settings += f" (+{self.RATE_LIMIT_BURST} request burst allowance)"
        return rate_limit_settings

    def get_non_unihan_character_name_map(self) -> dict[int, str]:
        if not self.CHAR_NAME_MAP.exists():  # pragma: no cover
            return {}
        json_map = json.loads(self.CHAR_NAME_MAP.read_text())
        return {int(codepoint): name for (codepoint, name) in json_map.items()}

    def get_unihan_character_name_map(self) -> dict[int, int]:
        if not self.UNIHAN_CHARS_JSON.exists():  # pragma: no cover
            return {}
        json_map = json.loads(self.UNIHAN_CHARS_JSON.read_text())
        return {int(codepoint): int(block_id) for (codepoint, block_id) in json_map.items()}

    def get_tangut_character_name_map(self) -> dict[int, int]:
        if not self.TANGUT_CHARS_JSON.exists():  # pragma: no cover
            return {}
        json_map = json.loads(self.TANGUT_CHARS_JSON.read_text())
        return {int(codepoint): int(block_id) for (codepoint, block_id) in json_map.items()}

    def get_property_value_id_map(self) -> "UnicodePropertyGroupMap":
        if not self.PROP_VALUES_JSON.exists():
            return PROP_GROUP_VALUE_MAP_DEFAULT
        return json.loads(self.PROP_VALUES_JSON.read_text())

    def get_boolean_chraracter_property_names(self) -> list[str]:
        if not self.PROP_VALUES_JSON.exists():
            return []
        prop_values_map = json.loads(self.PROP_VALUES_JSON.read_text())
        return prop_values_map["boolean_properties"]

    def get_missing_property_group_names(self) -> list[str]:
        if not self.PROP_VALUES_JSON.exists():
            return []
        prop_values_map = json.loads(self.PROP_VALUES_JSON.read_text())
        return prop_values_map["missing_prop_groups"]

    def init_data_folders(self) -> None:  # pragma: no cover
        self.TXT_FOLDER.mkdir(parents=True, exist_ok=True)
        self.DB_FOLDER.mkdir(parents=True, exist_ok=True)
        self.JSON_FOLDER.mkdir(parents=True, exist_ok=True)

        if self.DB_FILE.exists():
            self.DB_FILE.unlink()

        if self.PROP_VALUES_JSON.exists():
            self.PROP_VALUES_JSON.unlink()

        if self.PLANES_JSON.exists():
            self.PLANES_JSON.unlink()
        self.PLANES_JSON.write_text(json.dumps(UNICODE_PLANES_DEFAULT, indent=4))

        if self.BLOCKS_JSON.exists():
            self.BLOCKS_JSON.unlink()

        if self.CHAR_NAME_MAP.exists():
            self.CHAR_NAME_MAP.unlink()

        if self.UNIHAN_CHARS_JSON.exists():
            self.UNIHAN_CHARS_JSON.unlink()

        if self.TANGUT_CHARS_JSON.exists():
            self.TANGUT_CHARS_JSON.unlink()


def get_api_settings() -> UnicodeApiSettings:  # pragma: no cover
    env_vars = read_dotenv_file(DOTENV_FILE)
    settings: ApiSettingsDict = {
        "ENV": env_vars.get("ENV", "DEV"),
        "HOSTNAME": env_vars.get("HOSTNAME", "localhost"),
        "API_VERSION": "/v1",
        "UNICODE_VERSION": env_vars.get("UNICODE_VERSION", get_latest_unicode_version()),
        "REDIS_PW": env_vars.get("REDIS_PW", ""),
        "REDIS_HOST": env_vars.get("REDIS_HOST", ""),
        "REDIS_PORT": int(env_vars.get("REDIS_PORT", "6379")),
        "REDIS_DB": int(env_vars.get("REDIS_DB", "0")),
        "RATE_LIMIT_PER_PERIOD": int(env_vars.get("RATE_LIMIT_PER_PERIOD", "1")),
        "RATE_LIMIT_PERIOD_SECONDS": timedelta(seconds=int(env_vars.get("RATE_LIMIT_PERIOD_SECONDS", "100"))),
        "RATE_LIMIT_BURST": int(env_vars.get("RATE_LIMIT_BURST", "10")),
        "UMAMI_WEBSITE_ID": env_vars.get("UMAMI_WEBSITE_ID", ""),
    }
    return UnicodeApiSettings(**settings)


def get_test_settings() -> UnicodeApiSettings:
    settings: ApiSettingsDict = {
        "ENV": "TEST",
        "HOSTNAME": "localhost",
        "API_VERSION": "/v1",
        "UNICODE_VERSION": "15.0.0",
        "REDIS_PW": "",
        "REDIS_HOST": "",
        "REDIS_PORT": 0,
        "REDIS_DB": 0,
        "RATE_LIMIT_PER_PERIOD": 2,
        "RATE_LIMIT_PERIOD_SECONDS": timedelta(seconds=1),
        "RATE_LIMIT_BURST": 1,
        "UMAMI_WEBSITE_ID": "",
    }
    return UnicodeApiSettings(**settings)


def get_settings() -> UnicodeApiSettings:
    return get_test_settings() if "TEST" in os.environ.get("ENV", "DEV") else get_api_settings()
