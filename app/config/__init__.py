import logging
import os
from dataclasses import asdict
from pprint import pprint

from app.config.api_settings import UnicodeApiSettings, get_api_settings, get_test_settings


def get_settings() -> UnicodeApiSettings:
    env = os.environ.get("ENV", "DEV")
    settings = get_test_settings() if "TEST" in env else get_api_settings()

    print(f"{'#' * 10} API SETTINGS (get_settings) {'#' * 10}\n\n")
    pprint(asdict(settings))
    print(f"\n\n{'#' * 34}\n\n")

    logger = logging.getLogger("app.api")
    logger.debug(settings.api_settings_report)
    logger.debug(settings.rate_limit_settings_report)
    return settings
