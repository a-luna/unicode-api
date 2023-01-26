import operator
from functools import reduce
from typing import Any, Type

from sqlalchemy import column, select
from sqlalchemy.engine import Engine

import app.db.engine as db
from app.data.cache import cached_data
from app.db.character_props import CHARACTER_PROPERTY_GROUPS
from app.schemas.enums import CharPropertyGroup


def get_character_properties(engine: Engine, codepoint: int, show_props: list[CharPropertyGroup] | None = None):
    show_props = check_prop_group_selections(show_props)
    char_name = cached_data.get_character_name(codepoint)
    char_table_name = get_character_table_name_for_codepoint(codepoint)
    char_prop_dicts = [
        get_character_prop_group(engine, codepoint, group, char_name, char_table_name) for group in show_props
    ]
    return reduce(operator.ior, char_prop_dicts, {})


def check_prop_group_selections(prop_groups: list[CharPropertyGroup] | None = None) -> list[CharPropertyGroup]:
    if not prop_groups:
        prop_groups = [CharPropertyGroup.Minimum]
    if CharPropertyGroup.Minimum not in prop_groups:
        prop_groups = [CharPropertyGroup.Minimum] + prop_groups
    if prop_groups and CharPropertyGroup.All in prop_groups:
        prop_groups = [group for group in CharPropertyGroup if group != CharPropertyGroup.All]
    return prop_groups


def get_character_table_name_for_codepoint(
    codepoint: int,
) -> (Type[db.UnicodeCharacterNoName] | Type[db.UnicodeCharacter]):
    return db.UnicodeCharacter if cached_data.character_is_uniquely_named(codepoint) else db.UnicodeCharacterNoName


def get_character_prop_group(
    engine: Engine,
    codepoint: int,
    prop_group: CharPropertyGroup,
    char_name: str,
    char_table_name: Type[db.UnicodeCharacterNoName] | Type[db.UnicodeCharacter],
):
    char_props: dict[str, bool | int | str] = {"codepoint_dec": codepoint, "name": char_name}
    with engine.connect() as con:
        col_names = [prop["name_in"] for prop in CHARACTER_PROPERTY_GROUPS[prop_group] if prop["db_column"]]
        if col_names:
            query = (
                select(column(col_name) for col_name in col_names)
                .select_from(char_table_name)
                .where(column("codepoint_dec") == codepoint)
            )
            for row in con.execute(query):
                char_props.update(dict(row._mapping))
    return update_character_properties(char_props, prop_group)


def update_character_properties(char_dict: dict[str, Any | bool | int | str | None], prop_group: CharPropertyGroup):
    updated_dict = {}
    all_prop_names = [prop_map["name_in"] for prop_map in CHARACTER_PROPERTY_GROUPS[prop_group]]
    for prop_name in all_prop_names:
        prop_map = [map for map in CHARACTER_PROPERTY_GROUPS[prop_group] if map["name_in"] == prop_name][0]
        updated_dict[prop_map["name_out"]] = (
            prop_map["response_value"](char_dict)
            if prop_map["responsify"]
            else char_dict[prop_name]
            if prop_name in char_dict
            else None
        )
    return updated_dict
