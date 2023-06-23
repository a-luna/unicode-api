from enum import Enum

import app.db.models as db
from app.data.cache import cached_data
from app.schemas.util import normalize_string_lm3

UnicodeBlockName = Enum(
    "UnicodeBlockName", {b.name.replace(" ", "_").replace("-", "_").upper(): b for b in cached_data.blocks}
)


@classmethod
def match_loosely_block_name_get_block_id(cls, name: str):
    block_name_map = {normalize_string_lm3(e.name): e.value for e in cls}
    block: db.UnicodeBlock = block_name_map.get(normalize_string_lm3(name), 0)
    return block.id


@classmethod
def match_loosely_block_name_get_block(cls, name: str):
    block_name_map = {normalize_string_lm3(e.name): e.value for e in cls}
    return block_name_map.get(normalize_string_lm3(name), 0)


UnicodeBlockName.match_loosely = match_loosely_block_name_get_block_id
UnicodeBlockName.match_loosely_get_block = match_loosely_block_name_get_block
