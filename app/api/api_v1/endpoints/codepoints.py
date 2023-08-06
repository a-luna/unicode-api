from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query

import app.db.models as db
from app.api.api_v1.dependencies.db_session import DBSession, get_session
from app.api.api_v1.dependencies.filter_params import FilterParameterMatcher
from app.api.api_v1.dependencies.util import get_decimal_number_from_hex_codepoint
from app.api.api_v1.endpoints.util import get_character_details
from app.docs.dependencies.custom_parameters import (
    CODEPOINT_PATH_PARAM_DESSCRIPTION,
    VERBOSE_DESCRIPTION,
    get_description_and_values_table_for_property_group,
)
from app.schemas.enums.property_group import CharPropertyGroup

PropertyGroupMatcher = FilterParameterMatcher[CharPropertyGroup]("show_props", CharPropertyGroup)
router = APIRouter()


@router.get(
    "/{hex}",
    response_model=db.UnicodeCharacterResponse,
    response_model_exclude_unset=True,
)
def get_unicode_character_at_codepoint(
    db_ctx: Annotated[DBSession, Depends(get_session)],
    hex: Annotated[str, Path(description=CODEPOINT_PATH_PARAM_DESSCRIPTION)],
    show_props: Annotated[
        list[str] | None, Query(description=get_description_and_values_table_for_property_group())
    ] = None,
    verbose: Annotated[bool | None, Query(description=VERBOSE_DESCRIPTION)] = None,
):
    codepoint_dec = get_decimal_number_from_hex_codepoint(hex)
    if show_props:
        result = PropertyGroupMatcher.parse_enum_values(show_props)
        if result.failure:
            raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=result.error)
        prop_groups = result.value
    else:
        prop_groups = None
    if not verbose:
        verbose = False
    return get_character_details(db_ctx, codepoint_dec, prop_groups, verbose=verbose)
