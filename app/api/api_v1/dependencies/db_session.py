from typing import Any

from sqlalchemy import column, or_, select
from sqlalchemy.engine import Engine
from sqlalchemy.sql import Select
from sqlmodel import Session

import app.db.engine as db
from app.api.api_v1.dependencies.filter_params import FilterParameters
from app.db.get_char_details import get_character_properties
from app.schemas.enums import CharPropertyGroup

CHAR_TABLES = [db.UnicodeCharacter, db.UnicodeCharacterNoName]


def get_session():
    with Session(db.engine) as session:
        yield DBSession(session, db.engine)


class DBSession:
    def __init__(self, session: Session, engine: Engine):
        self.session = session
        self.engine = engine

    def get_character_properties(self, codepoint: int, show_props: list[CharPropertyGroup] | None) -> dict[str, Any]:
        return get_character_properties(self.engine, codepoint, show_props)

    def filter_all_characters(self, filter_params: FilterParameters) -> list[int]:
        queries = [construct_filter_query(filter_params, table) for table in CHAR_TABLES]
        return apply_filter(self.session, queries)


def construct_filter_query(
    filter_params: FilterParameters, table: db.UnicodeCharacter | db.UnicodeCharacterNoName
) -> Select:
    query = select(column("codepoint_dec")).select_from(table)
    if filter_params.name:
        query = query.where(column("name").contains(filter_params.name.upper()))
    if filter_params.categories:
        query = query.where(column("general_category").in_(filter_params.categories))
    if filter_params.age_list:
        query = query.where(column("age").in_(filter_params.age_list))
    if filter_params.scripts:
        script_conditions = [column("script_extensions").contains(script.code) for script in filter_params.scripts]
        query = query.where(or_(*script_conditions))
    if filter_params.bidi_class_list:
        query = query.where(column("bidirectional_class").in_(filter_params.bidi_class_list))
    if filter_params.decomp_types:
        query = query.where(column("decomposition_type").in_(filter_params.decomp_types))
    if filter_params.line_break_types:
        query = query.where(column("line_break").in_(filter_params.line_break_types))
    if filter_params.ccc_list:
        query = query.where(column("combining_class").in_(filter_params.ccc_list))
    return query


def apply_filter(session: Session, queries: list[Select]) -> list[int]:
    matching_codepoints = []
    for query in queries:
        results = session.execute(query).scalars().all()
        matching_codepoints.extend(results)
    return sorted(set(matching_codepoints))
