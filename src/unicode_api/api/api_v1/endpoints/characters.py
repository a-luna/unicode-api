from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

import unicode_api.db.models as db
from unicode_api.api.api_v1.dependencies import (
    CharacterSearchParameters,
    FilterSettings,
    ListParameters,
    UnicodeBlockQueryParamResolver,
)
from unicode_api.api.api_v1.dependencies.filter_param_matcher import CharacterPropGroupParameterMatcher
from unicode_api.api.api_v1.endpoints.util import get_character_details
from unicode_api.api.api_v1.pagination import paginate_search_results
from unicode_api.core.cache import cached_data
from unicode_api.core.encoding import get_codepoint_string
from unicode_api.core.util import convert_keys_to_camel_case
from unicode_api.db.session import DBSession, get_session
from unicode_api.docs.dependencies.custom_parameters import (
    UNICODE_CHAR_STRING_DESCRIPTION,
    VERBOSE_DESCRIPTION,
    get_description_and_values_table_for_property_group,
)

router = APIRouter()


@router.get(
    "",
    response_model=db.PaginatedList[db.UnicodeCharacterResponse],
    response_model_exclude_unset=True,
)
def list_all_unicode_characters(
    db_ctx: Annotated[DBSession, Depends(get_session)],
    list_params: Annotated[ListParameters, Depends()],
    block: Annotated[UnicodeBlockQueryParamResolver, Depends()],
):
    (start, stop) = get_char_list_endpoints(list_params, block)
    return {
        "url": f"{db_ctx.api_settings.API_VERSION}/characters",
        "has_more": stop <= block.finish,
        "data": [responsify_character_details(db_ctx, codepoint, []) for codepoint in range(start, stop)],
    }


@router.get(
    "/search",
    response_model=db.PaginatedSearchResults[db.UnicodeCharacterResult],
    response_model_exclude_unset=True,
)
def search_unicode_characters_by_name(
    db_ctx: Annotated[DBSession, Depends(get_session)],
    search_parameters: Annotated[CharacterSearchParameters, Depends()],
):
    response_data = {"url": f"{db_ctx.api_settings.API_VERSION}/characters/search", "query": search_parameters.name}
    search_results = cached_data.search_characters_by_name(search_parameters.name, search_parameters.min_score)
    return get_paginated_character_list(
        db_ctx,
        search_results,
        [db.CharPropertyGroup.MINIMUM],
        search_parameters.per_page,
        search_parameters.page,
        response_data,
        False,
    )


@router.get(
    "/filter",
    response_model=db.PaginatedSearchResults[db.UnicodeCharacterResponse],
    response_model_exclude_unset=True,
)
def filter_unicode_characters(
    db_ctx: Annotated[DBSession, Depends(get_session)], filter_settings: Annotated[FilterSettings, Depends()]
):
    if not filter_settings.did_parse:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=filter_settings.error_message,
        )
    if filter_settings.no_settings_provided:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filter settings were specified in the request.",
        )
    response_data = {
        "url": f"{db_ctx.api_settings.API_VERSION}/characters/filter",
        "filter_settings": filter_settings.parsed,
    }
    codepoints = db_ctx.filter_all_characters(filter_settings.params)
    filter_results = [(cp, None) for cp in codepoints]
    return get_paginated_character_list(
        db_ctx,
        filter_results,
        filter_settings.show_props,
        filter_settings.per_page,
        filter_settings.page,
        response_data,
        filter_settings.verbose,
    )


@router.get(
    "/-/{string:path}",
    response_model=list[db.UnicodeCharacterResponse],
    response_model_exclude_unset=True,
)
def get_unicode_character_details(
    db_ctx: Annotated[DBSession, Depends(get_session)],
    string: Annotated[str, Path(description=UNICODE_CHAR_STRING_DESCRIPTION)],
    show_props: Annotated[list[str], Query(description=get_description_and_values_table_for_property_group())] = None,  # type: ignore[reportArgumentType]
    verbose: Annotated[bool | None, Query(description=VERBOSE_DESCRIPTION)] = None,
):
    if show_props:
        param_matcher = CharacterPropGroupParameterMatcher("show_props")
        result = param_matcher.parse_filter_params(show_props)
        if result.failure or not result.value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.error)
        prop_groups = result.value
    else:
        prop_groups = []
    if verbose is None:
        verbose = False
    return [get_character_details(db_ctx, ord(char), prop_groups, verbose=verbose) for char in string]


def get_char_list_endpoints(list_params: ListParameters, block: UnicodeBlockQueryParamResolver) -> tuple[int, int]:
    start = block.start
    if list_params.starting_after:
        start = list_params.starting_after + 1
    if list_params.ending_before:
        start = list_params.ending_before - list_params.limit
    stop = min(block.finish + 1, start + list_params.limit)
    if start < block.start or start > stop:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"The starting codepoint value {get_codepoint_string(start)} is outside the range of characters "
                f"{get_codepoint_string(block.start)}...{get_codepoint_string(block.finish)} ({block.name})"
            ),
        )
    return (start, stop)


def get_paginated_character_list(
    db_ctx: DBSession,
    results: list[tuple[int, Any]],
    show_props: list[db.CharPropertyGroup],
    per_page: int,
    page: int,
    response_data: dict[str, Any],
    verbose: bool,
):
    codepoints = [cp for (cp, _) in results]
    if codepoints:
        result = paginate_search_results(codepoints, per_page, page)
        if result.failure:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.error)
        paginated = result.value or {}
        start = paginated.pop("start", 0)
        end = paginated.pop("end", 0)
        paginated["results"] = [
            responsify_character_details(db_ctx, cp, show_props, score, verbose) for (cp, score) in results[start:end]
        ]
        return response_data | paginated
    return response_data | {
        "current_page": 0,
        "total_results": 0,
        "has_more": False,
        "results": [],
    }


def responsify_character_details(
    db_ctx: DBSession,
    codepoint: int,
    show_props: list[db.CharPropertyGroup],
    score: float | None = None,
    verbose: bool = False,
) -> dict[str, Any]:
    return convert_keys_to_camel_case(get_character_details(db_ctx, codepoint, show_props, score, verbose=verbose))
