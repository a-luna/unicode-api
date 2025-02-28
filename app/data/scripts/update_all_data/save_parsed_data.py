import json

import app.db.models as db
from app.config.api_settings import UnicodeApiSettings
from app.core.result import Result
from app.data.scripts.script_types import AllParsedUnicodeData
from app.data.util.spinners import Spinner


def save_parsed_data(settings: UnicodeApiSettings, parsed_data: AllParsedUnicodeData) -> Result[None]:
    all_planes, all_blocks, non_unihan_chars, tangut_chars, unihan_chars = parsed_data
    update_json_files(settings, all_planes, all_blocks, non_unihan_chars, tangut_chars, unihan_chars)
    return Result.Ok()


def update_json_files(
    settings: UnicodeApiSettings,
    all_planes: list[db.UnicodePlane],
    all_blocks: list[db.UnicodeBlock],
    non_unihan_chars: list[db.UnicodeCharacter],
    tangut_chars: list[db.UnicodeCharacter],
    unihan_chars: list[db.UnicodeCharacterUnihan],
) -> None:
    spinner = Spinner()
    spinner.start("Creating JSON files for parsed Unicode data...")
    settings.PLANES_JSON.write_text(json.dumps([p.model_dump() for p in all_planes], indent=4))
    settings.BLOCKS_JSON.write_text(json.dumps([b.model_dump() for b in all_blocks], indent=4))
    char_name_map = {char.codepoint_dec: char.name for char in non_unihan_chars}
    settings.CHAR_NAME_MAP.write_text(json.dumps(char_name_map, indent=4))
    unihan_char_block_map = {char.codepoint_dec: char.block_id for char in unihan_chars}
    settings.UNIHAN_CHARS_JSON.write_text(json.dumps(unihan_char_block_map, indent=4))
    tangut_char_block_map = {char.codepoint_dec: char.block_id for char in tangut_chars}
    settings.TANGUT_CHARS_JSON.write_text(json.dumps(tangut_char_block_map, indent=4))
    spinner.successful("Successfully created JSON files for parsed Unicode data")
