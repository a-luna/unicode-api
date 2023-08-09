from pathlib import Path

from halo import Halo
from sqlalchemy.engine import Engine
from sqlalchemy.exc import StatementError
from sqlalchemy.sql import text
from sqlmodel import Session, SQLModel, create_engine

import app.db.models as db
from app.core.config import UnicodeApiSettings
from app.core.result import Result
from app.data.util import finish_task, start_task, update_progress
from app.db.character_props import PROPERTY_GROUPS
from app.schemas.enums import CharPropertyGroup

BATCH_SIZE = 10000


def populate_sqlite_database(config: UnicodeApiSettings) -> Result:
    table_csv_file_map: dict[
        type[db.UnicodePlane] | type[db.UnicodeBlock] | type[db.UnicodeCharacter] | type[db.UnicodeCharacterUnihan],
        Path,
    ] = {
        db.UnicodePlane: config.PLANES_CSV,
        db.UnicodeBlock: config.BLOCKS_CSV,
        db.UnicodeCharacter: config.NAMED_CHARS_CSV,
        db.UnicodeCharacterUnihan: config.UNIHAN_CHARS_CSV,
    }
    engine = create_engine(str(config.DB_URL), echo=False, connect_args={"check_same_thread": False})
    with Session(engine) as session:
        create_db_and_tables(config, engine)
        for table, csv_file in table_csv_file_map.items():
            spinner = start_task(f"Adding parsed {table.__tablename__} data to database...")
            import_data_from_csv_file(spinner, session, csv_file, table)
            finish_task(spinner, True, f"Successfully added parsed {table.__tablename__} data to database")
    engine.dispose()
    return Result.Ok()


def create_db_and_tables(config: UnicodeApiSettings, engine: Engine) -> None:
    if config.DB_FILE.exists():
        config.DB_FILE.unlink()

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
    spinner: Halo,
    session: Session,
    csv_file: Path,
    table: type[db.UnicodePlane] | type[db.UnicodeBlock] | type[db.UnicodeCharacter] | type[db.UnicodeCharacterUnihan],
) -> None:
    csv_rows = csv_file.read_text().split("\n")
    column_names = [col.strip() for col in csv_rows.pop(0).split(",")]
    batch, total_rows, row_count = [], len(csv_rows), 0
    first_row_skipped = False
    with Path(csv_file).open() as csv:
        while True:
            csv_row = csv.readline()
            if not csv_row:
                break
            if not first_row_skipped:
                first_row_skipped = True
                continue
            csv_values = [val.strip().replace(";", ",") for val in csv_row.split(",")]
            batch.append(table(**dict(zip(column_names, csv_values))))  # type: ignore  # noqa: PGH003
            if len(batch) < BATCH_SIZE:
                continue
            row_count += len(batch)
            perform_batch_insert(session, batch)
            update_progress(spinner, f"Adding parsed {table.__tablename__} data to database", row_count, total_rows)
        if batch:
            row_count += len(batch)
            perform_batch_insert(session, batch)
            update_progress(spinner, f"Adding parsed {table.__tablename__} data to database", row_count, total_rows)


def perform_batch_insert(
    session: Session,
    batch: list[
        type[db.UnicodePlane] | type[db.UnicodeBlock] | type[db.UnicodeCharacter] | type[db.UnicodeCharacterUnihan]
    ],
):
    try:
        session.add_all(batch)
        session.commit()
        batch.clear()
    except StatementError as ex:
        print(f"Error! {repr(ex)}")
