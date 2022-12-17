# flake8: noqa
from sqlmodel import Session, SQLModel, create_engine
from app.core.config import DB_FILE, DB_URL

from app.schemas.camel_model import GenericCamelModel, GenericModel
from app.schemas.plane import UnicodePlane, UnicodePlaneResponse
from app.schemas.block import UnicodeBlock, UnicodeBlockBase, UnicodeBlockResponse, UnicodeBlockResult
from app.schemas.character import (
    UnicodeCharacter,
    UnicodeCharacterBase,
    UnicodeCharacterResponse,
    UnicodeCharacterResult,
)
from app.schemas.pagination import PaginatedList, PaginatedSearchResults
from app.schemas.search import SearchResults

connect_args = {"check_same_thread": False}
engine = create_engine(DB_URL, echo=False, connect_args=connect_args)


def create_db_and_tables():
    if DB_FILE.exists():
        DB_FILE.unlink()
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
