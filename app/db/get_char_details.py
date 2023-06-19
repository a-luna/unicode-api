import operator
from functools import reduce
from typing import Any

from sqlalchemy import column, select
from sqlalchemy.engine import Engine

import app.db.models as db
from app.data.cache import cached_data
from app.db.character_props import PROPERTY_GROUPS
from app.schemas.enums import CharPropertyGroup


def get_character_properties(
    engine: Engine, codepoint: int, show_props: list[CharPropertyGroup] | None
) -> dict[str, Any]:
    prop_groups = get_prop_groups(codepoint, show_props)
    char_prop_dicts = [get_character_prop_group(engine, codepoint, group) for group in prop_groups]
    return reduce(operator.ior, char_prop_dicts, {})


def get_prop_groups(codepoint: int, show_props: list[CharPropertyGroup] | None) -> list[CharPropertyGroup]:
    unihan = cached_data.character_is_unihan(codepoint)
    show_props = show_props or []
    if not unihan and any("CJK" in prop_group.name for prop_group in show_props):
        show_props = [prop_group for prop_group in show_props if "CJK" not in prop_group.name]
    if not show_props:
        return [CharPropertyGroup.MINIMUM] if not unihan else [CharPropertyGroup.CJK_MINIMUM]
    if CharPropertyGroup.ALL in show_props:
        return (
            CharPropertyGroup.get_all_named_character_prop_groups()
            if not unihan
            else CharPropertyGroup.get_all_unihan_character_prop_groups()
        )
    if CharPropertyGroup.MINIMUM in show_props or CharPropertyGroup.CJK_MINIMUM in show_props:
        show_props = [
            prop_group
            for prop_group in show_props
            if prop_group not in [CharPropertyGroup.MINIMUM, CharPropertyGroup.CJK_MINIMUM]
        ]
        return show_props + [CharPropertyGroup.CJK_MINIMUM if unihan else CharPropertyGroup.MINIMUM]
    if CharPropertyGroup.BASIC in show_props or CharPropertyGroup.CJK_BASIC in show_props:
        show_props = [
            prop_group
            for prop_group in show_props
            if prop_group not in [CharPropertyGroup.BASIC, CharPropertyGroup.CJK_BASIC]
        ]
        return show_props + [CharPropertyGroup.CJK_BASIC if unihan else CharPropertyGroup.BASIC]
    return show_props


def get_character_prop_group(engine: Engine, codepoint: int, prop_group: CharPropertyGroup) -> dict[str, Any]:
    columns = [column(prop_map["name_in"]) for prop_map in PROPERTY_GROUPS[prop_group] if prop_map["db_column"]]
    char_props = get_prop_values_from_database(engine, codepoint, columns) if columns else {"codepoint_dec": codepoint}
    return {prop_map["name_out"]: prop_map["response_value"](char_props) for prop_map in PROPERTY_GROUPS[prop_group]}


def get_prop_values_from_database(engine: Engine, codepoint: int, columns):
    char_props = {"codepoint_dec": codepoint}
    table = db.UnicodeCharacter if cached_data.character_is_uniquely_named(codepoint) else db.UnicodeCharacterUnihan
    query = select(columns).select_from(table).where(column("codepoint_dec") == codepoint)
    with engine.connect() as con:
        for row in con.execute(query):
            char_props.update(dict(row._mapping))
    return char_props
