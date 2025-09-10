"""
Populates a SQLite database with Unicode data, including planes, blocks, characters,
and property groups.

Functions:
    populate_sqlite_database(settings: UnicodeApiSettings, parsed_data: AllParsedUnicodeData) -> Result[None]:
        Orchestrates the entire population process, including schema creation, data
        import, and maintenance operations.

Constants:
    BATCH_SIZE (int): Number of records to insert per batch (5000).
    PROP_GROUP_DB_MODEL_MAP (dict[str, UnicodePropertyGroupType]): Maps property
        group names to their corresponding database model classes.
"""

import json
from collections.abc import Sequence
from typing import TYPE_CHECKING, cast

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import StatementError
from sqlmodel import Session, SQLModel

import unicode_api.db.models as db
from unicode_api.config.api_settings import UnicodeApiSettings
from unicode_api.constants import PROP_GROUP_INVALID_FOR_VERSION_ROW_ID
from unicode_api.core.result import Result
from unicode_api.data.scripts.script_types import (
    AllParsedUnicodeData,
    UnicodeModel,
    UnicodePropertyGroupType,
)
from unicode_api.data.util.spinner import Spinner
from unicode_api.db.character_props import PROPERTY_GROUPS
from unicode_api.db.engine import rw_db_engine as engine

if TYPE_CHECKING:  # pragma: no cover
    from unicode_api.custom_types import UnicodePropertyGroupMap, UnicodePropertyGroupValues

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
    """
    Populates the SQLite database with Unicode data.

    This function initializes the database and its tables, imports Unicode property groups,
    and inserts parsed Unicode data into the appropriate tables. It also performs database
    maintenance operations such as VACUUM and ANALYZE after data insertion.

    Args:
        settings (UnicodeApiSettings): The application settings containing database configuration.
        parsed_data (AllParsedUnicodeData): A tuple containing all parsed Unicode data, including planes,
            blocks, non-Unihan characters, Tangut characters, and Unihan characters.

    Returns:
        Result[None]: A Result object indicating success or failure. On failure, contains the error.
    """
    all_planes, all_blocks, non_unihan_chars, tangut_chars, unihan_chars = parsed_data

    parsed_data_table_map: dict[
        type[UnicodeModel],
        list[db.UnicodePlane] | list[db.UnicodeBlock] | list[db.UnicodeCharacter] | list[db.UnicodeCharacterUnihan],
    ] = {
        db.UnicodePlane: all_planes,
        db.UnicodeBlock: all_blocks,
        db.UnicodeCharacter: non_unihan_chars + tangut_chars,
        db.UnicodeCharacterUnihan: unihan_chars,
    }
    result = Result[None].Ok()
    with Session(engine) as session:
        _initialize_database_schema(settings, engine)
        result = _import_unicode_property_groups(settings, session)
        if result.failure:
            return result
        for table, parsed in parsed_data_table_map.items():
            result = _import_unicode_entities(session, parsed, table)
            if result.failure:
                break
        with engine.connect() as conn:
            conn.execute(text("VACUUM;"))
            conn.execute(text("ANALYZE;"))
    return Result[None].Ok() if result.success else Result[None].Fail(result.error)


def _initialize_database_schema(settings: UnicodeApiSettings, engine: Engine) -> None:
    if settings.db_file.exists():
        settings.db_file.unlink()
    SQLModel.metadata.create_all(engine)
    with engine.connect() as con:
        for create_index_sql in _generate_covering_index_statements():
            con.execute(text(create_index_sql))


def _generate_covering_index_statements() -> list[str]:
    sql_statements = [
        _generate_covering_index_sql(prop_group)
        for prop_group in db.CharPropertyGroup
        if prop_group not in [db.CharPropertyGroup.ALL, db.CharPropertyGroup.NONE]
    ]
    return [sql for sql in sql_statements if sql]


def _generate_covering_index_sql(prop_group: db.CharPropertyGroup) -> str:
    columns = [prop.name_in for prop in PROPERTY_GROUPS[prop_group] if prop.db_column]
    table = "character" if "CJK" not in prop_group.name else "character_unihan"
    return f"CREATE INDEX ix_character_{prop_group.index_name} ON {table} ({', '.join(columns)})" if columns else ""


def _import_unicode_property_groups(settings: UnicodeApiSettings, session: Session) -> Result[None]:
    prop_value_map: UnicodePropertyGroupMap = json.loads(settings.prop_values_json.read_text())
    spinner = Spinner()
    spinner.start("Adding tables for character property values to database...", total=len(PROP_GROUP_DB_MODEL_MAP))
    for prop_group_name, table in PROP_GROUP_DB_MODEL_MAP.items():
        if prop_group_name not in prop_value_map:
            result = _add_unsupported_property_group_placeholder(prop_group_name, table, session)
            if result.failure:
                spinner.failed(f"Error! {repr(result.error)}")
                return result
            spinner.increment()
            continue
        result = _import_property_group_values(
            prop_group_name,
            table,
            cast(dict[str, "UnicodePropertyGroupValues"], prop_value_map[prop_group_name]),
            session,
        )
        if result.failure:
            spinner.failed(f"Error! {repr(result.error)}")
            return result
        spinner.increment()
    spinner.successful("Successfully added tables for character property values to database")
    return Result[None].Ok()


def _add_unsupported_property_group_placeholder(
    group: str, table: UnicodePropertyGroupType, session: Session
) -> Result[None]:
    try:
        session.add(table(id=PROP_GROUP_INVALID_FOR_VERSION_ROW_ID, short_name="N/A", long_name="N/A"))
        session.commit()
        return Result[None].Ok()
    except StatementError as ex:
        return Result[None].Fail(f"Error! {repr(ex)}")


def _import_property_group_values(
    group: str,
    table: UnicodePropertyGroupType,
    prop_values: dict[str, "UnicodePropertyGroupValues"],
    session: Session,
) -> Result[None]:
    try:
        for prop_value in prop_values.values():
            session.add(table(**prop_value))  # type: ignore[reportCallIssue]
        session.commit()
        return Result[None].Ok()
    except StatementError as ex:
        return Result[None].Fail(
            f"Error occurred while importing values for property group {group}!\nDetails:{repr(ex)}"
        )


def _import_unicode_entities[T: UnicodeModel](
    session: Session,
    parsed: Sequence[T],
    table: type[T],
) -> Result[None]:
    batch: list[T] = []
    spinner = Spinner()
    spinner.start(f"Adding parsed {table.__tablename__} data to database...", total=len(parsed))

    for obj in parsed:
        batch.append(obj)
        if len(batch) < BATCH_SIZE:
            continue
        result = _perform_batch_insert(session, batch)
        if result.failure:
            spinner.failed(result.error)
            return result
        batch.clear()
        spinner.increment(amount=BATCH_SIZE)
    if batch:
        result = _perform_batch_insert(session, batch)
        if result.failure:
            spinner.failed(result.error)
            return result
        batch.clear()
        spinner.increment(amount=len(batch))
    spinner.successful(f"Successfully added parsed {table.__tablename__} data to database")
    return Result[None].Ok()


def _perform_batch_insert(session: Session, batch: list[UnicodeModel]) -> Result[None]:
    try:
        session.add_all(batch)
        session.commit()
        return Result[None].Ok()
    except StatementError as ex:
        return Result[None].Fail(f"Error! {repr(ex)}")
