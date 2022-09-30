from typing import List
from app.schemas.block import UnicodeBlock
from app.schemas.camel_model import CamelModel
from app.schemas.character import UnicodeCharacterMinimal


class CharToBlockMap(CamelModel):
    block: UnicodeBlock
    characters_in_block: List[UnicodeCharacterMinimal]

