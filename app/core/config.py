import os

from pydantic import AnyHttpUrl, BaseSettings, RedisDsn

from app.core.constants import DEFAULT_REDIS_URL


class Settings(BaseSettings):
    ENV: str = os.environ.get("ENV")
    PROJECT_NAME: str | None = "Unicode API"
    API_VERSION: str = "/api/v1"
    REDIS_URL: RedisDsn = (
        DEFAULT_REDIS_URL if os.environ.get("ENV") == "DEV" else os.environ.get("REDIS_URL", DEFAULT_REDIS_URL)
    )
    SERVER_NAME: str | None = "vig-api.aaronluna.dev"
    SERVER_HOST: AnyHttpUrl | None = "https://vig-api.aaronluna.dev"
    CACHE_HEADER: str = "X-Vigorish-Cache"

    class Config:
        case_sensitive = True


print(f"ENV={os.environ.get('ENV')}")
settings = Settings()
