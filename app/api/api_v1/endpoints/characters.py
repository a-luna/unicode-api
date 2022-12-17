from functools import lru_cache
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from rapidfuzz import process
from sqlmodel import Session

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
from app.core.util import get_codepoint_string
import app.core.db as db
from app.data.constants import NULL_CHARACTER_RESULT
from app.data.encoding import get_uri_encoded_value
from app.models.enums import CharPropertyGroup

router = APIRouter()


@router.get(
    "",
    response_model=db.PaginatedList[db.UnicodeCharacterResponse | db.UnicodeCharacterResult],
    response_model_exclude_unset=True,
)
def list_all_unicode_characters(
    list_params: ListParameters = Depends(),
    block: UnicodeBlockQueryParamResolver = Depends(),
    min_details: bool = Depends(get_min_details_query_param),
    session: Session = Depends(db.get_session),
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
            get_character_details(session, codepoint, min_details=min_details)
            for codepoint in range(start, stop)
            if codepoint in get_char_name_map(session)
        ],
    }


@router.get(
    "/search",
    response_model=db.PaginatedSearchResults[db.UnicodeCharacterResult],
    response_model_exclude_unset=True,
)
def search_unicode_characters_by_name(
    search_params: CharacterSearchParameters = Depends(),
    session: Session = Depends(db.get_session),
):
    params = {
        "url": f"{settings.API_VERSION}/characters/search",
        "query": search_params.name,
    }
    results = search_characters_by_name(session, search_params.name, search_params.min_score)
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
    session: Session = Depends(db.get_session),
):
    prop_group_weights = CharPropertyGroup.get_group_weights()
    show_props_sorted = sorted(show_props, key=lambda x: prop_group_weights[x.name])
    return [get_character_details(session, ord(char), show_props_sorted, min_details=False) for char in string]


@lru_cache
def get_char_name_map(session: Session) -> dict[int, str]:
    return {char.codepoint_dec: char.name.lower() for char in session.query(db.UnicodeCharacter).all()}


def search_characters_by_name(session: Session, query: str, score_cutoff: int = 80) -> list[db.UnicodeCharacterResult]:
    char_name_map = get_char_name_map(session)
    return [
        db.UnicodeCharacterResult(
            character=chr(result),
            name=char_name_map[result],
            codepoint=get_codepoint_string(result),
            score=float(f"{score:.1f}"),
            link=f"{settings.API_VERSION}/characters/{get_uri_encoded_value(chr(result))}",
        )
        for (_, score, result) in process.extract(query.lower(), char_name_map, limit=len(char_name_map))
        if score >= float(score_cutoff)
    ]


def get_character_details(
    session: Session,
    codepoint: int,
    show_props: list[CharPropertyGroup] = [CharPropertyGroup.BASIC],
    min_details: bool = True,
) -> db.UnicodeCharacterResponse | db.UnicodeCharacterResult:
    if min_details:
        return get_min_character_details(session, codepoint)
    if codepoint not in get_char_name_map(session):
        raise HTTPException(
            status_code=int(HTTPStatus.NOT_FOUND),
            detail=f"Failed to retrieve data for character matching codepoint {get_codepoint_string(codepoint)}.",
        )
    char = session.query(db.UnicodeCharacter).filter(db.UnicodeCharacter.codepoint_dec == codepoint).one()
    return db.UnicodeCharacter.responsify(char, show_props)


def get_min_character_details(session: Session, codepoint: int) -> db.UnicodeCharacterResult:
    char_name_map = get_char_name_map(session)
    if codepoint not in char_name_map:
        return NULL_CHARACTER_RESULT
    return db.UnicodeCharacterResult(
        character=chr(codepoint),
        name=char_name_map[codepoint],
        codepoint=get_codepoint_string(codepoint),
        score=None,
        link=f"{settings.API_VERSION}/characters/{get_uri_encoded_value(chr(codepoint))}",
    )
