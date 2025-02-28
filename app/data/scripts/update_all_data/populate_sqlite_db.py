import json
from typing import TYPE_CHECKING

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import StatementError
from sqlmodel import Session, SQLModel

import app.db.models as db
from app.config.api_settings import UnicodeApiSettings
from app.constants import PROP_GROUP_INVALID_FOR_VERSION_ROW_ID
from app.core.result import Result
from app.data.scripts.script_types import (
    AllParsedUnicodeData,
    UnicodeModel,
    UnicodePropertyGroupType,
)
from app.data.util.spinners import Spinner
from app.db.character_props import PROPERTY_GROUPS
from app.db.engine import rw_db_engine as engine

if TYPE_CHECKING:  # pragma: no cover
    from app.custom_types import UnicodePropertyGroupMap, UnicodePropertyGroupValues

BATCH_SIZE = 5000
PROP_GROUP_DB_MODEL_MAP: dict[str, UnicodePropertyGroupType] = {
    "Age": db.Age,
    "Bidi_Class": db.Bidi_Class,
    "Bidi_Paired_Bracket_Type": db.Bidi_Paired_Bracket_Type,
    "Canonical_Combining_Class": db.Canonical_Combining_Class,
    "Decomposition_Type": db.Decomposition_Type,
    "East_Asian_Width": db.East_Asian_Width,
    "General_Category": db.General_Category,
    "Grapheme_Cluster_Break": db.Grapheme_Cluster_Break,
    "Hangul_Syllable_Type": db.Hangul_Syllable_Type,
    "Indic_Conjunct_Break": db.Indic_Conjunct_Break,
    "Indic_Positional_Category": db.Indic_Positional_Category,
    "Indic_Syllabic_Category": db.Indic_Syllabic_Category,
    "Jamo_Short_Name": db.Jamo_Short_Name,
    "Joining_Group": db.Joining_Group,
    "Joining_Type": db.Joining_Type,
    "Line_Break": db.Line_Break,
    "Numeric_Type": db.Numeric_Type,
    "Script": db.Script,
    "Sentence_Break": db.Sentence_Break,
    "Vertical_Orientation": db.Vertical_Orientation,
    "Word_Break": db.Word_Break,
}


def populate_sqlite_database(settings: UnicodeApiSettings, parsed_data: AllParsedUnicodeData) -> Result[None]:
    all_planes, all_blocks, non_unihan_chars, tangut_chars, unihan_chars = parsed_data

    parsed_data_table_map = {
        db.UnicodePlane: all_planes,
        db.UnicodeBlock: all_blocks,
        db.UnicodeCharacter: non_unihan_chars + tangut_chars,
        db.UnicodeCharacterUnihan: unihan_chars,
    }
    result = Result.Ok()
    with Session(engine) as session:
        create_db_and_tables(settings, engine)
        result = import_unicode_property_groups(settings, session)
        if result.failure:
            return result
        for table, parsed in parsed_data_table_map.items():
            result = import_parsed_unicode_data(session, parsed, table)
            if result.failure:
                break
        with engine.connect() as conn:
            conn.execute(text("VACUUM;"))
            conn.execute(text("ANALYZE;"))
    return Result.Ok() if result.success else Result.Fail(result.error)


def create_db_and_tables(settings: UnicodeApiSettings, engine: Engine) -> None:
    if settings.DB_FILE.exists():
        settings.DB_FILE.unlink()
    SQLModel.metadata.create_all(engine)
    with engine.connect() as con:
        for create_index_sql in generate_raw_sql_for_all_covering_indexes():
            con.execute(text(create_index_sql))


def generate_raw_sql_for_all_covering_indexes() -> list[str]:
    sql_statements = [
        generate_raw_sql_for_covering_index(prop_group)
        for prop_group in db.CharPropertyGroup
        if prop_group not in [db.CharPropertyGroup.ALL, db.CharPropertyGroup.NONE]
    ]
    return [sql for sql in sql_statements if sql]


def generate_raw_sql_for_covering_index(prop_group: db.CharPropertyGroup) -> str:
    columns = [prop["name_in"] for prop in PROPERTY_GROUPS[prop_group] if prop["db_column"]]
    table = "character" if "CJK" not in prop_group.name else "character_unihan"
    return f"CREATE INDEX ix_character_{prop_group.index_name} ON {table} ({', '.join(columns)})" if columns else ""


def import_unicode_property_groups(settings: UnicodeApiSettings, session: Session) -> Result[None]:
    prop_value_map: UnicodePropertyGroupMap = json.loads(settings.PROP_VALUES_JSON.read_text())
    spinner = Spinner()
    spinner.start("Adding tables for character property values to database...", total=len(PROP_GROUP_DB_MODEL_MAP))
    for prop_group, table in PROP_GROUP_DB_MODEL_MAP.items():
        if prop_group not in prop_value_map:
            result = add_placeholder_row_to_table(prop_group, table, session)
            if result.failure:
                spinner.failed(f"Error! {repr(result.error)}")
                return result
            spinner.increment()
            continue
        result = import_prop_group_values(prop_group, table, prop_value_map[prop_group], session)
        if result.failure:
            spinner.failed(f"Error! {repr(result.error)}")
            return result
        spinner.increment()
    spinner.successful("Successfully added tables for character property values to database")
    return Result.Ok()


def add_placeholder_row_to_table(group: str, table: UnicodePropertyGroupType, session: Session) -> Result[None]:
    try:
        session.add(table(id=PROP_GROUP_INVALID_FOR_VERSION_ROW_ID, short_name="N/A", long_name="N/A"))
        session.commit()
        return Result.Ok()
    except StatementError as ex:
        return Result.Fail(f"Error! {repr(ex)}")


def import_prop_group_values(
    group: str,
    table: UnicodePropertyGroupType,
    prop_values: dict[str, "UnicodePropertyGroupValues"],
    session: Session,
) -> Result[None]:
    try:
        for prop_value in prop_values.values():
            session.add(table(**prop_value))  # type: ignore[reportCallIssue]
        session.commit()
        return Result.Ok()
    except StatementError as ex:
        return Result.Fail(f"Error! {repr(ex)}")


def import_parsed_unicode_data[T: UnicodeModel](
    session: Session,
    parsed: list[T],
    table: type[T],
) -> Result[None]:
    batch = []
    spinner = Spinner()
    spinner.start(f"Adding parsed {table.__tablename__} data to database...", total=len(parsed))

    for obj in parsed:
        batch.append(obj)
        if len(batch) < BATCH_SIZE:
            continue
        result = perform_batch_insert(session, batch)
        if result.failure:
            spinner.failed(result.error)
            return result
        batch.clear()
        spinner.increment(amount=BATCH_SIZE)
    if batch:
        result = perform_batch_insert(session, batch)
        if result.failure:
            spinner.failed(result.error)
            return result
        batch.clear()
        spinner.increment(amount=len(batch))
    spinner.successful(f"Successfully added parsed {table.__tablename__} data to database")
    return Result.Ok()


def perform_batch_insert(session: Session, batch: list[UnicodeModel]) -> Result[None]:
    try:
        session.add_all(batch)
        session.commit()
        return Result.Ok()
    except StatementError as ex:
        return Result.Fail(f"Error! {repr(ex)}")
