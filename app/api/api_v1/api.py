from collections import defaultdict

from fastapi import APIRouter, Depends, Query

from app.api.api_v1.dependencies import get_char_from_hex_code_point_path_param, get_query_params, get_single_char
from app.data.blocks import get_unicode_block_containing_character
from app.data.characters import fuzzy_character_search, get_character_details
from app.schemas import CharToBlockMap, UnicodeCharacter
from app.schemas.search import SearchResults

router = APIRouter()


@router.get("/search", response_model=SearchResults)
def search_unicode_characters_by_name(
    name: str = Query(  # noqa: B008
        description=(
            "Search for any unicode character by name. Exact matches are unnecessary since the search algorithm "
            "will return character names similar to the search term."
        )
    ),
    minimum_score: int
    | None = Query(  # noqa: B008
        default=80,
        ge=0,
        le=100,
        description=(
            "A score between 0 and 100 (with 100 being a perfect match) is calculated for each search result. "
            "Raising this setting will result in fewer, higher-quality search results, while lowering it "
            "will ensure more, lower-quality results are returned."
        ),
    ),
):
    results = fuzzy_character_search(name, minimum_score)
    return SearchResults(query=name, total_results=len(results), results=results)


@router.get("/char/{char}", response_model=list[UnicodeCharacter])
def get_unicode_character_details(char: str = Depends(get_single_char)):  # noqa: B008
    return [get_character_details(c) for c in char]


@router.get("/code_point/{code_point}", response_model=UnicodeCharacter)
def get_unicode_character_details_by_code_point(
    *, code_point: str = Depends(get_char_from_hex_code_point_path_param)  # noqa: B008
):
    return get_character_details(code_point)


@router.get("/blocks", response_model=list[CharToBlockMap])
def get_unicode_block(char_list: str = Depends(get_query_params)):  # noqa: B008
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
    return sorted(results, key=lambda x: (-x["total_chars"], x["block"].start_dec))
