from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.engine import Engine
from sqlmodel import Session

import app.db.engine as db
from app.api.api_v1.dependencies import (
    CharacterSearchParameters,
    FilterParameters,
    get_description_and_values_table_for_property_group,
    ListParameters,
    parse_enum_values_from_parameter,
    UNICODE_CHAR_EXAMPLES,
    UNICODE_CHAR_STRING_DESCRIPTION,
    UnicodeBlockQueryParamResolver,
)
from app.api.api_v1.pagination import paginate_search_results
from app.core.config import settings
from app.data.cache import cached_data
from app.data.encoding import get_codepoint_string
from app.db.char_filters import filter_all_characters
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
    _, engine = db_ctx
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
    search_parameters: CharacterSearchParameters = Depends(),
    db_ctx: tuple[Session, Engine] = Depends(db.get_session),
):
    _, engine = db_ctx
    response_data = {"url": f"{settings.API_VERSION}/characters/search", "query": search_parameters.name}
    search_results = cached_data.search_characters_by_name(search_parameters.name, search_parameters.min_score)
    return get_paginated_character_list(
        engine,
        search_results,
        [CharPropertyGroup.Minimum],
        search_parameters.per_page,
        search_parameters.page,
        response_data,
    )


@router.get(
    "/filter",
    response_model=db.PaginatedSearchResults[db.UnicodeCharacterResponse],
    response_model_exclude_unset=True,
)
def filter_unicode_characters(
    filter_parameters: FilterParameters = Depends(),
    db_ctx: tuple[Session, Engine] = Depends(db.get_session),
):
    session, engine = db_ctx
    response_data = {"url": f"{settings.API_VERSION}/characters/filter"}
    codepoints = filter_all_characters(session, filter_parameters)
    filter_results = [(cp, None) for cp in codepoints]
    return get_paginated_character_list(
        engine,
        filter_results,
        filter_parameters.show_props,
        filter_parameters.per_page,
        filter_parameters.page,
        response_data,
    )


@router.get(
    "/{string}",
    response_model=list[db.UnicodeCharacterResponse],
    response_model_exclude_unset=True,
)
def get_unicode_character_details(
    string: str = Path(description=UNICODE_CHAR_STRING_DESCRIPTION, examples=UNICODE_CHAR_EXAMPLES),
    show_props: list[str]
    | None = Query(default=None, description=get_description_and_values_table_for_property_group()),
    db_ctx: tuple[Session, Engine] = Depends(db.get_session),
):
    _, engine = db_ctx
    prop_groups = parse_enum_values_from_parameter(CharPropertyGroup, "show_props", show_props) if show_props else None
    return [get_character_details(engine, ord(char), prop_groups) for char in string]


def get_char_list_endpoints(list_params: ListParameters, block: UnicodeBlockQueryParamResolver) -> tuple[int, int]:
    start = block.start
    if list_params.starting_after:
        start = list_params.starting_after + 1
    if list_params.ending_before:
        start = list_params.ending_before - list_params.limit
    stop = min(block.finish + 1, start + list_params.limit)
    if start < block.start or start > stop:
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail=(
                f"The starting codepoint value {get_codepoint_string(start)} is outside the range of characters "
                f"{get_codepoint_string(block.start)}...{get_codepoint_string(block.finish)} ({block.name})"
            ),
        )
    return (start, stop)


def get_paginated_character_list(
    engine: Engine,
    results: list[tuple[int, Any]],
    show_props: list[CharPropertyGroup] | None,
    per_page: int,
    page: int,
    response_data: dict[str, str],
):
    codepoints = [cp for (cp, _) in results]
    if codepoints:
        result = paginate_search_results(codepoints, per_page, page)
        if result.failure:
            raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=result.error)
        paginated = result.value if result.value else {}
        start = paginated.pop("start", 0)
        end = paginated.pop("end", 0)
        paginated["results"] = [
            get_character_details(engine, cp, show_props, score) for (cp, score) in results[start:end]
        ]
        return response_data | paginated
    return response_data | {
        "current_page": 0,
        "total_results": 0,
        "has_more": False,
        "results": [],
    }


def get_character_details(
    engine: Engine,
    codepoint: int,
    show_props: list[CharPropertyGroup] | None,
    score: float | None = None,
) -> db.UnicodeCharacterResponse:
    response_dict = get_character_properties(engine, codepoint, show_props)
    if score:
        response_dict["score"] = float(f"{score:.1f}")
    return db.UnicodeCharacterResponse(**response_dict)
