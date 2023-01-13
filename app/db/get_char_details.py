# flake8: noqa
import operator
from functools import lru_cache, reduce
from typing import Any, Type

from sqlalchemy import column, select, text
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text
from sqlmodel import Session

import app.db.engine as db
from app.core.result import Result
from app.core.util import get_codepoint_string
from app.data.constants import NON_CHARACTER_CODEPOINTS, PRIVATE_USE_BLOCK_IDS, SURROGATE_BLOCK_IDS
from app.db.constants import CJK_COMPATIBILITY_BLOCKS, CJK_UNIFIED_BLOCKS, TANGUT_BLOCKS
from app.schemas.enums import CharPropertyGroup, NamelessCharacterType
from app.schemas.prop_groups import get_all_db_columns_in_group, update_character_properties


@lru_cache
def all_codepoints_for_uniquely_named_chars(session: Session) -> set[int]:
    return set(char.codepoint_dec for char in session.query(db.UnicodeCharacter).all())


@lru_cache
def all_codepoints_for_generically_named_chars(session: Session) -> set[int]:
    return set(char.codepoint_dec for char in session.query(db.UnicodeCharacterNoName).all())


@lru_cache
def unique_character_name_map(engine: Engine):
    name_map = {}
    with engine.connect() as con:
        query = select([column("codepoint_dec"), column("name")]).select_from(db.UnicodeCharacter)
        name_map = {row["codepoint_dec"]: row["name"] for row in con.execute(query)}
    return name_map


def codepoint_is_in_unicode_range(codepoint: int) -> bool:
    return codepoint >= 0 and codepoint <= 1114111


def codepoint_is_a_generically_named_character(session: Session, codepoint: int) -> bool:
    return codepoint in all_codepoints_for_generically_named_chars(session)


def codepoint_is_a_nameless_character(session: Session, codepoint: int) -> bool:
    all_named_codepoints = set(
        list(all_codepoints_for_uniquely_named_chars(session))
        + list(all_codepoints_for_generically_named_chars(session))
    )
    return codepoint not in all_named_codepoints


def get_character_details(
    session: Session,
    engine: Engine,
    codepoint: int,
    show_props: list[CharPropertyGroup] | None = None,
    score: float | None = None,
) -> dict[str, Any | bool | int | str | None]:
    show_props = check_prop_group_selections(show_props)
    char_prop_dicts = [get_character_properties(session, engine, codepoint, group) for group in show_props]
    return reduce(operator.ior, char_prop_dicts, {"score": float(f"{score:.1f}")} if score else {})


def check_prop_group_selections(prop_groups: list[CharPropertyGroup] | None = None) -> list[CharPropertyGroup]:
    if not prop_groups:
        prop_groups = [CharPropertyGroup.Minimum]
    if CharPropertyGroup.Minimum not in prop_groups:
        prop_groups = [CharPropertyGroup.Minimum] + prop_groups
    if prop_groups and CharPropertyGroup.All in prop_groups:
        prop_groups = [group for group in CharPropertyGroup if group != CharPropertyGroup.All]
    return prop_groups


def get_character_properties(session: Session, engine: Engine, codepoint: int, prop_group: CharPropertyGroup):
    char: dict[str, Any | bool | int | str | None] = {"codepoint_dec": codepoint}
    with engine.connect() as con:
        col_names = get_all_db_columns_in_group(prop_group)
        if col_names:
            if "name" in col_names:
                result = get_character_name(engine, session, codepoint)
                if result.success:
                    char["name"] = result.value
            query = (
                select(column(col_name) for col_name in col_names)
                .select_from(get_character_table_name_for_codepoint(session, codepoint))
                .where(column("codepoint_dec") == codepoint)
            )
            for row in con.execute(query):
                char = dict(row._mapping) | char
    return update_character_properties(char, prop_group)


def get_character_table_name_for_codepoint(
    session: Session, codepoint: int
) -> (Type[db.UnicodeCharacterNoName] | Type[db.UnicodeCharacter]):
    no_name = codepoint in all_codepoints_for_generically_named_chars(session)
    return db.UnicodeCharacterNoName if no_name else db.UnicodeCharacter


def get_character_name(engine: Engine, session: Session, codepoint: int) -> Result[str]:
    if not codepoint_is_in_unicode_range(codepoint):
        return Result.Fail(
            f"Codepoint {get_codepoint_string(codepoint)} is not within the range of unicode characters (U+0000 to U+10FFFF)."
        )
    block = get_unicode_block_containing_codepoint(session, codepoint)
    char_name = (
        get_codepoint_label_for_nameless_character(codepoint, block)
        if codepoint_is_a_nameless_character(session, codepoint)
        else get_generic_character_name(codepoint, block)
        if codepoint_is_a_generically_named_character(session, codepoint)
        else get_unique_character_name(engine, codepoint)
    )
    return Result.Ok(char_name)


def get_unicode_block_containing_codepoint(session: Session, codepoint: int) -> db.UnicodeBlock:
    return (
        session.query(db.UnicodeBlock)
        .filter(db.UnicodeBlock.start_dec <= codepoint)
        .filter(db.UnicodeBlock.finish_dec >= codepoint)
        .one()
    )


def get_codepoint_label_for_nameless_character(codepoint: int, block: db.UnicodeBlock) -> str:
    charType = (
        NamelessCharacterType.NONCHARACTER
        if f"{codepoint:X}" in NON_CHARACTER_CODEPOINTS
        else NamelessCharacterType.SURROGATE
        if block.id in SURROGATE_BLOCK_IDS
        else NamelessCharacterType.PRIVATE_USE
        if block.id in PRIVATE_USE_BLOCK_IDS
        else NamelessCharacterType.RESERVED
    )
    return f"{charType} ({get_codepoint_string(codepoint)})"


def get_generic_character_name(codepoint: int, block: db.UnicodeBlock) -> str:
    return (
        f"CJK UNIFIED IDEOGRAPH-{codepoint:04X}"
        if block.id in CJK_UNIFIED_BLOCKS
        else f"CJK COMPATIBILITY IDEOGRAPH-{codepoint:04X}"
        if block.id in CJK_COMPATIBILITY_BLOCKS
        else f"TANGUT IDEOGRAPH-{codepoint:04X}"
        if block.id in TANGUT_BLOCKS
        else f"{block} ({get_codepoint_string(codepoint)})"
    )


def get_unique_character_name(engine: Engine, codepoint: int) -> str:
    name_map = unique_character_name_map(engine)
    return name_map.get(
        codepoint,
        f"Error! Failed to retrieve UnicodeCharacter from db for codepoint: ({get_codepoint_string(codepoint)})",
    )
