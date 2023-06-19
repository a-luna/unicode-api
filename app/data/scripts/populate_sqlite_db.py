import json

from sqlalchemy.sql import text
from sqlmodel import Session, SQLModel

import app.db.models as db
from app.core.config import BLOCKS_JSON, CHARACTERS_JSON, DB_FILE, PLANES_JSON
from app.core.result import Result
from app.data.constants import NULL_BLOCK, NULL_PLANE
from app.data.scripts.util import finish_task, start_task, update_progress
from app.db.character_props import CHARACTER_PROPERTY_GROUPS
from app.db.engine import engine
from app.schemas.enums import (
    BidirectionalBracketType,
    BidirectionalClass,
    CharPropertyGroup,
    DecompositionType,
    EastAsianWidthType,
    GeneralCategory,
    HangulSyllableType,
    JoiningType,
    LineBreakType,
    NumericType,
    ScriptCode,
    TriadicLogic,
    VerticalOrientationType,
)


def populate_sqlite_database():
    create_db_and_tables()
    all_planes, all_blocks = parse_unicode_planes_and_blocks_from_json()
    all_chars = parse_unicode_characters_from_json()
    all_blocks = assign_unicode_plane_to_each_block(all_planes, all_blocks)
    all_chars = assign_unicode_block_and_plane_to_each_character(all_planes, all_blocks, all_chars)

    with Session(engine) as session:
        add_unicode_data_to_database(all_planes, all_blocks, all_chars, session)
        commit_database_session(session)
    return Result.Ok()


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
        if prop_group not in [CharPropertyGroup.ALL, CharPropertyGroup.NONE]
    ]
    return [sql for sql in sql_statements if sql]


def generate_raw_sql_for_covering_index(prop_group: CharPropertyGroup) -> str:
    columns = [prop["name_in"] for prop in CHARACTER_PROPERTY_GROUPS[prop_group] if prop["db_column"]]
    table = "character" if "CJK" not in prop_group.name else "character_unihan"
    return f'CREATE INDEX ix_character_{prop_group.index_name} ON {table} ({", ".join(columns)})' if columns else ""


def parse_unicode_planes_and_blocks_from_json():
    spinner = start_task("Parsing Unicode plane and block data from JSON...")
    all_planes = [db.UnicodePlane(**plane) for plane in json.loads(PLANES_JSON.read_text())]
    all_blocks = [db.UnicodeBlock(**block) for block in json.loads(BLOCKS_JSON.read_text())]
    finish_task(spinner, True, "Successfully parsed plane and block data!")
    return (all_planes, all_blocks)


def parse_unicode_characters_from_json():
    spinner = start_task("Parsing Unicode character data from JSON...")
    all_char_dicts = [update_char_dict_enum_values(char) for char in json.loads(CHARACTERS_JSON.read_text())]
    all_named_chars = [db.UnicodeCharacter(**char_dict) for char_dict in all_char_dicts if not char_dict["unihan"]]
    all_unihan_chars = [db.UnicodeCharacterUnihan(**char_dict) for char_dict in all_char_dicts if char_dict["unihan"]]
    finish_task(spinner, True, "Successfully parsed character data!")
    return all_named_chars + all_unihan_chars


def update_char_dict_enum_values(char_dict):
    char_dict["general_category"] = GeneralCategory.from_code(char_dict["general_category"])
    char_dict["bidirectional_class"] = BidirectionalClass.from_code(char_dict["bidirectional_class"])
    char_dict["paired_bracket_type"] = BidirectionalBracketType.from_code(char_dict["paired_bracket_type"])
    char_dict["decomposition_type"] = DecompositionType.from_code(char_dict["decomposition_type"])
    char_dict["NFC_QC"] = TriadicLogic.from_code(char_dict["NFC_QC"])
    char_dict["NFD_QC"] = TriadicLogic.from_code(char_dict["NFD_QC"])
    char_dict["NFKC_QC"] = TriadicLogic.from_code(char_dict["NFKC_QC"])
    char_dict["NFKD_QC"] = TriadicLogic.from_code(char_dict["NFKD_QC"])
    char_dict["numeric_type"] = NumericType.from_code(char_dict["numeric_type"])
    char_dict["joining_type"] = JoiningType.from_code(char_dict["joining_type"])
    char_dict["line_break"] = LineBreakType.from_code(char_dict["line_break"])
    char_dict["east_asian_width"] = EastAsianWidthType.from_code(char_dict["east_asian_width"])
    char_dict["script"] = ScriptCode.from_code(char_dict["script"])
    char_dict["hangul_syllable_type"] = HangulSyllableType.from_code(char_dict["hangul_syllable_type"])
    char_dict["vertical_orientation"] = VerticalOrientationType.from_code(char_dict["vertical_orientation"])
    return char_dict


def assign_unicode_plane_to_each_block(all_planes, all_blocks):
    spinner = start_task("Assigning Unicode plane to each block...")
    update_progress(spinner, "Assigning Unicode planes to each block...", 0, len(all_blocks))
    for i, block in enumerate(all_blocks, start=1):
        block.plane = get_unicode_plane_containing_block(all_planes, block)
        update_progress(spinner, "Assigning Unicode planes to each block...", i, len(all_blocks))
    finish_task(spinner, True, "Successfully assigned a Unicode plane to all blocks!")
    return all_blocks


def get_unicode_plane_containing_block(all_planes, block):
    found = [plane for plane in all_planes if plane.start_block_id <= block.id and block.id <= plane.finish_block_id]
    return found[0] if found else db.UnicodePlane(**NULL_PLANE)


def assign_unicode_block_and_plane_to_each_character(all_planes, all_blocks, all_chars):
    spinner = start_task("Assigning Unicode block and plane to each character...")
    for i, char in enumerate(all_chars, start=1):
        char.block = get_unicode_block_containing_codepoint(all_blocks, char.codepoint_dec)
        char.plane = get_unicode_plane_containing_block(all_planes, char.block)
        update_progress(spinner, "Assigning Unicode block and plane to each character...", i, len(all_chars))
    finish_task(spinner, True, "Successfully assigned a Unicode block and plane to all characters!")
    return all_chars


def get_unicode_block_containing_codepoint(all_blocks, codepoint):
    found = [block for block in all_blocks if block.start_dec <= codepoint and codepoint <= block.finish_dec]
    return found[0] if found else db.UnicodeBlock(**NULL_BLOCK)


def add_unicode_data_to_database(all_planes, all_blocks, all_chars, session):
    spinner = start_task("Adding Unicode data to database session...")
    for plane in all_planes:
        session.add(plane)
    session.commit()
    for block in all_blocks:
        session.add(block)
    session.commit()
    for i, char in enumerate(all_chars, start=1):
        session.add(char)
        update_progress(spinner, "Adding Unicode characters to database session...", i, len(all_chars))
    finish_task(spinner, True, "Successfully added all characters to database session!!")


def commit_database_session(session):
    spinner = start_task("Committing all data from this session to the database...")
    session.commit()
    finish_task(spinner, True, "Successfully committed all data!")
