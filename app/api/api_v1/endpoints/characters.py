import operator
from functools import reduce
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from rapidfuzz import process
from sqlalchemy.engine import Engine
from sqlmodel import Session

import app.core.db as db
from app.api.api_v1.dependencies import (
    CharacterSearchParameters,
    get_char_property_groups_query_param,
    get_min_details_query_param,
    get_string_path_param,
    ListParameters,
    UnicodeBlockQueryParamResolver,
)
from app.api.api_v1.pagination import paginate_search_results
from app.core.config import settings
from app.core.enums.block_name import UnicodeBlockName
from app.core.util import get_codepoint_string
from app.data.cache import cached_data
from app.schemas.enums import CharPropertyGroup

router = APIRouter()


@router.get(
    "",
    response_model=db.PaginatedList[db.UnicodeCharacterResponse],
    response_model_exclude_unset=True,
)
def list_all_unicode_characters(
    list_params: ListParameters = Depends(),
    block: UnicodeBlockQueryParamResolver = Depends(),
    min_details: bool = Depends(get_min_details_query_param),
    db_ctx: tuple[Session, Engine] = Depends(db.get_session),
):
    _, engine = db_ctx
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
    show_props = [CharPropertyGroup.BASIC] if min_details else [CharPropertyGroup.ALL]
    return {
        "url": f"{settings.API_VERSION}/characters",
        "has_more": stop <= last_codepoint,
        "data": [
            get_character_details(engine, codepoint, show_props)
            for codepoint in range(start, stop)
            if codepoint in cached_data.all_codepoints
        ],
    }


@router.get(
    "/search",
    response_model=db.PaginatedSearchResults[db.UnicodeCharacterResult],
    response_model_exclude_unset=True,
)
def search_unicode_characters_by_name(
    search_params: CharacterSearchParameters = Depends(),
    db_ctx: tuple[Session, Engine] = Depends(db.get_session),
):
    _, engine = db_ctx
    params = {
        "url": f"{settings.API_VERSION}/characters/search",
        "query": search_params.name,
    }
    results = search_characters_by_name(engine, search_params.name, search_params.min_score)
    if results:
        paginate_result = paginate_search_results(results, search_params.per_page, search_params.page)
        if paginate_result.failure:
            raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=paginate_result.error)
        paginated = paginate_result.value
        if paginated:
            return params | paginated
    return params | {
        "current_page": 0,
        "total_results": 0,
        "has_more": False,
        "results": [],
    }


@router.get(
    "/{string}",
    response_model=list[db.UnicodeCharacterResponse],
    response_model_exclude_unset=True,
)
def get_unicode_character_details(
    string: str = Depends(get_string_path_param),
    show_props: list[CharPropertyGroup] = Depends(get_char_property_groups_query_param),
    db_ctx: tuple[Session, Engine] = Depends(db.get_session),
):
    _, engine = db_ctx
    prop_group_weights = CharPropertyGroup.get_group_weights()
    show_props_sorted = sorted(show_props, key=lambda x: prop_group_weights[x.name])
    return [get_character_details(engine, ord(char), show_props_sorted) for char in string]


def search_characters_by_name(engine: Engine, query: str, score_cutoff: int = 80) -> list[db.UnicodeCharacterResponse]:
    char_name_map = cached_data.char_name_map
    return [
        get_character_details(engine, result, [CharPropertyGroup.BASIC], float(score))
        for (_, score, result) in process.extract(query.lower(), char_name_map, limit=len(char_name_map))
        if score >= float(score_cutoff)
    ]


def get_character_details(
    engine: Engine,
    codepoint: int,
    show_props: list[CharPropertyGroup] | None = None,
    score: float | None = None,
) -> db.UnicodeCharacterResponse:
    if codepoint not in cached_data.all_codepoints:
        raise HTTPException(
            status_code=int(HTTPStatus.NOT_FOUND),
            detail=f"Failed to retrieve data for character matching codepoint {get_codepoint_string(codepoint)}.",
        )
    if not show_props:
        show_props = [CharPropertyGroup.BASIC]
    if CharPropertyGroup.BASIC not in show_props:
        show_props = [CharPropertyGroup.BASIC] + show_props
    if show_props and CharPropertyGroup.ALL in show_props:
        show_props = [group for group in CharPropertyGroup if group != CharPropertyGroup.ALL]
    no_name = codepoint in cached_data.char_no_name_map
    char_prop_dicts = [db.get_character_properties(engine, codepoint, group, no_name) for group in show_props]
    response_dict = reduce(operator.ior, char_prop_dicts, {})
    if score:
        response_dict["score"] = float(f"{score:.1f}")
    return db.UnicodeCharacterResponse(**response_dict)


def get_unicode_char_name(codepoint: int) -> str:
    block = get_unicode_block_containing_codepoint(codepoint)
    if block == UnicodeBlockName.NONE:
        return f"Invalid Codepoint ({get_codepoint_string(codepoint)})"
    if block in db.CJK_UNIFIED_BLOCKS:
        return f"CJK UNIFIED IDEOGRAPH-{codepoint:04X}"
    if block in db.CJK_COMPATIBILITY_BLOCKS:
        return f"CJK COMPATIBILITY IDEOGRAPH-{codepoint:04X}"
    if block in db.TANGUT_BLOCKS:
        return f"TANGUT IDEOGRAPH-{codepoint:04X}"
    if block in db.SINGLE_NO_NAME_BLOCKS:
        return f"{block} ({get_codepoint_string(codepoint)})"
    return cached_data.char_name_map.get(
        codepoint, f"Undefined Codepoint ({get_codepoint_string(codepoint)}) (Reserved for {block})"
    )


def get_unicode_block_containing_codepoint(codepoint: int) -> UnicodeBlockName:
    found = [
        block["id"]
        for block in cached_data.blocks
        if int(block["start_dec"]) <= codepoint and codepoint <= int(block["finish_dec"])
    ]
    return UnicodeBlockName.from_block_id(found[0]) if found else UnicodeBlockName.NONE
