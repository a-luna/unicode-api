from typing import Annotated

from fastapi import Query

from unicode_api.docs.dependencies.custom_parameters import (
    MIN_SCORE_DESCRIPTION,
    MIN_SEARCH_RESULT_SCORE,
    PAGE_NUMBER_DESCRIPTION,
    PER_PAGE_DESCRIPTION,
    SEARCH_CHAR_NAME_DESCRIPTION,
)


class CharacterSearchParameters:
    def __init__(
        self,
        name: Annotated[str, Query(description=SEARCH_CHAR_NAME_DESCRIPTION)],
        min_score: Annotated[
            int | None, Query(ge=MIN_SEARCH_RESULT_SCORE, le=100, description=MIN_SCORE_DESCRIPTION)
        ] = None,
        per_page: Annotated[int | None, Query(ge=1, le=100, description=PER_PAGE_DESCRIPTION)] = None,
        page: Annotated[int | None, Query(ge=1, description=PAGE_NUMBER_DESCRIPTION)] = None,
    ):
        self.name = name
        self.min_score = min_score or 80
        self.per_page = per_page or 10
        self.page = page or 1
