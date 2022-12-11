import os
from pathlib import Path

from pydantic import AnyHttpUrl, BaseSettings, RedisDsn

from app.data.scripts.init_prod_data import init_prod_data

# URLS
DEFAULT_REDIS_URL = "redis://127.0.0.1:6379"
S3_BUCKET_URL = "s3://unicode-api"

# FOLDER PATHS
ROOT_FOLDER = Path(__file__).parent.parent.parent
APP_FOLDER = ROOT_FOLDER.joinpath("app")
DATA_FOLDER = APP_FOLDER.joinpath("data")
JSON_FOLDER = DATA_FOLDER.joinpath("json")

# JSON DATA FILES
BLOCKS_JSON = JSON_FOLDER.joinpath("blocks.json")
CHARACTERS_JSON = JSON_FOLDER.joinpath("characters.json")
PLANES_JSON = JSON_FOLDER.joinpath("planes.json")

# FILE PATHS
DOTENV_FILE = ROOT_FOLDER.joinpath(".env")


class Settings(BaseSettings):
    if os.environ.get("ENV") == "PROD":
        init_prod_data()

    ENV: str = os.environ.get("ENV")
    PROJECT_NAME: str | None = "Unicode API"
    API_VERSION: str = "/v1"
    REDIS_URL: RedisDsn = (
        DEFAULT_REDIS_URL if os.environ.get("ENV") == "DEV" else os.environ.get("REDIS_URL", DEFAULT_REDIS_URL)
    )
    SERVER_NAME: str | None = "unicode-api.aaronluna.dev"
    SERVER_HOST: AnyHttpUrl | None = "https://unicode-api.aaronluna.dev"
    CACHE_HEADER: str = "X-UnicodeAPI-Cache"

    class Config:
        case_sensitive = True


settings = Settings()
