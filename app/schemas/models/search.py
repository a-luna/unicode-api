from typing import Generic, TypeVar

from app.schemas.models.camel_model import GenericCamelModel

T = TypeVar("T")


class SearchResults(GenericCamelModel, Generic[T]):
    query: str
    total_results: int
    results: list[T]
