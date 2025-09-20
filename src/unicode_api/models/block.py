from typing import TYPE_CHECKING, Self

from sqlmodel import Field, Relationship

from unicode_api.models.camel_model import CamelModel
from unicode_api.models.util import normalize_string_lm3

if TYPE_CHECKING:  # pragma: no cover
    from unicode_api.custom_types import UnicodePropertyGroupValues
    from unicode_api.models.character import UnicodeCharacter, UnicodeCharacterUnihan
    from unicode_api.models.plane import UnicodePlane


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
    __tablename__: str = "block"  # type: ignore  # noqa: PGH003

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
    plane: "UnicodePlane" = Relationship(back_populates="blocks")
    characters: list["UnicodeCharacter"] = Relationship(back_populates="block")
    unihan_characters: list["UnicodeCharacterUnihan"] = Relationship(back_populates="block")

    @property
    def display_name(self) -> str:  # pragma: no cover
        return self.long_name

    @property
    def short_and_long_name_differ(self) -> bool:  # pragma: no cover
        if self.long_name and self.short_name:
            return normalize_string_lm3(self.long_name) != normalize_string_lm3(self.short_name)
        return False

    def as_response(self) -> "UnicodeBlockResponse":
        block_dict = self.model_dump(by_alias=True)
        block_dict["name"] = self.long_name
        block_dict["plane"] = self.plane.abbreviation
        block_dict["start"] = f"U+{self.start}"
        block_dict["finish"] = f"U+{self.finish}"
        return UnicodeBlockResponse(**block_dict)

    def as_search_result(self, score: float | None = None) -> "UnicodeBlockResult":
        block_dict = self.model_dump(by_alias=True)
        block_dict["name"] = self.long_name
        block_dict["plane"] = self.plane.abbreviation
        block_dict["start"] = f"U+{self.start}"
        block_dict["finish"] = f"U+{self.finish}"
        block_dict["score"] = f"{score:.1f}"
        return UnicodeBlockResult(**block_dict)

    @classmethod
    def from_dict(cls, model_dict: "UnicodePropertyGroupValues") -> Self:
        return super().model_validate(model_dict)
