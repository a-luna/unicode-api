import logging
import os

from app.config.api_settings import UnicodeApiSettings, get_api_settings, get_test_settings


def get_settings() -> UnicodeApiSettings:
    env = os.environ.get("ENV", "DEV")
    settings = get_test_settings() if "TEST" in env else get_api_settings()
    logger = logging.getLogger("app.api")
    logger.debug(settings.api_settings_report)
    logger.debug(settings.rate_limit_settings_report)
    return settings
