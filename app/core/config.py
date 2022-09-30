import os
from typing import Optional

from pydantic import AnyHttpUrl, BaseSettings, RedisDsn


class Settings(BaseSettings):
    ENV: str = os.environ.get("ENV")
    PROJECT_NAME: Optional[str] = "Unicode API"
    API_VERSION: str = "/api/v1"
    REDIS_URL: RedisDsn = "redis://127.0.0.1:6379"
    SERVER_NAME: Optional[str] = "vig-api.aaronluna.dev"
    SERVER_HOST: Optional[AnyHttpUrl] = "https://vig-api.aaronluna.dev"
    CACHE_HEADER: str = "X-Vigorish-Cache"

    class Config:
        case_sensitive = True


settings = Settings()
