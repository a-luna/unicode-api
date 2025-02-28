from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.camel_model import CamelModel
from app.models.util import normalize_string_lm3

if TYPE_CHECKING:  # pragma: no cover
    from app.models.character import UnicodeCharacter, UnicodeCharacterUnihan
    from app.models.plane import UnicodePlane


class UnicodeBlockResponse(CamelModel):
    id: int | None
    name: str = Field(index=True)
    short_name: str
    plane: str
    start: str
    finish: str
    total_allocated: int | None
    total_defined: int | None


class UnicodeBlockResult(UnicodeBlockResponse):
    score: float | None

    def __str__(self) -> str:
        name = self.name.replace(" ", "_")
        return f"{name} ({self.start}...{self.finish})"


class UnicodeBlock(CamelModel, table=True):
    __tablename__ = "block"  # type: ignore  # noqa: PGH003

    id: int | None = Field(default=None, primary_key=True)
    long_name: str = Field(index=True)
    short_name: str
    start: str
    finish: str
    start_dec: int
    finish_dec: int
    total_allocated: int
    total_defined: int

    plane_id: int = Field(foreign_key="plane.id")
    plane: "UnicodePlane" = Relationship(back_populates="blocks")  # type: ignore  # noqa: PGH003
    characters: list["UnicodeCharacter"] = Relationship(back_populates="block")  # type: ignore  # noqa: PGH003
    unihan_characters: list["UnicodeCharacterUnihan"] = Relationship(back_populates="block")  # type: ignore  # noqa: PGH003

    @property
    def display_name(self) -> str:
        return self.long_name

    @property
    def short_and_long_name_differ(self) -> bool:
        if self.long_name is None or self.short_name is None:
            return False
        return normalize_string_lm3(self.long_name) != normalize_string_lm3(self.short_name)

    def as_response(self) -> "UnicodeBlockResponse":
        block_dict = self.model_dump(by_alias=True)
        block_dict["name"] = self.long_name
        block_dict["short_name"] = self.short_name
        block_dict["plane"] = self.plane.abbreviation
        block_dict["start"] = f"U+{self.start}"
        block_dict["finish"] = f"U+{self.finish}"
        return UnicodeBlockResponse(**block_dict)

    def as_search_result(self, score=None) -> "UnicodeBlockResult":
        block_dict = self.model_dump(by_alias=True)
        block_dict["name"] = self.long_name
        block_dict["short_name"] = self.short_name
        block_dict["plane"] = self.plane.abbreviation
        block_dict["start"] = f"U+{self.start}"
        block_dict["finish"] = f"U+{self.finish}"
        block_dict["score"] = f"{score:.1f}"
        return UnicodeBlockResult(**block_dict)
