from sqlmodel import Field, Relationship

from app.schemas.models.camel_model import CamelModel


class UnicodeBlockBase(CamelModel):
    name: str = Field(index=True)
    start: str
    finish: str
    total_allocated: int
    total_defined: int

    plane_id: int = Field(foreign_key="plane.id")


class UnicodeBlockResponse(CamelModel):
    id: int | None
    name: str = Field(index=True)
    plane: str
    start: str
    finish: str
    total_allocated: int | None
    total_defined: int | None


class UnicodeBlockResult(UnicodeBlockResponse):
    score: float | None


class UnicodeBlock(UnicodeBlockBase, table=True):
    __tablename__ = "block"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    start_dec: int
    finish_dec: int

    plane: "UnicodePlane" = Relationship(back_populates="blocks")  # type: ignore
    characters: list["UnicodeCharacter"] = Relationship(back_populates="block")  # type: ignore
    characters_no_name: list["UnicodeCharacterNoName"] = Relationship(back_populates="block")  # type: ignore

    def as_response(self) -> "UnicodeBlockResponse":
        block_dict = self.dict(by_alias=True)
        block_dict["plane"] = self.plane.abbreviation
        block_dict["start"] = f"U+{self.start}"
        block_dict["finish"] = f"U+{self.finish}"
        return UnicodeBlockResponse(**block_dict)

    def as_search_result(self, score=None) -> "UnicodeBlockResult":
        block_dict = self.dict(by_alias=True)
        block_dict["plane"] = self.plane.abbreviation
        block_dict["start"] = f"U+{self.start}"
        block_dict["finish"] = f"U+{self.finish}"
        block_dict["score"] = f"{score:.1f}"
        return UnicodeBlockResult(**block_dict)
