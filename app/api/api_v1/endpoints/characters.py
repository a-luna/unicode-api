from http import HTTPStatus
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Path, Query

import app.db.models as db
from app.api.api_v1.dependencies import (
    CharacterSearchParameters,
    DBSession,
    FilterParameters,
    ListParameters,
    UnicodeBlockQueryParamResolver,
    get_session,
)
from app.api.api_v1.dependencies.filter_params import FilterParameterMatcher
from app.api.api_v1.pagination import paginate_search_results
from app.core.config import settings
from app.data.cache import cached_data
from app.data.encoding import get_codepoint_string
from app.docs.dependencies.custom_parameters import (
    UNICODE_CHAR_EXAMPLES,
    UNICODE_CHAR_STRING_DESCRIPTION,
    get_description_and_values_table_for_property_group,
)
from app.schemas.enums import CharPropertyGroup

PropertyGroupMatcher = FilterParameterMatcher[CharPropertyGroup]("show_props", CharPropertyGroup)
DatabaseSession = Annotated[DBSession, Depends(get_session)]
router = APIRouter()


@router.get(
    "",
    response_model=db.PaginatedList[db.UnicodeCharacterResponse],
    response_model_exclude_unset=True,
)
def list_all_unicode_characters(
    db_ctx: DatabaseSession,
    list_params: ListParameters = Depends(),
    block: UnicodeBlockQueryParamResolver = Depends(),
):
    (start, stop) = get_char_list_endpoints(list_params, block)
    return {
        "url": f"{settings.API_VERSION}/characters",
        "has_more": stop <= block.finish,
        "data": [
            get_character_details(db_ctx, codepoint, [CharPropertyGroup.MINIMUM]) for codepoint in range(start, stop)
        ],
    }


@router.get(
    "/search",
    response_model=db.PaginatedSearchResults[db.UnicodeCharacterResult],
    response_model_exclude_unset=True,
)
def search_unicode_characters_by_name(
    db_ctx: DatabaseSession,
    search_parameters: CharacterSearchParameters = Depends(),
):
    response_data = {"url": f"{settings.API_VERSION}/characters/search", "query": search_parameters.name}
    search_results = cached_data.search_characters_by_name(search_parameters.name, search_parameters.min_score)
    return get_paginated_character_list(
        db_ctx,
        search_results,
        [CharPropertyGroup.MINIMUM],
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
    db_ctx: DatabaseSession,
    filter_parameters: FilterParameters = Depends(),
):
    response_data = {"url": f"{settings.API_VERSION}/characters/filter"}
    codepoints = db_ctx.filter_all_characters(filter_parameters)
    filter_results = [(cp, None) for cp in codepoints]
    return get_paginated_character_list(
        db_ctx,
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
    db_ctx: DatabaseSession,
    string: str = Path(description=UNICODE_CHAR_STRING_DESCRIPTION, examples=UNICODE_CHAR_EXAMPLES),
    show_props: list[str]
    | None = Query(default=None, description=get_description_and_values_table_for_property_group()),
):
    if show_props:
        result = PropertyGroupMatcher.parse_enum_values(show_props)
        if result.failure:
            raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=result.error)
        prop_groups = result.value
    else:
        prop_groups = None
    return [get_character_details(db_ctx, ord(char), prop_groups) for char in string]


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
    db_ctx: DBSession,
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
            get_character_details(db_ctx, cp, show_props, score) for (cp, score) in results[start:end]
        ]
        return response_data | paginated
    return response_data | {
        "current_page": 0,
        "total_results": 0,
        "has_more": False,
        "results": [],
    }


def get_character_details(
    db_ctx: DBSession,
    codepoint: int,
    show_props: list[CharPropertyGroup] | None,
    score: float | None = None,
) -> db.UnicodeCharacterResponse:
    response_dict = db_ctx.get_character_properties(codepoint, show_props)
    if score:
        response_dict["score"] = float(f"{score:.1f}")
    return db.UnicodeCharacterResponse(**response_dict)
