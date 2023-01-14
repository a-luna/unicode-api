import operator
from functools import reduce
from http import HTTPStatus
from typing import Type

from fastapi import APIRouter, Depends, HTTPException, Query
from rapidfuzz import process
from sqlalchemy.engine import Engine
from sqlmodel import Session

import app.db.engine as db
from app.api.api_v1.dependencies import (
    CharacterSearchParameters,
    get_string_path_param,
    ListParameters,
    UnicodeBlockQueryParamResolver,
)
from app.api.api_v1.pagination import paginate_search_results
from app.core.config import settings
from app.data.cache import cached_data
from app.data.encoding import get_codepoint_string
from app.db.get_char_details import get_character_properties
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
    db_ctx: tuple[Session, Engine] = Depends(db.get_session),
):
    session, engine = db_ctx
    (start, stop) = get_char_list_endpoints(list_params, block)
    return {
        "url": f"{settings.API_VERSION}/characters",
        "has_more": stop <= block.finish,
        "data": [
            get_character_details(engine, codepoint, [CharPropertyGroup.Minimum]) for codepoint in range(start, stop)
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
    session, engine = db_ctx
    params = {
        "url": f"{settings.API_VERSION}/characters/search",
        "query": search_params.name,
    }
    results = [char for char in search_characters_by_name(session, engine, search_params.name, search_params.min_score)]
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
    show_props: list[CharPropertyGroup] | None = Query(default=None),
    db_ctx: tuple[Session, Engine] = Depends(db.get_session),
):
    _, engine = db_ctx
    return [get_character_details(engine, ord(char), show_props) for char in string]


def get_char_list_endpoints(list_params: ListParameters, block: UnicodeBlockQueryParamResolver) -> tuple[int, int]:
    start = block.start
    if list_params.starting_after:
        start = list_params.starting_after + 1
    elif list_params.ending_before:
        start = list_params.ending_before - list_params.limit
    stop = min(block.finish + 1, start + list_params.limit)
    if start < block.start or start > block.finish:
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail=(
                f"The starting codepoint value {get_codepoint_string(start)} is outside the range of characters "
                f"{get_codepoint_string(block.start)}...{get_codepoint_string(block.finish)} ({block.name})"
            ),
        )
    return (start, stop)


def search_characters_by_name(
    session: Session, engine: Engine, query: str, score_cutoff: int = 80
) -> list[db.UnicodeCharacterResponse]:
    fuzzy_search_results = process.extract(
        query.lower(),
        cached_data.char_unique_name_search_choices,
        limit=cached_data.total_char_unique_name_search_choices,
    )
    return [
        get_character_details(engine, result, [CharPropertyGroup.Minimum], float(score))
        for (_, score, result) in fuzzy_search_results
        if score >= float(score_cutoff)
    ]


def get_character_details(
    engine: Engine,
    codepoint: int,
    show_props: list[CharPropertyGroup] | None = None,
    score: float | None = None,
) -> db.UnicodeCharacterResponse:
    if not cached_data.codepoint_is_in_unicode_range(codepoint):
        raise HTTPException(
            status_code=int(HTTPStatus.NOT_FOUND),
            detail=f"Failed to retrieve data for character matching codepoint {get_codepoint_string(codepoint)}.",
        )
    show_props = check_prop_group_selections(show_props)
    char_name = cached_data.get_character_name(codepoint)
    char_table_name = get_character_table_name_for_codepoint(codepoint)
    char_prop_dicts = [
        get_character_properties(engine, codepoint, group, char_name, char_table_name) for group in show_props
    ]
    response_dict = reduce(operator.ior, char_prop_dicts, {})
    if score:
        response_dict["score"] = float(f"{score:.1f}")
    return db.UnicodeCharacterResponse(**response_dict)


def check_prop_group_selections(prop_groups: list[CharPropertyGroup] | None = None) -> list[CharPropertyGroup]:
    if not prop_groups:
        prop_groups = [CharPropertyGroup.Minimum]
    if CharPropertyGroup.Minimum not in prop_groups:
        prop_groups = [CharPropertyGroup.Minimum] + prop_groups
    if prop_groups and CharPropertyGroup.All in prop_groups:
        prop_groups = [group for group in CharPropertyGroup if group != CharPropertyGroup.All]
    return prop_groups


def get_character_table_name_for_codepoint(
    codepoint: int,
) -> (Type[db.UnicodeCharacterNoName] | Type[db.UnicodeCharacter]):
    return db.UnicodeCharacter if cached_data.character_is_uniquely_named(codepoint) else db.UnicodeCharacterNoName
