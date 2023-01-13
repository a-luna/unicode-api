from functools import cache

from sqlalchemy import column, select, text
from sqlalchemy.engine import Engine
from sqlmodel import Session

import app.db.engine as db


class DatabaseCache:
    @cache
    def all_codepoints_for_uniquely_named_chars(self, session: Session) -> set[int]:
        return set(char.codepoint_dec for char in session.query(db.UnicodeCharacter).all())

    @cache
    def all_codepoints_for_generically_named_chars(self, session: Session) -> set[int]:
        return set(char.codepoint_dec for char in session.query(db.UnicodeCharacterNoName).all())

    @cache
    def unique_character_name_map(self, engine: Engine):
        name_map = {}
        with engine.connect() as con:
            query = select([column("codepoint_dec"), column("name")]).select_from(db.UnicodeCharacter)
            name_map = {row["codepoint_dec"]: row["name"] for row in con.execute(query)}
        return name_map
