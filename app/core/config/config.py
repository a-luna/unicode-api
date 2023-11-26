import json
import os
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Any

from app.core.dotenv_file import DotEnvFile
from app.data.constants import UNICODE_PLANES_DEFAULT

HTTP_BUCKET_URL = "https://unicode-api.us-southeast-1.linodeobjects.com"
S3_BUCKET_URL = "s3://unicode-api"
DEV_API_ROOT = "http://localhost:3507"
PROD_API_ROOT = "https://unicode-api.aaronluna.dev"

XML_FILE_NAME = "ucd.all.flat.xml"
XML_ZIP_FILE_NAME = "ucd.all.flat.zip"
DB_FILE_NAME = "unicode-api.db"
DB_ZIP_FILE_NAME = "unicode-api.db.zip"
JSON_ZIP_FILE_NAME = "unicode_json.zip"

APP_FOLDER = Path(__file__).parent.parent.parent
ROOT_FOLDER = APP_FOLDER.parent
DOTENV_FILE = ROOT_FOLDER.joinpath(".env")

if os.environ.get("ENV", "") != "PROD":  # pragma: no cover
    dotenv = DotEnvFile(dotenv_filepath=DOTENV_FILE)

LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "app.core.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": True,
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "app.api": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "app.api.error": {"level": "INFO"},
    },
}


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
    API_ROOT: str
    LOGGING_CONFIG: dict[str, Any]
    ROOT_FOLDER: Path
    APP_FOLDER: Path
    DATA_FOLDER: Path
    TESTS_FOLDER: Path
    VERSION_FOLDER: Path
    XML_FOLDER: Path
    XML_FILE: Path
    XML_ZIP_FILE: Path
    DB_FOLDER: Path
    DB_FILE: Path
    DB_ZIP_FILE: Path
    DB_ZIP_URL: str
    DB_URL: str
    S3_BUCKET_URL: str
    JSON_FOLDER: Path
    PLANES_JSON: Path
    BLOCKS_JSON: Path
    CHAR_NAME_MAP: Path
    JSON_ZIP_FILE: Path
    JSON_ZIP_URL: str
    CSV_FOLDER: Path
    PLANES_CSV: Path
    BLOCKS_CSV: Path
    NAMED_CHARS_CSV: Path
    UNIHAN_CHARS_CSV: Path

    def init_data_folders(self) -> None:
        self.DB_FOLDER.mkdir(parents=True, exist_ok=True)
        if self.DB_FILE.exists():
            self.DB_FILE.unlink()

        self.JSON_FOLDER.mkdir(parents=True, exist_ok=True)
        if self.PLANES_JSON.exists():
            self.PLANES_JSON.unlink()
        if self.BLOCKS_JSON.exists():
            self.BLOCKS_JSON.unlink()
        if self.CHAR_NAME_MAP.exists():
            self.CHAR_NAME_MAP.unlink()

        if "PROD" in self.ENV:
            return

        self.CSV_FOLDER.mkdir(parents=True, exist_ok=True)
        if self.BLOCKS_CSV.exists():
            self.BLOCKS_CSV.unlink()
        if self.NAMED_CHARS_CSV.exists():
            self.NAMED_CHARS_CSV.unlink()
        if self.UNIHAN_CHARS_CSV.exists():
            self.UNIHAN_CHARS_CSV.unlink()
        if self.PLANES_CSV.exists():
            self.PLANES_CSV.unlink()

        self.create_planes_json()

    def create_planes_json(self) -> None:
        self.PLANES_JSON.write_text(json.dumps(UNICODE_PLANES_DEFAULT, indent=4))


def get_api_settings() -> UnicodeApiSettings:
    env = os.environ.get("ENV", "DEV")
    unicode_version = os.environ.get("UNICODE_VERSION", "15.0.0")
    data_folder = APP_FOLDER.joinpath("data")
    version_folder = data_folder.joinpath("unicode_versions").joinpath(unicode_version)
    xml_folder = version_folder.joinpath("xml")
    db_folder = version_folder.joinpath("db")
    json_folder = version_folder.joinpath("json")
    csv_folder = version_folder.joinpath("csv")

    settings = UnicodeApiSettings(
        ENV=env,
        UNICODE_VERSION=unicode_version,
        PROJECT_NAME="Unicode API",
        API_VERSION="/v1",
        REDIS_PW=os.environ.get("REDIS_PW", ""),
        REDIS_HOST=os.environ.get("REDIS_HOST", ""),
        REDIS_PORT=int(os.environ.get("REDIS_PORT", "")),
        REDIS_DB=int(os.environ.get("REDIS_DB", "0")),
        RATE_LIMIT_PER_PERIOD=int(os.environ.get("RATE_LIMIT_PER_PERIOD", "1")),
        RATE_LIMIT_PERIOD_SECONDS=timedelta(seconds=int(os.environ.get("RATE_LIMIT_PERIOD_SECONDS", "100"))),
        RATE_LIMIT_BURST=int(os.environ.get("RATE_LIMIT_BURST", "10")),
        SERVER_NAME="unicode-api.aaronluna.dev",
        SERVER_HOST=PROD_API_ROOT,
        CACHE_HEADER="X-UnicodeAPI-Cache",
        API_ROOT=DEV_API_ROOT if "PROD" not in env else PROD_API_ROOT,
        LOGGING_CONFIG=LOGGING_CONFIG,
        ROOT_FOLDER=ROOT_FOLDER,
        APP_FOLDER=ROOT_FOLDER.joinpath("app"),
        DATA_FOLDER=data_folder,
        TESTS_FOLDER=APP_FOLDER.joinpath("tests"),
        VERSION_FOLDER=version_folder,
        XML_FOLDER=xml_folder,
        XML_FILE=xml_folder.joinpath(XML_FILE_NAME),
        XML_ZIP_FILE=xml_folder.joinpath(XML_ZIP_FILE_NAME),
        DB_FOLDER=db_folder,
        DB_FILE=db_folder.joinpath(DB_FILE_NAME),
        DB_ZIP_FILE=db_folder.joinpath(DB_ZIP_FILE_NAME),
        DB_ZIP_URL=f"{HTTP_BUCKET_URL}/{unicode_version}/{DB_ZIP_FILE_NAME}",
        DB_URL=f"sqlite:///{db_folder.joinpath(DB_FILE_NAME)}",
        S3_BUCKET_URL=S3_BUCKET_URL,
        JSON_FOLDER=json_folder,
        PLANES_JSON=json_folder.joinpath("planes.json"),
        BLOCKS_JSON=json_folder.joinpath("blocks.json"),
        CHAR_NAME_MAP=json_folder.joinpath("char_name_map.json"),
        JSON_ZIP_FILE=json_folder.joinpath(JSON_ZIP_FILE_NAME),
        JSON_ZIP_URL=f"{HTTP_BUCKET_URL}/{unicode_version}/{JSON_ZIP_FILE_NAME}",
        CSV_FOLDER=csv_folder,
        PLANES_CSV=csv_folder.joinpath("planes.csv"),
        BLOCKS_CSV=csv_folder.joinpath("blocks.csv"),
        NAMED_CHARS_CSV=csv_folder.joinpath("named_chars.csv"),
        UNIHAN_CHARS_CSV=csv_folder.joinpath("unihan_chars.csv"),
    )
    return settings


def get_test_settings() -> UnicodeApiSettings:
    env = "TEST"
    unicode_version = "15.0.0"
    data_folder = APP_FOLDER.joinpath("data")
    version_folder = data_folder.joinpath("unicode_versions").joinpath(unicode_version)
    xml_folder = version_folder.joinpath("xml")
    db_folder = version_folder.joinpath("db")
    json_folder = version_folder.joinpath("json")
    csv_folder = version_folder.joinpath("csv")

    settings = UnicodeApiSettings(
        ENV=env,
        UNICODE_VERSION=unicode_version,
        PROJECT_NAME="Test Unicode API",
        API_VERSION="/v1",
        REDIS_PW="",
        REDIS_HOST="",
        REDIS_PORT=0,
        REDIS_DB=0,
        RATE_LIMIT_PER_PERIOD=1,
        RATE_LIMIT_PERIOD_SECONDS=timedelta(seconds=100),
        RATE_LIMIT_BURST=10,
        SERVER_NAME="",
        SERVER_HOST="",
        CACHE_HEADER="",
        API_ROOT=DEV_API_ROOT,
        LOGGING_CONFIG=LOGGING_CONFIG,
        ROOT_FOLDER=ROOT_FOLDER,
        APP_FOLDER=ROOT_FOLDER.joinpath("app"),
        DATA_FOLDER=data_folder,
        TESTS_FOLDER=APP_FOLDER.joinpath("tests"),
        VERSION_FOLDER=version_folder,
        XML_FOLDER=xml_folder,
        XML_FILE=xml_folder.joinpath(XML_FILE_NAME),
        XML_ZIP_FILE=xml_folder.joinpath(XML_ZIP_FILE_NAME),
        DB_FOLDER=db_folder,
        DB_FILE=db_folder.joinpath(DB_FILE_NAME),
        DB_ZIP_FILE=db_folder.joinpath(DB_ZIP_FILE_NAME),
        DB_ZIP_URL=f"{HTTP_BUCKET_URL}/{unicode_version}/{DB_ZIP_FILE_NAME}",
        DB_URL=f"sqlite:///{db_folder.joinpath(DB_FILE_NAME)}",
        S3_BUCKET_URL=S3_BUCKET_URL,
        JSON_FOLDER=json_folder,
        PLANES_JSON=json_folder.joinpath("planes.json"),
        BLOCKS_JSON=json_folder.joinpath("blocks.json"),
        CHAR_NAME_MAP=json_folder.joinpath("char_name_map.json"),
        JSON_ZIP_FILE=json_folder.joinpath(JSON_ZIP_FILE_NAME),
        JSON_ZIP_URL=f"{HTTP_BUCKET_URL}/{unicode_version}/{JSON_ZIP_FILE_NAME}",
        CSV_FOLDER=csv_folder,
        PLANES_CSV=csv_folder.joinpath("planes.csv"),
        BLOCKS_CSV=csv_folder.joinpath("blocks.csv"),
        NAMED_CHARS_CSV=csv_folder.joinpath("named_chars.csv"),
        UNIHAN_CHARS_CSV=csv_folder.joinpath("unihan_chars.csv"),
    )
    return settings
