"""
This module imports and exposes utility functions for updating all data in the Unicode API application.
It includes functions for backing up databases and JSON files, retrieving API settings, obtaining property values,
downloading and parsing the XML Unicode database, populating the SQLite database, and saving parsed data.

Imported functions:
- backup_db_and_json_files: Handles backup of the database and JSON files.
- get_api_settings: Retrieves API configuration settings.
- get_prop_values: Obtains Unicode property values.
- download_xml_unicode_database: Downloads the XML Unicode database.
- parse_xml_unicode_database: Parses the downloaded XML Unicode database.
- populate_sqlite_database: Populates the SQLite database with parsed data.
- save_parsed_data: Saves the parsed data to appropriate files.
"""

from unicode_api.data.scripts.update_all_data.backup_db_and_json_files import backup_db_and_json_files
from unicode_api.data.scripts.update_all_data.get_api_settings import get_api_settings
from unicode_api.data.scripts.update_all_data.get_prop_values import get_prop_values
from unicode_api.data.scripts.update_all_data.get_xml_unicode_db import download_xml_unicode_database
from unicode_api.data.scripts.update_all_data.parse_xml_unicode_db import parse_xml_unicode_database
from unicode_api.data.scripts.update_all_data.populate_sqlite_db import populate_sqlite_database
from unicode_api.data.scripts.update_all_data.save_parsed_data import save_parsed_data

__all__ = [
    "backup_db_and_json_files",
    "get_api_settings",
    "get_prop_values",
    "download_xml_unicode_database",
    "parse_xml_unicode_database",
    "populate_sqlite_database",
    "save_parsed_data",
]
