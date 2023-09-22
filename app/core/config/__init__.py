import os

from app.core.config.config import UnicodeApiSettings
from app.core.config.test_config import UnicodeApiSettingsTest


def get_settings():
    return UnicodeApiSettings() if os.environ["ENV"] != "TEST" else UnicodeApiSettingsTest()
