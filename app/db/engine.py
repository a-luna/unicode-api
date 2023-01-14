# flake8: noqa
from sqlalchemy import event
from sqlalchemy.sql import text
from sqlmodel import create_engine, Session, SQLModel

from app.core.config import DB_FILE, DB_URL
from app.db.constants import CHARACTER_PROPERTY_GROUPS
from app.schemas.enums import CharPropertyGroup
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


def get_session():
    with Session(engine) as session:
        yield (session, engine)


def create_db_and_tables():
    if DB_FILE.exists():
        DB_FILE.unlink()
    SQLModel.metadata.create_all(engine)
    with engine.connect() as con:
        for create_index_sql in generate_raw_sql_for_all_covering_indexes():
            con.execute(text(create_index_sql))


def generate_raw_sql_for_all_covering_indexes() -> list[str]:
    sql_statements = [
        generate_raw_sql_for_covering_index(prop_group)
        for prop_group in CharPropertyGroup
        if prop_group != CharPropertyGroup.All
    ]
    return [sql for sql in sql_statements if sql]


def generate_raw_sql_for_covering_index(prop_group: CharPropertyGroup) -> str:
    columns = get_all_db_columns_in_group(prop_group)
    return f'CREATE INDEX ix_character_{prop_group.index_name} ON character ({", ".join(columns)})' if columns else ""


def _fk_pragma_on_connect(dbapi_con, _):
    dbapi_con.execute("pragma journal_mode=OFF")
    dbapi_con.execute("PRAGMA synchronous=OFF")
    dbapi_con.execute("PRAGMA cache_size=100000")


def get_all_db_columns_in_group(prop_group: CharPropertyGroup) -> list[str]:
    return [prop["name_in"] for prop in CHARACTER_PROPERTY_GROUPS[prop_group] if prop["db_column"]]


engine = create_engine(DB_URL, echo=False, connect_args={"check_same_thread": False})
event.listen(engine, "connect", _fk_pragma_on_connect)
