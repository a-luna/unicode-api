from typing import Any, Type

from sqlalchemy import column, select
from sqlalchemy.engine import Engine

import app.db.engine as db
from app.db.constants import CHARACTER_PROPERTY_GROUPS
from app.schemas.enums import CharPropertyGroup


def get_character_properties(
    engine: Engine,
    codepoint: int,
    prop_group: CharPropertyGroup,
    char_name: str,
    char_table_name: Type[db.UnicodeCharacterNoName] | Type[db.UnicodeCharacter],
):
    char_props: dict[str, bool | int | str] = {"codepoint_dec": codepoint, "name": char_name}
    with engine.connect() as con:
        col_names = db.get_all_db_columns_in_group(prop_group)
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
