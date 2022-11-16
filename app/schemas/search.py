from app.schemas.camel_model import CamelModel
from app.schemas.character import UnicodeCharacterMinimal


class FuzzySearchResult(CamelModel):
    character: str
    score: int
    details: UnicodeCharacterMinimal


class ResultsForScore(CamelModel):
    score: int
    total_results: int
    results: list[UnicodeCharacterMinimal]


class SearchResults(CamelModel):
    query: str
    total_results: int
    results_by_score: list[ResultsForScore]
