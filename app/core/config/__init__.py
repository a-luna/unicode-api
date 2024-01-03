import os

from app.core.config.config import UnicodeApiSettings, get_api_settings, get_test_settings


def get_settings() -> UnicodeApiSettings:
    return get_api_settings() if "TEST" not in os.environ.get("ENV", "DEV") else get_test_settings()
