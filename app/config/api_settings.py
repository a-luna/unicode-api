import json
from dataclasses import dataclass, field
from datetime import timedelta
from pathlib import Path
from pprint import pprint

import app.db.models as db
from app.config.dotenv_file import read_dotenv_file
from app.data.constants import UNICODE_PLANES_DEFAULT, UNICODE_VERSION_RELEASE_DATES

UNICODE_ORG_ROOT = "https://www.unicode.org/Public"
UNICODE_XML_FOLDER = "ucdxml"
HTTP_BUCKET_URL = "https://unicode-api.us-southeast-1.linodeobjects.com"
S3_BUCKET_URL = "s3://unicode-api"
DEV_API_ROOT = "http://localhost:3507"
PROD_API_ROOT = "https://unicode-api.aaronluna.dev"

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
    UNICODE_VERSION: str
    PROJECT_NAME: str
    API_VERSION: str
    REDIS_PW: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    RATE_LIMIT_PER_PERIOD: int
    RATE_LIMIT_PERIOD_SECONDS: timedelta
    RATE_LIMIT_BURST: int
    SERVER_NAME: str
    SERVER_HOST: str
    CACHE_HEADER: str
    API_ROOT: str = field(init=False, default="")
    ROOT_FOLDER: Path = field(init=False)
    APP_FOLDER: Path = field(init=False)
    DATA_FOLDER: Path = field(init=False)
    TESTS_FOLDER: Path = field(init=False)
    VERSION_FOLDER: Path = field(init=False)
    XML_FOLDER: Path = field(init=False)
    XML_FILE: Path = field(init=False)
    XML_ZIP_FILE: Path = field(init=False)
    XML_DB_URL: str = field(init=False, default="")
    DB_FOLDER: Path = field(init=False)
    DB_FILE: Path = field(init=False)
    DB_ZIP_FILE: Path = field(init=False)
    DB_ZIP_URL: str = field(init=False, default="")
    DB_URL: str = field(init=False, default="")
    S3_BUCKET_URL: str = field(init=False, default="")
    JSON_FOLDER: Path = field(init=False)
    PLANES_JSON: Path = field(init=False)
    BLOCKS_JSON: Path = field(init=False)
    CHAR_NAME_MAP: Path = field(init=False)
    JSON_ZIP_FILE: Path = field(init=False)
    JSON_ZIP_URL: str = field(init=False, default="")
    CSV_FOLDER: Path = field(init=False)
    PLANES_CSV: Path = field(init=False)
    BLOCKS_CSV: Path = field(init=False)
    NAMED_CHARS_CSV: Path = field(init=False)
    UNIHAN_CHARS_CSV: Path = field(init=False)

    def __post_init__(self) -> None:
        data_folder = APP_FOLDER.joinpath("data")
        version_folder = data_folder.joinpath("unicode_versions").joinpath(self.UNICODE_VERSION)
        xml_folder = version_folder.joinpath("xml")
        db_folder = version_folder.joinpath("db")
        json_folder = version_folder.joinpath("json")
        csv_folder = version_folder.joinpath("csv")

        self.API_ROOT = DEV_API_ROOT if "PROD" not in self.ENV else PROD_API_ROOT
        self.ROOT_FOLDER = ROOT_FOLDER
        self.APP_FOLDER = ROOT_FOLDER.joinpath("app")
        self.DATA_FOLDER = data_folder
        self.TESTS_FOLDER = APP_FOLDER.joinpath("tests")
        self.VERSION_FOLDER = version_folder
        self.XML_FOLDER = xml_folder
        self.XML_FILE = xml_folder.joinpath(XML_FILE_NAME)
        self.XML_ZIP_FILE = xml_folder.joinpath(XML_ZIP_FILE_NAME)
        self.XML_DB_URL = f"{UNICODE_ORG_ROOT}/{self.UNICODE_VERSION}/{UNICODE_XML_FOLDER}/{self.XML_ZIP_FILE.name}"
        self.DB_FOLDER = db_folder
        self.DB_FILE = db_folder.joinpath(DB_FILE_NAME)
        self.DB_ZIP_FILE = db_folder.joinpath(DB_ZIP_FILE_NAME)
        self.DB_ZIP_URL = f"{HTTP_BUCKET_URL}/{self.UNICODE_VERSION}/{DB_ZIP_FILE_NAME}"
        self.DB_URL = f"sqlite:///{db_folder.joinpath(DB_FILE_NAME)}"
        self.S3_BUCKET_URL = S3_BUCKET_URL
        self.JSON_FOLDER = json_folder
        self.PLANES_JSON = json_folder.joinpath("planes.json")
        self.BLOCKS_JSON = json_folder.joinpath("blocks.json")
        self.CHAR_NAME_MAP = json_folder.joinpath("char_name_map.json")
        self.JSON_ZIP_FILE = json_folder.joinpath(JSON_ZIP_FILE_NAME)
        self.JSON_ZIP_URL = f"{HTTP_BUCKET_URL}/{self.UNICODE_VERSION}/{JSON_ZIP_FILE_NAME}"
        self.CSV_FOLDER = csv_folder
        self.PLANES_CSV = csv_folder.joinpath("planes.csv")
        self.BLOCKS_CSV = csv_folder.joinpath("blocks.csv")
        self.NAMED_CHARS_CSV = csv_folder.joinpath("named_chars.csv")
        self.UNIHAN_CHARS_CSV = csv_folder.joinpath("unihan_chars.csv")

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
    def api_settings_report(self) -> str:
        return f"API Settings: (ENV: {self.ENV}) (UNICODE_VERSION: {self.UNICODE_VERSION})"

    @property
    def rate_limit_settings_report(self) -> str:
        rate = f"{self.RATE_LIMIT_PER_PERIOD} request{'s' if self.RATE_LIMIT_PER_PERIOD > 1 else ''}"
        interval = self.RATE_LIMIT_PERIOD_SECONDS.total_seconds()
        period = f"{interval} seconds" if interval > 1 else "second"
        rate_limit_settings = f"Rate Limit Settings: {rate} per {period}"
        burst_enabled = self.RATE_LIMIT_BURST > 1
        if burst_enabled:  # pragma: no cover
            rate_limit_settings += f" (+{self.RATE_LIMIT_BURST} request burst allowance)"
        return rate_limit_settings

    def get_unicode_planes_data(self) -> list[db.UnicodePlane]:
        planes_dict = json.loads(self.PLANES_JSON.read_text()) if self.PLANES_JSON.exists() else UNICODE_PLANES_DEFAULT
        return [db.UnicodePlane(**plane) for plane in planes_dict]

    def get_unicode_blocks_data(self) -> list[db.UnicodeBlock]:
        blocks_dict = json.loads(self.BLOCKS_JSON.read_text()) if self.BLOCKS_JSON.exists() else []
        return [db.UnicodeBlock(**block) for block in blocks_dict]

    def get_non_unihan_character_name_map(self) -> dict[int, str]:
        if not self.CHAR_NAME_MAP.exists():
            return {}
        json_map = json.loads(self.CHAR_NAME_MAP.read_text())
        return {int(codepoint): name for (codepoint, name) in json_map.items()}

    def init_data_folders(self) -> None:  # pragma: no cover
        self.DB_FOLDER.mkdir(parents=True, exist_ok=True)
        if self.DB_FILE.exists():
            self.DB_FILE.unlink()

        self.JSON_FOLDER.mkdir(parents=True, exist_ok=True)
        if self.PLANES_JSON.exists():
            self.PLANES_JSON.unlink()
        self.PLANES_JSON.write_text(json.dumps(UNICODE_PLANES_DEFAULT, indent=4))
        if self.BLOCKS_JSON.exists():
            self.BLOCKS_JSON.unlink()
        if self.CHAR_NAME_MAP.exists():
            self.CHAR_NAME_MAP.unlink()

        if self.is_dev or self.is_test:
            self.CSV_FOLDER.mkdir(parents=True, exist_ok=True)
            if self.BLOCKS_CSV.exists():
                self.BLOCKS_CSV.unlink()
            if self.NAMED_CHARS_CSV.exists():
                self.NAMED_CHARS_CSV.unlink()
            if self.UNIHAN_CHARS_CSV.exists():
                self.UNIHAN_CHARS_CSV.unlink()
            if self.PLANES_CSV.exists():
                self.PLANES_CSV.unlink()


def get_api_settings() -> UnicodeApiSettings:  # pragma: no cover
    env_vars = read_dotenv_file(DOTENV_FILE)
    settings = {
        "ENV": env_vars.get("ENV", "DEV"),
        "UNICODE_VERSION": env_vars.get("UNICODE_VERSION", get_latest_unicode_version()),
        "PROJECT_NAME": "Unicode API",
        "API_VERSION": "/v1",
        "REDIS_PW": env_vars.get("REDIS_PW", ""),
        "REDIS_HOST": env_vars.get("REDIS_HOST", ""),
        "REDIS_PORT": int(env_vars.get("REDIS_PORT", "6379")),
        "REDIS_DB": int(env_vars.get("REDIS_DB", "0")),
        "RATE_LIMIT_PER_PERIOD": int(env_vars.get("RATE_LIMIT_PER_PERIOD", "1")),
        "RATE_LIMIT_PERIOD_SECONDS": timedelta(seconds=int(env_vars.get("RATE_LIMIT_PERIOD_SECONDS", "100"))),
        "RATE_LIMIT_BURST": int(env_vars.get("RATE_LIMIT_BURST", "10")),
        "SERVER_NAME": "unicode-api.aaronluna.dev",
        "SERVER_HOST": PROD_API_ROOT,
        "CACHE_HEADER": "X-UnicodeAPI-Cache",
    }
    print(f"\n\n{'#' * 10} SETTINGS DICT (get_api_settings) {'#' * 10}\n\n")
    pprint(settings)
    return UnicodeApiSettings(**settings)


def get_test_settings() -> UnicodeApiSettings:
    settings = {
        "ENV": "TEST",
        "UNICODE_VERSION": "15.0.0",
        "PROJECT_NAME": "Test Unicode API",
        "API_VERSION": "/v1",
        "REDIS_PW": "",
        "REDIS_HOST": "",
        "REDIS_PORT": 0,
        "REDIS_DB": 0,
        "RATE_LIMIT_PER_PERIOD": 2,
        "RATE_LIMIT_PERIOD_SECONDS": timedelta(seconds=1),
        "RATE_LIMIT_BURST": 1,
        "SERVER_NAME": "",
        "SERVER_HOST": "",
        "CACHE_HEADER": "",
    }
    return UnicodeApiSettings(**settings)
