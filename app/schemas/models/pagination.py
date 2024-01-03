from typing import Generic, TypeVar

from app.schemas.models.camel_model import GenericCamelModel

T = TypeVar("T")


class PaginatedList(GenericCamelModel[T], Generic[T]):
    url: str
    total_results: int | None = None
    has_more: bool
    data: list[T]


class PaginatedSearchResults(GenericCamelModel[T], Generic[T]):
    url: str
    query: str | None = None
    filter_settings: dict[str, str] | None = None
    has_more: bool
    current_page: int
    next_page: int | None = None
    total_results: int
    results: list[T]
