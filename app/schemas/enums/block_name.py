from enum import Enum

import app.db.models as db
from app.data.cache import cached_data
from app.schemas.util import normalize_string_lm3

UnicodeBlockName = Enum(
    "UnicodeBlockName", {b.name.replace(" ", "_").replace("-", "_").upper(): b for b in cached_data.blocks}
)


def display_name(self) -> str:  # pragma: no cover
    return self.name.replace("_", " ").title()


def _match_loosely(name, values) -> db.UnicodeBlock:
    block_name_map = {normalize_string_lm3(e.name): e.value for e in values}
    return block_name_map.get(normalize_string_lm3(name), None)


@classmethod
def match_loosely_block_name_get_block_id(cls, value: str) -> int:
    block = _match_loosely(value, list(cls))
    return block.id if block and block.id else 0


@classmethod
def match_loosely_block_name_get_block(cls, value: str) -> db.UnicodeBlock | None:
    return _match_loosely(value, list(cls))


UnicodeBlockName.match_loosely = match_loosely_block_name_get_block_id
UnicodeBlockName.match_loosely_get_block = match_loosely_block_name_get_block
