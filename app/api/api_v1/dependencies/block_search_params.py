from fastapi import Query

from app.docs.dependencies.custom_parameters import (
    MIN_SCORE_DESCRIPTION,
    PAGE_NUMBER_DESCRIPTION,
    PER_PAGE_DESCRIPTION,
    SEARCH_BLOCK_NAME_DESCRIPTION,
)


class BlockSearchParameters:
    def __init__(
        self,
        name: str = Query(description=SEARCH_BLOCK_NAME_DESCRIPTION),
        min_score: int | None = Query(default=None, ge=0, le=100, description=MIN_SCORE_DESCRIPTION),
        per_page: int | None = Query(default=None, ge=1, le=100, description=PER_PAGE_DESCRIPTION),
        page: int | None = Query(default=None, ge=1, description=PAGE_NUMBER_DESCRIPTION),
    ):
        self.name = name
        self.min_score = min_score or 80
        self.per_page = per_page or 10
        self.page = page or 1
