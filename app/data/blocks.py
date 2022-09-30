from http import HTTPStatus
import json
from typing import Dict, List, Union

from fastapi import HTTPException

from app.core.constants import DATA_FOLDER
from app.core.string_util import get_codepoint_string
from app.schemas.block import UnicodeBlockInternal


def get_unicode_blocks() -> List[UnicodeBlockInternal]:
    blocks_json_file = DATA_FOLDER.joinpath("blocks.json")
    blocks_json = json.loads(blocks_json_file.read_text())
    return [update_block_values(block_dict, i) for (i, block_dict) in enumerate(blocks_json, start=1)]


def update_block_values(block_dict: Dict[str, Union[int, str]], id: int) -> UnicodeBlockInternal:
    block_dict = {
        "id": id,
        "block": block_dict["block"],
        "start_dec": block_dict["start"],
        "start": get_codepoint_string(block_dict["start"]),
        "finish_dec": block_dict["finish"],
        "finish": get_codepoint_string(block_dict["finish"]),
        "total_assigned": block_dict["total_assigned"],
    }
    return UnicodeBlockInternal(**block_dict)


unicode_blocks = get_unicode_blocks()


def get_unicode_block_containing_character(uni_char: str) -> UnicodeBlockInternal:
    if len(uni_char) != 1:
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail="This operation is only valid for strings containing a single character",
        )
    codepoint = ord(uni_char)
    found = [block for block in unicode_blocks if block.start_dec <= codepoint and codepoint <= block.finish_dec]
    return found[0] if found else UnicodeBlockInternal(block="Invalid Codepoint", start=0, finish=0, total_assigned=0)
