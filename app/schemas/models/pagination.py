from typing import Generic, TypeVar

from app.schemas.models.camel_model import GenericCamelModel

T = TypeVar("T")


class PaginatedList(GenericCamelModel, Generic[T]):
    url: str
    total_results: int | None
    has_more: bool
    data: list[T]


class PaginatedSearchResults(GenericCamelModel, Generic[T]):
    url: str
    query: str
    has_more: bool
    current_page: int
    next_page: int | None
    total_results: int
    results: list[T]
