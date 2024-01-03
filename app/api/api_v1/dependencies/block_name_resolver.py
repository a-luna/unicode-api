from typing import Annotated

from fastapi import HTTPException, Path, Query, status

import app.db.models as db
from app.data.cache import cached_data
from app.docs.dependencies.custom_parameters import BLOCK_NAME_DESCRIPTION, CHAR_SEARCH_BLOCK_NAME_DESCRIPTION
from app.schemas.enums.block_name import UnicodeBlockName


class UnicodeBlockQueryParamResolver:
    def __init__(
        self,
        block: Annotated[str | None, Query(description=CHAR_SEARCH_BLOCK_NAME_DESCRIPTION)] = None,
    ):
        self.block = loose_match_string_with_unicode_block_name(block) if block else cached_data.all_characters_block
        self.name = self.block.name
        self.start = self.block.start_dec
        self.finish = self.block.finish_dec


class UnicodeBlockPathParamResolver:
    def __init__(
        self,
        name: Annotated[str, Path(description=BLOCK_NAME_DESCRIPTION)],
    ):
        self.block = loose_match_string_with_unicode_block_name(name)
        self.name = self.block.name
        self.start = self.block.start_dec
        self.finish = self.block.finish_dec


def loose_match_string_with_unicode_block_name(name: str) -> db.UnicodeBlock:
    block = UnicodeBlockName.match_loosely_get_block(name)
    if block and block.name != "None":
        return block

    detail = f"{name!r} does not match any valid Unicode block name."
    fuzzy_matches = [
        cached_data.get_unicode_block_by_id(block_id).as_search_result(score)
        for (block_id, score) in cached_data.search_blocks_by_name(name, score_cutoff=72)
    ]
    if fuzzy_matches:
        detail += " The following block names are similar to the name you provided: "
        detail += f'{", ".join([str(b) for b in fuzzy_matches])}'
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
