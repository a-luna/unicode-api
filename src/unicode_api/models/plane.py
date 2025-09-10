from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from unicode_api.models.camel_model import CamelModel

if TYPE_CHECKING:  # pragma: no cover
    from unicode_api.models.block import UnicodeBlock
    from unicode_api.models.character import UnicodeCharacter, UnicodeCharacterUnihan


class UnicodePlaneResponse(CamelModel):
    number: int
    name: str
    abbreviation: str
    start: str
    finish: str
    total_allocated: int
    total_defined: int


class UnicodePlane(UnicodePlaneResponse, table=True):
    __tablename__: str = "plane"  # type: ignore  # noqa: PGH003

    id: int | None = Field(default=None, primary_key=True)
    start_dec: int
    finish_dec: int
    start_block_id: int
    finish_block_id: int

    blocks: list["UnicodeBlock"] = Relationship(back_populates="plane")
    characters: list["UnicodeCharacter"] = Relationship(back_populates="plane")
    unihan_characters: list["UnicodeCharacterUnihan"] = Relationship(back_populates="plane")

    def as_response(self) -> "UnicodePlaneResponse":
        plane_dict = self.model_dump(by_alias=True)
        plane_dict["start"] = f"U+{self.start}" if not self.start.startswith("U+") else self.start
        plane_dict["finish"] = f"U+{self.finish}" if not self.finish.startswith("U+") else self.finish
        return UnicodePlaneResponse(**plane_dict)
