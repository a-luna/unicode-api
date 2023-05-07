# flake8: noqa
from sqlalchemy import event
from sqlmodel import create_engine

from app.core.config import DB_URL
from app.schemas.models.block import UnicodeBlock, UnicodeBlockResponse, UnicodeBlockResult
from app.schemas.models.camel_model import GenericCamelModel, GenericModel
from app.schemas.models.character import (
    UnicodeCharacter,
    UnicodeCharacterBase,
    UnicodeCharacterNoName,
    UnicodeCharacterResponse,
    UnicodeCharacterResult,
)
from app.schemas.models.pagination import PaginatedList, PaginatedSearchResults
from app.schemas.models.plane import UnicodePlane, UnicodePlaneResponse


def _fk_pragma_on_connect(dbapi_con, _):
    dbapi_con.execute("pragma journal_mode=OFF")
    dbapi_con.execute("PRAGMA synchronous=OFF")
    dbapi_con.execute("PRAGMA cache_size=100000")


engine = create_engine(DB_URL, echo=False, connect_args={"check_same_thread": False})
event.listen(engine, "connect", _fk_pragma_on_connect)
