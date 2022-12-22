from sqlmodel import Field, Relationship

from app.schemas.models.camel_model import CamelModel


class UnicodePlaneResponse(CamelModel):
    number: int
    name: str
    abbreviation: str
    start: str
    finish: str
    total_allocated: int
    total_defined: int


class UnicodePlane(UnicodePlaneResponse, table=True):

    __tablename__ = "plane"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    start_dec: int
    finish_dec: int
    start_block_id: int
    finish_block_id: int

    blocks: list["UnicodeBlock"] = Relationship(back_populates="plane")  # type: ignore
    characters: list["UnicodeCharacter"] = Relationship(back_populates="plane")  # type: ignore
    characters_no_name: list["UnicodeCharacterNoName"] = Relationship(back_populates="plane")  # type: ignore

    @classmethod
    def responsify(cls, plane) -> "UnicodePlaneResponse":
        plane.start = f"U+{plane.start}"
        plane.finish = f"U+{plane.finish}"
        return plane
