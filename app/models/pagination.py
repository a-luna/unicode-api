from typing import Generic, TypeVar

from app.models.camel_model import CamelModel, GenericCamelModel

T = TypeVar("T")


class UserFilterSettings(CamelModel):
    name: str | None = None
    cjk_definition: str | None = None
    block: list[str] | None = None
    category: list[str] | None = None
    version: list[str] | None = None
    script: list[str] | None = None
    bidi_class: list[str] | None = None
    decomp_type: list[str] | None = None
    line_break: list[str] | None = None
    ccc: list[str] | None = None
    num_type: list[str] | None = None
    join_type: list[str] | None = None
    flag: list[str] | None = None
    property_groups: list[str] | None = None


class PaginatedList(GenericCamelModel[T], Generic[T]):
    url: str
    total_results: int | None = None
    has_more: bool
    data: list[T]


class PaginatedSearchResults(GenericCamelModel[T], Generic[T]):
    url: str
    query: str | None = None
    filter_settings: UserFilterSettings | None = None
    has_more: bool
    current_page: int
    next_page: int | None = None
    total_results: int
    results: list[T]
