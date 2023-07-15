from http import HTTPStatus
from typing import Annotated

from fastapi import HTTPException, Query

from app.data.cache import cached_data
from app.data.constants import MAX_CODEPOINT
from app.data.encoding import get_codepoint_string
from app.docs.dependencies.custom_parameters import (
    CODEPOINT_INVALID_ERROR,
    CODEPOINT_REGEX,
    ENDING_BEFORE_BLOCK_ID_DESCRIPTION,
    ENDING_BEFORE_CODEPOINT_DESCRIPTION,
    LIMIT_DESCRIPTION,
    STARTING_AFTER_BLOCK_ID_DESCRIPTION,
    STARTING_AFTER_CODEPOINT_DESCRIPTION,
)


def get_decimal_number_from_hex_codepoint(codepoint: str, starting_after: bool = True) -> int:
    match = CODEPOINT_REGEX.match(codepoint)
    if not match:
        raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=CODEPOINT_INVALID_ERROR)
    groups = match.groupdict()
    codepoint_dec = int(groups.get("codepoint_prefix", "0") or groups.get("codepoint", "0"), 16)
    lower_limit = 0 if starting_after else 1
    upper_limit = MAX_CODEPOINT if starting_after else MAX_CODEPOINT + 1
    if codepoint_dec >= lower_limit and codepoint_dec <= upper_limit:
        return codepoint_dec
    raise HTTPException(
        status_code=int(HTTPStatus.BAD_REQUEST),
        detail=(
            f"Codepoint {get_codepoint_string(codepoint_dec)} is not within the range of Unicode "
            "characters (U+0000 to U+10FFFF)."
        ),
    )


class ListParameters:
    def __init__(
        self,
        limit: Annotated[int | None, Query(ge=1, le=100, description=LIMIT_DESCRIPTION)] = None,
        starting_after: Annotated[str | None, Query(description=STARTING_AFTER_CODEPOINT_DESCRIPTION)] = None,
        ending_before: Annotated[str | None, Query(description=ENDING_BEFORE_CODEPOINT_DESCRIPTION)] = None,
    ):
        if ending_before and starting_after:
            raise HTTPException(
                status_code=int(HTTPStatus.BAD_REQUEST),
                detail=(
                    "Request contained values for BOTH 'ending_before' and 'starting_after', you must specify ONLY ONE "
                    "of these two values."
                ),
            )
        self.limit: int = limit or 10
        self.ending_before: int | None = (
            get_decimal_number_from_hex_codepoint(ending_before, starting_after=False) if ending_before else None
        )
        self.starting_after: int | None = (
            get_decimal_number_from_hex_codepoint(starting_after) if starting_after else None
        )


class ListParametersDecimal:
    def __init__(
        self,
        limit: Annotated[int | None, Query(ge=1, le=100, description=LIMIT_DESCRIPTION)] = None,
        starting_after: Annotated[
            int | None, Query(ge=1, le=len(cached_data.blocks), description=STARTING_AFTER_BLOCK_ID_DESCRIPTION)
        ] = None,
        ending_before: Annotated[
            int | None, Query(ge=1, le=len(cached_data.blocks), description=ENDING_BEFORE_BLOCK_ID_DESCRIPTION)
        ] = None,
    ):
        if ending_before and starting_after:
            raise HTTPException(
                status_code=int(HTTPStatus.BAD_REQUEST),
                detail=(
                    "Request contained values for BOTH 'ending_before' and 'starting_after', you must specify "
                    "ONLY ONE of these two values."
                ),
            )
        self.limit = limit or 10
        self.ending_before = ending_before
        self.starting_after = starting_after
