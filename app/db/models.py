# flake8: noqa
from app.schemas.models.block import UnicodeBlock, UnicodeBlockResponse, UnicodeBlockResult
from app.schemas.models.character import (
    UnicodeCharacter,
    UnicodeCharacterBase,
    UnicodeCharacterResponse,
    UnicodeCharacterResult,
    UnicodeCharacterUnihan,
)
from app.schemas.models.pagination import PaginatedList, PaginatedSearchResults
from app.schemas.models.plane import UnicodePlane, UnicodePlaneResponse

CHAR_TABLES = [UnicodeCharacter, UnicodeCharacterUnihan]
