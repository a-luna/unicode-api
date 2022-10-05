from app.schemas.camel_model import CamelModel
from app.schemas.character import UnicodeCharacterMinimal


class UnicodeBlockBlase(CamelModel):
    block: str
    start: str
    finish: str
    total_assigned: int


class UnicodeBlock(UnicodeBlockBlase):
    pass


class UnicodeBlockInternal(UnicodeBlockBlase):
    id: int
    start_dec: int
    finish_dec: int


class CharToBlockMap(CamelModel):
    block: UnicodeBlock
    characters_in_block: list[UnicodeCharacterMinimal]
