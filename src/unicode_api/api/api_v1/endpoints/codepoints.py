from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

import unicode_api.db.models as db
from unicode_api.api.api_v1.dependencies.filter_param_matcher import CharacterPropGroupParameterMatcher
from unicode_api.api.api_v1.dependencies.util import get_decimal_number_from_hex_codepoint
from unicode_api.api.api_v1.endpoints.util import get_character_details
from unicode_api.db.session import DBSession, get_session
from unicode_api.docs.dependencies.custom_parameters import (
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
        param_matcher = CharacterPropGroupParameterMatcher("show_props")
        result = param_matcher.parse_filter_params(show_props)
        if result.failure:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.error)
        prop_groups = result.value or []
    else:
        prop_groups = []
    if not verbose:
        verbose = False
    return get_character_details(db_ctx, codepoint_dec, prop_groups, verbose=verbose)
