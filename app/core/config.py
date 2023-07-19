import os
from datetime import timedelta
from pathlib import Path

from pydantic import BaseSettings

from app.core.dotenv_file import DotEnvFile

HTTP_BUCKET_URL = "https://unicode-api.us-southeast-1.linodeobjects.com"
S3_BUCKET_URL = "s3://unicode-api"
DEV_API_ROOT = "http://localhost:3507"
PROP_API_ROOT = "https://unicode-api.aaronluna.dev"

XML_FILE_NAME = "ucd.all.flat.xml"
XML_ZIP_FILE_NAME = "ucd.all.flat.zip"
DB_FILE_NAME = "unicode-api.db"
DB_ZIP_FILE_NAME = "unicode-api.db.zip"

APP_FOLDER = Path(__file__).parent.parent
ROOT_FOLDER = APP_FOLDER.parent
DOTENV_FILE = ROOT_FOLDER.joinpath(".env")

if os.environ.get("ENV", "") != "PROD":  # pragma: no cover
    dotenv = DotEnvFile(dotenv_filepath=DOTENV_FILE)


class UnicodeApiSettings(BaseSettings):
    ENV: str = os.environ.get("ENV", "DEV")
    UNICODE_VERSION: str = os.environ.get("UNICODE_VERSION", "")
    PROJECT_NAME: str = "Unicode API"
    API_VERSION: str = "/v1"
    REDIS_PW: str = os.environ.get("REDIS_PW", "")
    REDIS_HOST: str = os.environ.get("REDIS_HOST", "")
    REDIS_PORT: int = int(os.environ.get("REDIS_PORT", ""))
    REDIS_DB: int = int(os.environ.get("REDIS_DB", "0"))
    RATE_LIMIT_PER_PERIOD: int = int(os.environ.get("RATE_LIMIT_PER_PERIOD", "1"))
    RATE_LIMIT_PERIOD_SECONDS: timedelta = timedelta(seconds=int(os.environ.get("RATE_LIMIT_PERIOD_SECONDS", "100")))
    RATE_LIMIT_BURST: int = int(os.environ.get("RATE_LIMIT_BURST", "10"))
    SERVER_NAME: str = "unicode-api.aaronluna.dev"
    SERVER_HOST: str = "https://unicode-api.aaronluna.dev"
    CACHE_HEADER: str = "X-UnicodeAPI-Cache"
    API_ROOT = DEV_API_ROOT if os.environ.get("ENV") == "DEV" else PROP_API_ROOT

    ROOT_FOLDER: Path = ROOT_FOLDER
    APP_FOLDER: Path = ROOT_FOLDER.joinpath("app")
    DATA_FOLDER: Path = APP_FOLDER.joinpath("data")
    VERSION_FOLDER: Path = DATA_FOLDER.joinpath("unicode_versions").joinpath(UNICODE_VERSION)
    XML_FOLDER: Path = VERSION_FOLDER.joinpath("xml")
    XML_FILE: Path = XML_FOLDER.joinpath(XML_FILE_NAME)
    XML_ZIP_FILE: Path = XML_FOLDER.joinpath(XML_ZIP_FILE_NAME)
    DB_FOLDER: Path = VERSION_FOLDER.joinpath("db")
    DB_FILE: Path = DB_FOLDER.joinpath(DB_FILE_NAME)
    DB_ZIP_FILE: Path = DB_FOLDER.joinpath(DB_ZIP_FILE_NAME)
    DB_ZIP_URL: str = f"{HTTP_BUCKET_URL}/{UNICODE_VERSION}/{DB_ZIP_FILE.name}"
    DB_URL: str = f"sqlite:///{DB_FILE}"
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


settings = UnicodeApiSettings()
