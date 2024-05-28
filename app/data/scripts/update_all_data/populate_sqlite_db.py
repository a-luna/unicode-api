from pathlib import Path
from types import NoneType

from pydantic import ValidationError
from sqlalchemy.engine import Engine
from sqlalchemy.exc import StatementError
from sqlalchemy.sql import text
from sqlmodel import Session, SQLModel, create_engine

import app.db.models as db
from app.config.api_settings import UnicodeApiSettings
from app.core.result import Result
from app.data.scripts.script_types import UnicodeModel
from app.data.util.spinners import Spinner
from app.db.character_props import PROPERTY_GROUPS
from app.schemas.enums import (
    BidirectionalBracketType,
    BidirectionalClass,
    CharPropertyGroup,
    CombiningClassCategory,
    DecompositionType,
    EastAsianWidthType,
    HangulSyllableType,
    JoiningType,
    LineBreakType,
    NumericType,
    ScriptCode,
    TriadicLogic,
    VerticalOrientationType,
)

BATCH_SIZE = 10000


def populate_sqlite_database(settings: UnicodeApiSettings) -> Result[None]:
    table_csv_file_map: dict[UnicodeModel, Path] = {
        db.UnicodePlane: settings.PLANES_CSV,
        db.UnicodeBlock: settings.BLOCKS_CSV,
        db.UnicodeCharacter: settings.NAMED_CHARS_CSV,
        db.UnicodeCharacterUnihan: settings.UNIHAN_CHARS_CSV,
    }
    engine = create_engine(str(settings.DB_URL), echo=False, connect_args={"check_same_thread": False})
    result = Result.Ok()
    with Session(engine) as session:
        create_db_and_tables(settings, engine)
        for table, csv_file in table_csv_file_map.items():
            result = import_data_from_csv_file(session, csv_file, table)
            if result.failure:
                break
    engine.dispose()
    return Result.Ok()


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
        for prop_group in CharPropertyGroup
        if prop_group not in [CharPropertyGroup.ALL, CharPropertyGroup.NONE]
    ]
    return [sql for sql in sql_statements if sql]


def generate_raw_sql_for_covering_index(prop_group: CharPropertyGroup) -> str:
    columns = [prop["name_in"] for prop in PROPERTY_GROUPS[prop_group] if prop["db_column"]]
    table = "character" if "CJK" not in prop_group.name else "character_unihan"
    return f'CREATE INDEX ix_character_{prop_group.index_name} ON {table} ({", ".join(columns)})' if columns else ""


def import_data_from_csv_file(
    session: Session,
    csv_file: Path,
    table: UnicodeModel,
) -> Result[None]:
    column_names, total_rows = get_column_names_and_total_rows(csv_file)
    batch, first_row_skipped = [], False
    spinner = Spinner()
    spinner.start(f"Adding parsed {table.__tablename__} data to database...", total=total_rows)
    with Path(csv_file).open() as csv:
        while True:
            csv_row = csv.readline()
            if not csv_row:
                break
            if not first_row_skipped:
                first_row_skipped = True
                continue
            csv_values = [val.strip().replace(";", ",") for val in csv_row.split(",")]
            result = create_object_dict_with_expected_types(column_names, csv_values, table)
            if result.failure:
                spinner.failed(result.error)
                return result
            object_dict = result.value
            try:
                batch.append(table.model_validate(object_dict))
            except ValidationError as ex:
                spinner.failed(f"Error! {repr(ex)}")
                return Result.Fail(f"Error! {repr(ex)}")
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


def get_column_names_and_total_rows(csv_file: Path) -> tuple[list[str], int]:
    csv_rows = csv_file.read_text().split("\n")
    column_names = [col.strip() for col in csv_rows.pop(0).split(",")]
    return (column_names, len(csv_rows))


def create_object_dict_with_expected_types(
    column_names: list[str], csv_values: list[str], table: UnicodeModel
) -> Result[dict]:
    enum_types = (
        BidirectionalBracketType,
        BidirectionalClass,
        CombiningClassCategory,
        DecompositionType,
        EastAsianWidthType,
        HangulSyllableType,
        JoiningType,
        LineBreakType,
        NumericType,
        ScriptCode,
        TriadicLogic,
        VerticalOrientationType,
    )
    object_dict = {}
    for name, value in dict(zip(column_names, csv_values)).items():
        if name not in table.model_fields:
            return Result.Fail(f"Error! Database model {table.name} has no property named {name}")
        prop_type = table.model_fields[name].annotation
        if prop_type in enum_types or prop_type in [int, int | NoneType]:
            try:
                object_dict[name] = int(value)
            except ValueError:
                object_dict[name] = None
        elif prop_type in [bool, bool | NoneType]:
            if "True" in value:
                object_dict[name] = True
            if "False" in value:
                object_dict[name] = False
        else:
            object_dict[name] = value
    return Result.Ok(object_dict)


def perform_batch_insert(session: Session, batch: list[UnicodeModel]) -> Result[None]:
    try:
        session.add_all(batch)
        session.commit()
        return Result.Ok()
    except StatementError as ex:
        return Result.Fail(f"Error! {repr(ex)}")
