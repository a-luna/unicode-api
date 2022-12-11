from app.schemas.camel_model import CamelModel
from app.schemas.character import UnicodeCharacterResult


class UnicodeBlockBase(CamelModel):
    id: int
    name: str
    plane: str
    start: str
    finish: str


class UnicodeBlockResult(UnicodeBlockBase):
    score: float | None
    link: str

    def __str__(self):
        return (
            "UnicodeBlockResult<"
            f"score={self.score}, "
            f"name={self.name}, "
            f"start={self.start}, "
            f"finish={self.finish}"
            ">"
        )


class UnicodeBlock(UnicodeBlockBase):
    total_allocated: int
    total_defined: int

    def __str__(self):
        return self.name

    def __repr__(self):
        return (
            "UnicodeBlock<"
            f'name="{self.name}", '
            f'plane="{self.plane}", '
            f'start="{self.start}", '
            f'finish="{self.finish}", '
            f"total_allocated={self.total_allocated}, "
            f"total_defined={self.total_defined}"
            ">"
        )


class UnicodeBlockInternal(UnicodeBlock):
    start_dec: int
    finish_dec: int

    def __str__(self):
        return (
            "UnicodeBlockInternal<"
            f"score={self.score}, "
            f"name={self.name}, "
            f"start={self.start}, "
            f"finish={self.finish}, "
            f"start_dec={self.start_dec}, "
            f"finish_dec={self.finish_dec}"
            ">"
        )


class CharToBlockMap(CamelModel):
    block: UnicodeBlock
    characters_in_block: list[UnicodeCharacterResult]
