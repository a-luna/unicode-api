from datetime import timedelta
from pathlib import Path
from typing import Any

from pydantic import BaseSettings

HTTP_BUCKET_URL = "https://unicode-api.us-southeast-1.linodeobjects.com"
S3_BUCKET_URL = "s3://unicode-api"
DEV_API_ROOT = "http://localhost:3507"

XML_FILE_NAME = "ucd.all.flat.xml"
XML_ZIP_FILE_NAME = "ucd.all.flat.zip"
DB_FILE_NAME = "unicode-api.db"
DB_ZIP_FILE_NAME = "unicode-api.db.zip"

APP_FOLDER = Path(__file__).parent.parent.parent
ROOT_FOLDER = APP_FOLDER.parent

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


class UnicodeApiSettingsTest(BaseSettings):
    ENV: str = "TEST"
    UNICODE_VERSION: str = "15.0.0"
    PROJECT_NAME: str = "Test Unicode API"
    API_VERSION: str = "/v1"
    REDIS_PW: str = ""
    REDIS_HOST: str = ""
    REDIS_PORT: int = 0
    REDIS_DB: int = 0
    RATE_LIMIT_PER_PERIOD: int = 0
    RATE_LIMIT_PERIOD_SECONDS: timedelta = timedelta()
    RATE_LIMIT_BURST: int = 0
    SERVER_NAME: str = ""
    SERVER_HOST: str = ""
    CACHE_HEADER: str = ""
    API_ROOT = DEV_API_ROOT = DEV_API_ROOT
    LOGGING_CONFIG: dict[str, Any] = LOGGING_CONFIG

    ROOT_FOLDER: Path = ROOT_FOLDER
    APP_FOLDER: Path = ROOT_FOLDER.joinpath("app")
    DATA_FOLDER: Path = APP_FOLDER.joinpath("data")
    TESTS_FOLDER: Path = APP_FOLDER.joinpath("tests")
    VERSION_FOLDER: Path = DATA_FOLDER.joinpath("unicode_versions").joinpath(UNICODE_VERSION)
    XML_FOLDER: Path = VERSION_FOLDER.joinpath("xml")
    XML_FILE: Path = XML_FOLDER.joinpath(XML_FILE_NAME)
    XML_ZIP_FILE: Path = XML_FOLDER.joinpath(XML_ZIP_FILE_NAME)
    DB_FOLDER: Path = VERSION_FOLDER.joinpath("db")
    DB_FILE: Path = DB_FOLDER.joinpath(DB_FILE_NAME)
    DB_ZIP_FILE: Path = DB_FOLDER.joinpath(DB_ZIP_FILE_NAME)
    DB_ZIP_URL: str = f"{HTTP_BUCKET_URL}/{UNICODE_VERSION}/{DB_ZIP_FILE.name}"
    DB_URL: str = f"sqlite:///{DB_FILE}"
    S3_BUCKET_URL: str = S3_BUCKET_URL
    JSON_FOLDER: Path = VERSION_FOLDER.joinpath("json")
    PLANES_JSON: Path = JSON_FOLDER.joinpath("planes.json")
    BLOCKS_JSON: Path = JSON_FOLDER.joinpath("blocks.json")
    CHAR_NAME_MAP: Path = JSON_FOLDER.joinpath("char_name_map.json")
    JSON_ZIP_FILE: Path = JSON_FOLDER.joinpath("unicode_json.zip")
    JSON_ZIP_URL: str = f"{HTTP_BUCKET_URL}/{UNICODE_VERSION}/{JSON_ZIP_FILE.name}"
    CSV_FOLDER: Path = VERSION_FOLDER.joinpath("csv")
    PLANES_CSV: Path = CSV_FOLDER.joinpath("planes.csv")
    BLOCKS_CSV: Path = CSV_FOLDER.joinpath("blocks.csv")
    NAMED_CHARS_CSV: Path = CSV_FOLDER.joinpath("named_chars.csv")
    UNIHAN_CHARS_CSV: Path = CSV_FOLDER.joinpath("unihan_chars.csv")

    class Config:
        case_sensitive = True
