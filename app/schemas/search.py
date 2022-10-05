from app.schemas.camel_model import CamelModel
from app.schemas.character import UnicodeCharacter


class FuzzySearchResult(CamelModel):
    character: str
    score: int
    details: UnicodeCharacter


class SearchResults(CamelModel):
    query: str
    total_results: int
    results: list[FuzzySearchResult]
