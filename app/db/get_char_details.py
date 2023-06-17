import operator
from functools import reduce
from typing import Any

from sqlalchemy import column, select
from sqlalchemy.engine import Engine

import app.db.models as db
import app.schemas.enums as enum
from app.data.cache import cached_data
from app.db.character_props import CHARACTER_PROPERTY_GROUPS


def get_character_properties(
    engine: Engine, codepoint: int, show_props: list[enum.CharPropertyGroup] | None
) -> dict[str, Any]:
    prop_groups = get_prop_groups(show_props)
    char_prop_dicts = [get_character_prop_group(engine, codepoint, group) for group in prop_groups]
    return reduce(operator.ior, char_prop_dicts, {})


def get_prop_groups(show_props: list[enum.CharPropertyGroup] | None) -> list[enum.CharPropertyGroup]:
    if not show_props:
        return [enum.CharPropertyGroup.Minimum]
    if enum.CharPropertyGroup.All in show_props:
        return [
            group
            for group in enum.CharPropertyGroup
            if group not in [enum.CharPropertyGroup.All, enum.CharPropertyGroup.NONE]
        ]
    if enum.CharPropertyGroup.Minimum not in show_props:
        return [enum.CharPropertyGroup.Minimum] + show_props
    return show_props


def get_character_prop_group(engine: Engine, codepoint: int, prop_group: enum.CharPropertyGroup) -> dict[str, Any]:
    columns = [
        column(prop_map["name_in"]) for prop_map in CHARACTER_PROPERTY_GROUPS[prop_group] if prop_map["db_column"]
    ]
    char_props = get_prop_values_from_database(engine, codepoint, columns) if columns else {"codepoint_dec": codepoint}
    return {
        prop_map["name_out"]: prop_map["response_value"](char_props)
        for prop_map in CHARACTER_PROPERTY_GROUPS[prop_group]
    }


def get_prop_values_from_database(engine: Engine, codepoint: int, columns):
    char_props = {"codepoint_dec": codepoint}
    table = db.UnicodeCharacter if cached_data.character_is_uniquely_named(codepoint) else db.UnicodeCharacterNoName
    query = select(columns).select_from(table).where(column("codepoint_dec") == codepoint)
    with engine.connect() as con:
        for row in con.execute(query):
            char_props.update(dict(row._mapping))
    return char_props
