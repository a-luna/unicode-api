from typing import Type

from sqlalchemy import column, select
from sqlalchemy.engine import Engine

import app.db.engine as db
from app.schemas.enums import CharPropertyGroup
from app.schemas.prop_groups import get_all_db_columns_in_group, update_character_properties


def get_character_properties(
    engine: Engine,
    codepoint: int,
    prop_group: CharPropertyGroup,
    char_name: str,
    char_table_name: Type[db.UnicodeCharacterNoName] | Type[db.UnicodeCharacter],
):
    char: dict[str, bool | int | str] = {"codepoint_dec": codepoint, "name": char_name}
    with engine.connect() as con:
        col_names = get_all_db_columns_in_group(prop_group)
        if col_names:
            query = (
                select(column(col_name) for col_name in col_names)
                .select_from(char_table_name)
                .where(column("codepoint_dec") == codepoint)
            )
            for row in con.execute(query):
                char = dict(row._mapping) | char
    return update_character_properties(char, prop_group)
