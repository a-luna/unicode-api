# flake8: noqa
from sqlalchemy import column, event, select, text
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text
from sqlmodel import create_engine, Session, SQLModel

from app.core.config import DB_FILE, DB_URL
from app.core.enums import UnicodeBlockName
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
from app.schemas.prop_groups import get_all_db_columns_in_group, update_character_properties

CJK_UNIFIED_BLOCKS = [
    UnicodeBlockName.CJK_UNIFIED_IDEOGRAPHS,
    UnicodeBlockName.CJK_UNIFIED_IDEOGRAPHS_EXTENSION_A,
    UnicodeBlockName.CJK_UNIFIED_IDEOGRAPHS_EXTENSION_B,
    UnicodeBlockName.CJK_UNIFIED_IDEOGRAPHS_EXTENSION_C,
    UnicodeBlockName.CJK_UNIFIED_IDEOGRAPHS_EXTENSION_D,
    UnicodeBlockName.CJK_UNIFIED_IDEOGRAPHS_EXTENSION_E,
    UnicodeBlockName.CJK_UNIFIED_IDEOGRAPHS_EXTENSION_F,
    UnicodeBlockName.CJK_UNIFIED_IDEOGRAPHS_EXTENSION_G,
    UnicodeBlockName.CJK_UNIFIED_IDEOGRAPHS_EXTENSION_H,
]

CJK_COMPATIBILITY_BLOCKS = [
    UnicodeBlockName.CJK_COMPATIBILITY_IDEOGRAPHS,
    UnicodeBlockName.CJK_COMPATIBILITY_IDEOGRAPHS_SUPPLEMENT,
]

TANGUT_BLOCKS = [
    UnicodeBlockName.TANGUT,
    UnicodeBlockName.TANGUT_SUPPLEMENT,
]

SINGLE_NO_NAME_BLOCKS = [
    UnicodeBlockName.HIGH_SURROGATES,
    UnicodeBlockName.HIGH_PRIVATE_USE_SURROGATES,
    UnicodeBlockName.LOW_SURROGATES,
    UnicodeBlockName.PRIVATE_USE_AREA,
    UnicodeBlockName.SUPPLEMENTARY_PRIVATE_USE_AREA_A,
    UnicodeBlockName.SUPPLEMENTARY_PRIVATE_USE_AREA_B,
]

NO_NAME_BLOCKS = CJK_UNIFIED_BLOCKS + CJK_COMPATIBILITY_BLOCKS + TANGUT_BLOCKS + SINGLE_NO_NAME_BLOCKS


def create_db_and_tables():
    if DB_FILE.exists():
        DB_FILE.unlink()
    SQLModel.metadata.create_all(engine)
    with engine.connect() as con:
        for create_index_sql in generate_raw_sql_for_all_covering_indexes():
            con.execute(text(create_index_sql))


def generate_raw_sql_for_covering_index(prop_group: CharPropertyGroup) -> str:
    columns = get_all_db_columns_in_group(prop_group)
    return f'CREATE INDEX ix_character_{prop_group.index_name} ON character ({", ".join(columns)})' if columns else ""


def generate_raw_sql_for_all_covering_indexes() -> list[str]:
    sql_statements = [
        generate_raw_sql_for_covering_index(prop_group)
        for prop_group in CharPropertyGroup
        if prop_group != CharPropertyGroup.ALL
    ]
    return [sql for sql in sql_statements if sql]


def get_character_properties(engine: Engine, codepoint: int, prop_group: CharPropertyGroup, no_name: bool = False):
    char: dict[str, bool | int | str] = {"codepoint_dec": codepoint}
    table_name = "character_no_name" if no_name else "character"
    with engine.connect() as con:
        columns = [column(col_name) for col_name in get_all_db_columns_in_group(prop_group)]
        if columns:
            for row in con.execute(
                select(columns).select_from(text(table_name)).where(column("codepoint_dec") == codepoint)
            ):
                char = dict(row._mapping)
    return update_character_properties(char, prop_group)


def get_session():
    with Session(engine) as session:
        yield (session, engine)


def _fk_pragma_on_connect(dbapi_con, _):
    dbapi_con.execute("pragma journal_mode=OFF")
    dbapi_con.execute("PRAGMA synchronous=OFF")
    dbapi_con.execute("PRAGMA cache_size=100000")


engine = create_engine(DB_URL, echo=False, connect_args={"check_same_thread": False})
event.listen(engine, "connect", _fk_pragma_on_connect)
