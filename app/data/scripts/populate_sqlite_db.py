import json

from sqlmodel import Session

import app.db.engine as db
from app.core.config import BLOCKS_JSON, CHARACTERS_JSON, PLANES_JSON
from app.core.result import Result
from app.data.constants import NULL_BLOCK, NULL_PLANE
from app.data.scripts.util import finish_task, start_task, update_progress
from app.schemas.enums import (
    BidirectionalBracketType,
    BidirectionalClass,
    DecompositionType,
    EastAsianWidthType,
    GeneralCategory,
    HangulSyllableType,
    JoiningClass,
    LineBreakType,
    NumericType,
    ScriptCode,
    VerticalOrientationType,
)


def populate_sqlite_database():
    db.create_db_and_tables()
    all_planes, all_blocks = parse_unicode_planes_and_blocks_from_json()
    all_chars = parse_unicode_characters_from_json()
    all_blocks = assign_unicode_plane_to_each_block(all_planes, all_blocks)
    all_chars = assign_unicode_block_and_plane_to_each_character(all_planes, all_blocks, all_chars)

    with Session(db.engine) as session:
        add_unicode_data_to_database(all_planes, all_blocks, all_chars, session)
        commit_database_session(session)
    return Result.Ok()


def parse_unicode_planes_and_blocks_from_json():
    spinner = start_task("Parsing unicode plane and block data from JSON...")
    all_planes = parse_unicode_planes_from_json()
    all_blocks = parse_unicode_blocks_from_json()
    finish_task(spinner, True, "Successfully parsed plane and block data!")
    return (all_planes, all_blocks)


def parse_unicode_planes_from_json():
    plane_dicts = json.loads(PLANES_JSON.read_text())
    return [db.UnicodePlane(**plane) for plane in plane_dicts]


def parse_unicode_blocks_from_json():
    block_dicts = json.loads(BLOCKS_JSON.read_text())
    return [db.UnicodeBlock(**block) for block in block_dicts]


def parse_unicode_characters_from_json():
    spinner = start_task("Parsing unicode character data from JSON...")
    char_dicts = json.loads(CHARACTERS_JSON.read_text())
    all_char_dicts = [update_char_dict_enum_values(char) for char in char_dicts]
    all_named_chars = [db.UnicodeCharacter(**char_dict) for char_dict in all_char_dicts if not char_dict["no_name"]]
    all_no_name_chars = [db.UnicodeCharacterNoName(**char_dict) for char_dict in all_char_dicts if char_dict["no_name"]]
    finish_task(spinner, True, "Successfully parsed character data!")
    return all_named_chars + all_no_name_chars


def update_char_dict_enum_values(char_dict):
    char_dict["general_category"] = GeneralCategory.from_code(char_dict["general_category"])
    char_dict["bidirectional_class"] = BidirectionalClass.from_code(char_dict["bidirectional_class"])
    char_dict["paired_bracket_type"] = BidirectionalBracketType.from_code(char_dict["paired_bracket_type"])
    char_dict["decomposition_type"] = DecompositionType.from_code(char_dict["decomposition_type"])
    char_dict["numeric_type"] = NumericType.from_code(char_dict["numeric_type"])
    char_dict["joining_class"] = JoiningClass.from_code(char_dict["joining_class"])
    char_dict["line_break"] = LineBreakType.from_code(char_dict["line_break"])
    char_dict["east_asian_width"] = EastAsianWidthType.from_code(char_dict["east_asian_width"])
    char_dict["script"] = ScriptCode.from_code(char_dict["script"])
    char_dict["hangul_syllable_type"] = HangulSyllableType.from_code(char_dict["hangul_syllable_type"])
    char_dict["vertical_orientation"] = VerticalOrientationType.from_code(char_dict["vertical_orientation"])
    return char_dict


def assign_unicode_plane_to_each_block(all_planes, all_blocks):
    spinner = start_task("Assigning unicode plane to each block...")
    update_progress(spinner, "Assigning unicode planes to each block...", 0, len(all_blocks))
    for i, block in enumerate(all_blocks, start=1):
        found = [
            plane for plane in all_planes if plane.start_block_id <= block.id and block.id <= plane.finish_block_id
        ]
        block.plane = found[0] if found else db.UnicodePlane(**NULL_PLANE)
        update_progress(spinner, "Assigning unicode planes to each block...", i, len(all_blocks))
    finish_task(spinner, True, "Successfully assigned a unicode plane to all blocks!")
    return all_blocks


def assign_unicode_block_and_plane_to_each_character(all_planes, all_blocks, all_chars):
    spinner = start_task("Assigning unicode block and plane to each character...")
    for i, char in enumerate(all_chars, start=1):
        found_block = [
            block
            for block in all_blocks
            if block.start_dec <= char.codepoint_dec and char.codepoint_dec <= block.finish_dec
        ]
        block = found_block[0] if found_block else db.UnicodeBlock(**NULL_BLOCK)
        found_plane = [
            plane for plane in all_planes if plane.start_block_id <= block.id and block.id <= plane.finish_block_id
        ]
        plane = found_plane[0] if found_plane else db.UnicodePlane(**NULL_PLANE)
        char.block = block
        char.plane = plane
        update_progress(spinner, "Assigning unicode block and plane to each character...", i, len(all_chars))
    finish_task(spinner, True, "Successfully assigned a unicode block and plane to all characters!")
    return all_chars


def add_unicode_data_to_database(all_planes, all_blocks, all_chars, session):
    spinner = start_task("Adding unicode data to database session...")
    for plane in all_planes:
        session.add(plane)
    session.commit()
    for block in all_blocks:
        session.add(block)
    session.commit()
    for i, char in enumerate(all_chars, start=1):
        session.add(char)
        update_progress(spinner, "Adding unicode characters to database session...", i, len(all_chars))
    finish_task(spinner, True, "Successfully added all characters to database session!!")


def commit_database_session(session):
    spinner = start_task("Committing all data from this session to the database...")
    session.commit()
    finish_task(spinner, True, "Successfully committed all data!")


if __name__ == "__main__":
    populate_sqlite_database()
