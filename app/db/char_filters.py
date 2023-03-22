from sqlalchemy import column, or_, select
from sqlalchemy.sql import Select
from sqlmodel import Session

import app.db.engine as db
from app.api.api_v1.dependencies import FilterParameters

CHAR_TABLES = [db.UnicodeCharacter, db.UnicodeCharacterNoName]


def filter_all_characters(session: Session, filter_params: FilterParameters) -> list[int]:
    statements = []
    for table in CHAR_TABLES:
        statement = select(column("codepoint_dec")).select_from(table)
        if filter_params.name:
            statement = statement.where(column("name").contains(filter_params.name.upper()))
        if filter_params.categories:
            statement = statement.where(column("general_category").in_(filter_params.categories))
        if filter_params.age_list:
            statement = statement.where(column("age").in_(filter_params.age_list))
        if filter_params.scripts:
            script_conditions = [column("script_extensions").contains(script.code) for script in filter_params.scripts]
            statement = statement.where(or_(*script_conditions))
        statements.append(statement)
    return apply_filter(session, statements)


def apply_filter(session: Session, statements: list[Select]) -> list[int]:
    all_codepoints = get_all_assigned_codepoints(session)
    matching_codepoints = []
    for statement in statements:
        results = session.execute(statement).scalars().all()
        matching_codepoints.extend(results)
    return sorted(set(all_codepoints).intersection(set(matching_codepoints)))


def get_all_assigned_codepoints(session: Session) -> list[int]:
    codepoints = []
    for table in CHAR_TABLES:
        statement = select(column("codepoint_dec")).select_from(table)
        results = session.execute(statement).scalars().all()
        codepoints.extend(results)
    return sorted(codepoints)
