import json
from http import HTTPStatus

from fastapi import HTTPException

from app.core.constants import DATA_FOLDER
from app.core.util import get_code_point_string
from app.schemas.block import UnicodeBlockInternal

CJK_UNIFIED_BLOCKS = [
    "CJK Unified Ideographs",
    "CJK Unified Ideographs Extension A",
    "CJK Unified Ideographs Extension B",
    "CJK Unified Ideographs Extension C",
    "CJK Unified Ideographs Extension D",
    "CJK Unified Ideographs Extension E",
    "CJK Unified Ideographs Extension F",
    "CJK Unified Ideographs Extension G",
]
CJK_COMPATIBILITY_BLOCKS = ["CJK Compatibility Ideographs", "CJK Compatibility Ideographs Supplement"]
TANGUT_BLOCKS = ["Tangut", "Tangut Supplement"]
NULL_BLOCK = UnicodeBlockInternal(
    id=0, block="Undefined Codepoint", start_dec=0, start=0, finish_dec=0, finish=0, total_assigned=0
)


def get_unicode_blocks() -> list[UnicodeBlockInternal]:
    blocks_json_file = DATA_FOLDER.joinpath("json/blocks.json")
    blocks_json = json.loads(blocks_json_file.read_text())
    return [update_block_values(block_dict, i) for (i, block_dict) in enumerate(blocks_json, start=1)]


def update_block_values(block_dict: dict[str, int | str], id: int) -> UnicodeBlockInternal:
    block_dict = {
        "id": id,
        "block": block_dict["block"],
        "start_dec": block_dict["start"],
        "start": get_code_point_string(block_dict["start"]),
        "finish_dec": block_dict["finish"],
        "finish": get_code_point_string(block_dict["finish"]),
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
    code_point = ord(uni_char)
    found = [block for block in unicode_blocks if block.start_dec <= code_point and code_point <= block.finish_dec]
    return found[0] if found else NULL_BLOCK
