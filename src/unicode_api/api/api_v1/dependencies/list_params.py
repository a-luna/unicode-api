from typing import Annotated

from fastapi import HTTPException, Query, status

from unicode_api.api.api_v1.dependencies.util import get_decimal_number_from_hex_codepoint
from unicode_api.core.cache import cached_data
from unicode_api.docs.dependencies.custom_parameters import (
    ENDING_BEFORE_BLOCK_ID_DESCRIPTION,
    ENDING_BEFORE_CODEPOINT_DESCRIPTION,
    LIMIT_DESCRIPTION,
    STARTING_AFTER_BLOCK_ID_DESCRIPTION,
    STARTING_AFTER_CODEPOINT_DESCRIPTION,
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
                status_code=status.HTTP_400_BAD_REQUEST,
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
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Request contained values for BOTH 'ending_before' and 'starting_after', you must specify "
                    "ONLY ONE of these two values."
                ),
            )
        self.limit = limit or 10
        self.ending_before = ending_before
        self.starting_after = starting_after
