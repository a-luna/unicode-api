from collections import defaultdict
from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from app.core.constants import HEX_REGEX
from app.data.blocks import get_unicode_block_containing_character
from app.data.characters import fuzzy_character_search, get_character_details
from app.schemas import CharToBlockMap, FuzzySearchResult, UnicodeCharacter

router = APIRouter()


@router.get("/search/", response_model=List[FuzzySearchResult])
def search_character_name(q: str):
    results = fuzzy_character_search(q)
    for char_match in results:
        char_match["details"] = get_character_details(chr(char_match["result"]))
    return results


@router.get("/blocks/", response_model=List[CharToBlockMap])
def get_unicode_block(
    codepoint_int: Optional[int] = Query(default=None, ge=0, le=917631),
    codepoint_hex: Optional[str] = None,
    char: Optional[str] = None,
):
    if codepoint_int:
        char_list = [chr(codepoint_int)]
    if codepoint_hex:
        if not HEX_REGEX.match(codepoint_hex):
            raise HTTPException(
                status_code=int(HTTPStatus.BAD_REQUEST), detail=f"{codepoint_hex} is not a valid hex value"
            )
        char_list = [chr(int(codepoint_hex, 16))]
    if char:
        char_list = char

    block_map = {}
    char_map = defaultdict(list)
    for c in char_list:
        block = get_unicode_block_containing_character(c)
        block_map[block.id] = block
        char_map[block.id].append(c)

    results = [
        {
            "total_chars": len(list(set(chars_in_block))),
            "characters_in_block": [get_character_details(c) for c in list(set(chars_in_block))],
            "block": block_map[block_id],
        }
        for (block_id, chars_in_block) in char_map.items()
    ]

    return sorted(results, key=lambda x: -x["total_chars"])


@router.get("/characters/", response_model=List[UnicodeCharacter])
def get_unicode_character_info(char: str):
    return [get_character_details(c) for c in char]
