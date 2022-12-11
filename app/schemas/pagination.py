from typing import Generic, TypeVar

from app.schemas.camel_model import GenericCamelModel

T = TypeVar("T")


class PaginatedList(GenericCamelModel, Generic[T]):
    url: str
    total_results: int | None
    has_more: bool
    data: list[T]


class PaginatedSearchResults(GenericCamelModel, Generic[T]):
    url: str
    query: str
    total_results: int
    has_more: bool
    next_page: int | None
    results: list[T]
