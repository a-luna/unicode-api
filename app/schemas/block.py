from sqlmodel import Field, Relationship
from app.schemas.camel_model import CamelModel


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
    start_dec: int | None
    finish_dec: int | None
    total_allocated: int | None
    total_defined: int | None


class UnicodeBlock(UnicodeBlockBase, table=True):

    __tablename__ = "block"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    start_dec: int
    finish_dec: int

    plane: "UnicodePlane" = Relationship(back_populates="blocks")  # type: ignore
    characters: list["UnicodeCharacter"] = Relationship(back_populates="block")  # type: ignore

    @classmethod
    def responsify(cls, block) -> "UnicodeBlockResponse":
        block_dict = block.dict(by_alias=True)
        block_dict["plane"] = block.plane.abbreviation
        block_dict["start"] = f"U+{block.start}"
        block_dict["finish"] = f"U+{block.finish}"
        return UnicodeBlockResponse(**block_dict)


class UnicodeBlockResult(UnicodeBlockResponse):
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
