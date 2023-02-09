import os
from pathlib import Path

from pydantic import BaseSettings

# FOLDER PATHS
ROOT_FOLDER = Path(__file__).parent.parent.parent
APP_FOLDER = ROOT_FOLDER.joinpath("app")
DATA_FOLDER = APP_FOLDER.joinpath("data")
JSON_FOLDER = DATA_FOLDER.joinpath("json")
DB_FOLDER = DATA_FOLDER.joinpath("db")

# FILE PATHS
DOTENV_FILE = ROOT_FOLDER.joinpath(".env")
DB_FILE = DB_FOLDER.joinpath("unicode-api.db")
BLOCKS_JSON = JSON_FOLDER.joinpath("blocks.json")
CHARACTERS_JSON = JSON_FOLDER.joinpath("characters.json")
PLANES_JSON = JSON_FOLDER.joinpath("planes.json")
CHAR_NAME_MAP = JSON_FOLDER.joinpath("char_name_map.json")
CHAR_NO_NAME_MAP = JSON_FOLDER.joinpath("char_no_name_map.json")

# URLS
DEFAULT_REDIS_URL = "redis://127.0.0.1:6379"
S3_BUCKET_URL = "s3://unicode-api"
DB_URL = f"sqlite:///{DB_FILE}"


class Settings(BaseSettings):
    ENV: str = os.environ.get("ENV", "DEV")
    PROJECT_NAME: str = "Unicode API"
    API_VERSION: str = "/v1"
    REDIS_URL: str = (
        DEFAULT_REDIS_URL if os.environ.get("ENV") == "DEV" else os.environ.get("REDIS_URL", DEFAULT_REDIS_URL)
    )
    SERVER_NAME: str = "unicode-api.aaronluna.dev"
    SERVER_HOST: str = "https://unicode-api.aaronluna.dev"
    CACHE_HEADER: str = "X-UnicodeAPI-Cache"

    class Config:
        case_sensitive = True


settings = Settings()
