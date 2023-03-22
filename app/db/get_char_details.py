import operator
from functools import reduce
from typing import Any

from sqlalchemy import column, select
from sqlalchemy.engine import Engine

import app.db.engine as db
from app.data.cache import cached_data
from app.db.character_props import CHARACTER_PROPERTY_GROUPS
from app.schemas.enums import CharPropertyGroup


def get_character_properties(
    engine: Engine, codepoint: int, show_props: list[CharPropertyGroup] | None
) -> dict[str, Any]:
    prop_groups = get_prop_groups(show_props)
    char_prop_dicts = [get_character_prop_group(engine, codepoint, group) for group in prop_groups]
    return reduce(operator.ior, char_prop_dicts, {})


def get_prop_groups(show_props: list[CharPropertyGroup] | None) -> list[CharPropertyGroup]:
    if show_props:
        if CharPropertyGroup.All in show_props:
            return [group for group in CharPropertyGroup if group != CharPropertyGroup.All]
        if CharPropertyGroup.Minimum not in show_props:
            return [CharPropertyGroup.Minimum] + show_props
    return [CharPropertyGroup.Minimum]


def get_character_prop_group(engine: Engine, codepoint: int, prop_group: CharPropertyGroup) -> dict[str, Any]:
    char_props = {"codepoint_dec": codepoint}
    prop_columns = [column(prop["name_in"]) for prop in CHARACTER_PROPERTY_GROUPS[prop_group] if prop["db_column"]]
    if prop_columns:
        char_table = (
            db.UnicodeCharacter if cached_data.character_is_uniquely_named(codepoint) else db.UnicodeCharacterNoName
        )
        query = select(prop_columns).select_from(char_table).where(column("codepoint_dec") == codepoint)
        with engine.connect() as con:
            for row in con.execute(query):
                char_props.update(dict(row._mapping))
    return get_remaining_prop_values(char_props, prop_group)


def get_remaining_prop_values(char_props: dict[str, Any], prop_group: CharPropertyGroup) -> dict[str, Any]:
    return {
        prop_map["name_out"]: prop_map["response_value"](char_props)
        for prop_map in CHARACTER_PROPERTY_GROUPS[prop_group]
    }
