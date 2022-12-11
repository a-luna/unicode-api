from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from app.api.api_v1.dependencies import (
    ListParameters,
    CharacterSearchParameters,
    UnicodeBlockQueryParamResolver,
    get_min_details_query_param,
    get_string_path_param,
    get_unicode,
)
from app.core.config import settings
from app.core.util import get_codepoint_string, paginate_search_results
from app.data.unicode import Unicode
from app.schemas import (
    PaginatedList,
    PaginatedSearchResults,
    UnicodeCharacter,
    UnicodeCharacterResult,
)

router = APIRouter()


@router.get(
    "",
    response_model=PaginatedList[UnicodeCharacter | UnicodeCharacterResult],
    response_model_exclude_unset=True,
)
def list_all_unicode_characters(
    list_params: ListParameters = Depends(),
    block: UnicodeBlockQueryParamResolver = Depends(),
    min_details: bool = Depends(get_min_details_query_param),
    unicode: Unicode = Depends(get_unicode),
):
    first_codepoint = block.start_dec
    last_codepoint = block.finish_dec
    start = first_codepoint
    if list_params.starting_after:
        start = list_params.starting_after + 1
    elif list_params.ending_before:
        start = list_params.ending_before - list_params.limit
    stop = min(last_codepoint + 1, start + list_params.limit)
    if start < first_codepoint or start > last_codepoint:
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail=(
                f"The starting codepoint value {get_codepoint_string(start)} is outside the range of characters "
                f"{get_codepoint_string(first_codepoint)}...{get_codepoint_string(last_codepoint)} ({block.name})"
            ),
        )
    return {
        "url": f"{settings.API_VERSION}/characters",
        "has_more": stop <= last_codepoint,
        "data": [
            unicode.get_character_details(codepoint, min_details=min_details)
            for codepoint in range(start, stop)
            if codepoint in unicode.character_map
        ],
    }


@router.get(
    "/search",
    response_model=PaginatedSearchResults[UnicodeCharacterResult],
    response_model_exclude_unset=True,
)
def search_unicode_characters_by_name(
    search_params: CharacterSearchParameters = Depends(),
    unicode: Unicode = Depends(get_unicode),
):
    params = {
        "url": f"{settings.API_VERSION}/characters/search",
        "query": search_params.name,
    }
    results = unicode.search_characters_by_name(search_params.name, search_params.min_score)
    if not results:
        return params | {
            "current_page": 0,
            "total_results": 0,
            "has_more": False,
            "results": [],
        }
    paginate_result = paginate_search_results(results, search_params.per_page, search_params.page)
    if paginate_result.failure:
        raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=paginate_result.error)
    paginated = paginate_result.value
    return params | paginated


@router.get("/{string}", response_model=list[UnicodeCharacter], response_model_exclude_unset=True,)
def get_unicode_character_details(
    string: str = Depends(get_string_path_param),
    unicode: Unicode = Depends(get_unicode),
):
    return [unicode.get_character_details(ord(char), min_details=False) for char in string]


# @router.get("/{codepoint}", tags=["Unicode Characters"], response_model=UnicodeCharacter)
# def get_unicode_character_details_by_codepoint(
#     *, codepoint: str = Depends(get_char_from_hex_codepoint_path_param)
# ):
#     return get_character_details(codepoint)
