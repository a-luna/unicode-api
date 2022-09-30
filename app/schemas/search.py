from app.schemas.camel_model import CamelModel
from app.schemas.character import UnicodeCharacter


class FuzzySearchResult(CamelModel):
    score: int
    details: UnicodeCharacter