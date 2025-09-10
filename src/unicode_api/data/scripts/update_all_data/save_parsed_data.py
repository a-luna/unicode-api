"""
This module provides functionality to save parsed Unicode data into JSON files.

Functions:
    save_parsed_data(settings: UnicodeApiSettings, parsed_data: AllParsedUnicodeData) -> Result[None]:
        Saves parsed Unicode data to JSON files based on the provided settings.
"""

import json

import unicode_api.db.models as db
from unicode_api.config.api_settings import UnicodeApiSettings
from unicode_api.core.result import Result
from unicode_api.data.scripts.script_types import AllParsedUnicodeData
from unicode_api.data.util.spinner import Spinner


def save_parsed_data(settings: UnicodeApiSettings, parsed_data: AllParsedUnicodeData) -> Result[None]:
    """
    Saves parsed Unicode data to JSON files based on the provided settings.

    Args:
        settings (UnicodeApiSettings): Configuration settings for saving the data.

        parsed_data (AllParsedUnicodeData): A tuple containing all parsed Unicode data, including planes, blocks,
            non-Unihan characters, Tangut characters, and Unihan characters.

    Returns:
        Result[None]: A Result object indicating success or failure of the save operation.
    """
    all_planes, all_blocks, non_unihan_chars, tangut_chars, unihan_chars = parsed_data
    _update_json_files(settings, all_planes, all_blocks, non_unihan_chars, tangut_chars, unihan_chars)
    return Result[None].Ok()


def _update_json_files(
    settings: UnicodeApiSettings,
    all_planes: list[db.UnicodePlane],
    all_blocks: list[db.UnicodeBlock],
    non_unihan_chars: list[db.UnicodeCharacter],
    tangut_chars: list[db.UnicodeCharacter],
    unihan_chars: list[db.UnicodeCharacterUnihan],
) -> None:
    spinner = Spinner()
    spinner.start("Creating JSON files for parsed Unicode data...")
    settings.planes_json.write_text(json.dumps([p.model_dump() for p in all_planes], indent=4))
    settings.blocks_json.write_text(json.dumps([b.model_dump() for b in all_blocks], indent=4))
    char_name_map = {char.codepoint_dec: char.name for char in non_unihan_chars}
    settings.char_name_map.write_text(json.dumps(char_name_map, indent=4))
    unihan_char_block_map = {char.codepoint_dec: char.block_id for char in unihan_chars}
    settings.unihan_chars_json.write_text(json.dumps(unihan_char_block_map, indent=4))
    tangut_char_block_map = {char.codepoint_dec: char.block_id for char in tangut_chars}
    settings.tangut_chars_json.write_text(json.dumps(tangut_char_block_map, indent=4))
    spinner.successful("Successfully created JSON files for parsed Unicode data")
