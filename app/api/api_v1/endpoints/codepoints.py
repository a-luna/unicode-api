from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

import app.db.models as db
from app.api.api_v1.dependencies.filter_param_matcher import FilterParameterMatcher
from app.api.api_v1.dependencies.util import get_decimal_number_from_hex_codepoint
from app.api.api_v1.endpoints.util import get_character_details
from app.db.session import DBSession, get_session
from app.docs.dependencies.custom_parameters import (
    CODEPOINT_PATH_PARAM_DESSCRIPTION,
    VERBOSE_DESCRIPTION,
    get_description_and_values_table_for_property_group,
)

router = APIRouter()


@router.get(
    "/{codepoint}",
    response_model=db.UnicodeCharacterResponse,
    response_model_exclude_unset=True,
)
def get_unicode_character_at_codepoint(
    db_ctx: Annotated[DBSession, Depends(get_session)],
    codepoint: Annotated[str, Path(description=CODEPOINT_PATH_PARAM_DESSCRIPTION)],
    show_props: Annotated[list[str], Query(description=get_description_and_values_table_for_property_group())] = None,  # type: ignore[reportArgumentType]
    verbose: Annotated[bool | None, Query(description=VERBOSE_DESCRIPTION)] = None,
):
    codepoint_dec = get_decimal_number_from_hex_codepoint(codepoint)
    if show_props:
        param_matcher = FilterParameterMatcher("show_props", db.CharPropertyGroup)
        result = param_matcher.parse_filter_params(show_props)
        if result.failure:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.error)
        prop_groups = result.value
    else:
        prop_groups = None
    if not verbose:
        verbose = False
    return get_character_details(db_ctx, codepoint_dec, prop_groups, verbose=verbose)
