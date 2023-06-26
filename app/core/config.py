import os
from pathlib import Path

from pydantic import BaseSettings

from app.core.dotenv_file import DotEnvFile

HTTP_BUCKET_URL = "https://unicode-api.us-southeast-1.linodeobjects.com"
S3_BUCKET_URL = "s3://unicode-api"
DEFAULT_REDIS_URL = "redis://127.0.0.1:6379"
DEV_API_ROOT = "http://localhost:3507"
PROP_API_ROOT = "https://unicode-api.aaronluna.dev"

XML_FILE_NAME = "ucd.all.flat.xml"
XML_ZIP_FILE_NAME = "ucd.all.flat.zip"
DB_FILE_NAME = "unicode-api.db"
DB_ZIP_FILE_NAME = "unicode-api.db.zip"

ROOT_FOLDER = Path(__file__).parent.parent.parent
DOTENV_FILE = ROOT_FOLDER.joinpath(".env")
dotenv = DotEnvFile(dotenv_filepath=DOTENV_FILE)


class UnicodeApiSettings(BaseSettings):
    ENV: str = os.environ.get("ENV", "DEV")
    UNICODE_VERSION: str = os.environ.get("UNICODE_VERSION", "")
    PROJECT_NAME: str = "Unicode API"
    API_VERSION: str = "/v1"
    REDIS_URL: str = (
        DEFAULT_REDIS_URL if os.environ.get("ENV") == "DEV" else os.environ.get("REDIS_URL", DEFAULT_REDIS_URL)
    )
    SERVER_NAME: str = "unicode-api.aaronluna.dev"
    SERVER_HOST: str = "https://unicode-api.aaronluna.dev"
    CACHE_HEADER: str = "X-UnicodeAPI-Cache"
    API_ROOT = DEV_API_ROOT if os.environ.get("ENV") == "DEV" else PROP_API_ROOT

    ROOT_FOLDER: Path = ROOT_FOLDER
    APP_FOLDER: Path = ROOT_FOLDER.joinpath("app")
    DATA_FOLDER: Path = APP_FOLDER.joinpath("data")
    XML_FOLDER: Path = DATA_FOLDER.joinpath("xml").joinpath(UNICODE_VERSION)
    XML_FILE: Path = XML_FOLDER.joinpath(XML_FILE_NAME)
    XML_ZIP_FILE: Path = XML_FOLDER.joinpath(XML_ZIP_FILE_NAME)
    DB_FOLDER: Path = DATA_FOLDER.joinpath("db").joinpath(UNICODE_VERSION)
    DB_FILE: Path = DB_FOLDER.joinpath(DB_FILE_NAME)
    DB_ZIP_FILE: Path = DB_FOLDER.joinpath(DB_ZIP_FILE_NAME)
    DB_ZIP_URL: str = f"{HTTP_BUCKET_URL}/{UNICODE_VERSION}/{DB_ZIP_FILE.name}"
    DB_URL: str = f"sqlite:///{DB_FILE}"
    JSON_FOLDER: Path = DATA_FOLDER.joinpath("json").joinpath(UNICODE_VERSION)
    PLANES_JSON: Path = JSON_FOLDER.joinpath("planes.json")
    BLOCKS_JSON: Path = JSON_FOLDER.joinpath("blocks.json")
    CHAR_NAME_MAP: Path = JSON_FOLDER.joinpath("char_name_map.json")
    JSON_ZIP_FILE: Path = JSON_FOLDER.joinpath("unicode_json.zip")
    JSON_ZIP_URL: str = f"{HTTP_BUCKET_URL}/{JSON_ZIP_FILE.name}"
    CSV_FOLDER: Path = DATA_FOLDER.joinpath("csv").joinpath(UNICODE_VERSION)
    PLANES_CSV: Path = CSV_FOLDER.joinpath("planes.csv")
    BLOCKS_CSV: Path = CSV_FOLDER.joinpath("blocks.csv")
    NAMED_CHARS_CSV: Path = CSV_FOLDER.joinpath("named_chars.csv")
    UNIHAN_CHARS_CSV: Path = CSV_FOLDER.joinpath("unihan_chars.csv")

    class Config:
        case_sensitive = True


settings = UnicodeApiSettings()
