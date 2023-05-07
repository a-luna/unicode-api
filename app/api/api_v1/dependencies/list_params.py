from http import HTTPStatus

from fastapi import HTTPException, Query

from app.data.cache import cached_data
from app.data.encoding import get_codepoint_string
from app.docs.dependencies.custom_parameters import (
    CODEPOINT_EXAMPLES,
    CODEPOINT_INVALID_ERROR,
    CODEPOINT_REGEX,
    ENDING_BEFORE_BLOCK_ID_DESCRIPTION,
    ENDING_BEFORE_CODEPOINT_DESCRIPTION,
    LIMIT_DESCRIPTION,
    STARTING_AFTER_BLOCK_ID_DESCRIPTION,
    STARTING_AFTER_CODEPOINT_DESCRIPTION,
)


def get_decimal_number_from_hex_codepoint(codepoint: str) -> int:
    match = CODEPOINT_REGEX.match(codepoint)
    if not match:
        raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=CODEPOINT_INVALID_ERROR)
    groups = match.groupdict()
    codepoint_dec = int(groups.get("codepoint_prefix", "0") or groups.get("codepoint", "0"), 16)
    if not cached_data.codepoint_is_in_unicode_range(codepoint_dec):
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail=(
                f"Codepoint {get_codepoint_string(codepoint_dec)} is not within the range of unicode "
                "characters (U+0000 to U+10FFFF)."
            ),
        )
    return codepoint_dec


class ListParameters:
    def __init__(
        self,
        limit: int = Query(default=None, ge=1, le=100, description=LIMIT_DESCRIPTION),
        starting_after: str
        | None = Query(
            default=None,
            description=STARTING_AFTER_CODEPOINT_DESCRIPTION,
            examples=CODEPOINT_EXAMPLES,
        ),
        ending_before: str
        | None = Query(
            default=None,
            description=ENDING_BEFORE_CODEPOINT_DESCRIPTION,
            examples=CODEPOINT_EXAMPLES,
        ),
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
        self.ending_before: int | None = get_decimal_number_from_hex_codepoint(ending_before) if ending_before else None
        self.starting_after: int | None = (
            get_decimal_number_from_hex_codepoint(starting_after) if starting_after else None
        )


class ListParametersDecimal:
    def __init__(
        self,
        limit: int = Query(default=None, ge=1, le=100, description=LIMIT_DESCRIPTION),
        starting_after: int
        | None = Query(
            default=None,
            ge=1,
            le=len(cached_data.blocks),
            description=STARTING_AFTER_BLOCK_ID_DESCRIPTION,
        ),
        ending_before: int
        | None = Query(
            default=None,
            ge=1,
            le=len(cached_data.blocks),
            description=ENDING_BEFORE_BLOCK_ID_DESCRIPTION,
        ),
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
