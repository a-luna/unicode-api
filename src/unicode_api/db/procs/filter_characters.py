from typing import TYPE_CHECKING

from sqlmodel import Session, column, or_, select, true
from sqlmodel.sql._expression_select_cls import SelectOfScalar

import unicode_api.db.models as db

if TYPE_CHECKING:  # pragma: no cover
    from unicode_api.api.api_v1.dependencies.filter_settings import FilterParameters

CHAR_TABLES = [db.UnicodeCharacter, db.UnicodeCharacterUnihan]


def filter_all_characters(session: Session, filter_params: "FilterParameters") -> list[int]:
    """
    Apply filtering logic to all character types and return matching codepoints.

    This function applies the provided filter parameters across all character tables
    and returns a sorted list of unique codepoints that match the criteria.

    Args:
        session (Session): The database session used to execute queries.
        filter_params (FilterParameters): The filtering criteria to apply.

    Returns:
        list[int]: A sorted list of unique codepoints that match the filter criteria.

    Note:
        This function aggregates results from all character tables by constructing
        separate queries for each table and combining the results.
    """
    matching_codepoints: list[int] = []
    for query in [_construct_filter_query(filter_params, table) for table in CHAR_TABLES]:
        if query is None:
            continue
        results = session.scalars(query).all()
        matching_codepoints.extend(results)
    return sorted(set(matching_codepoints))


def _construct_filter_query(  # noqa: C901
    filter_params: "FilterParameters",
    table: type[db.UnicodeCharacter | db.UnicodeCharacterUnihan],
) -> SelectOfScalar[int] | None:
    if table == db.UnicodeCharacter and filter_params.cjk_definition:
        return None
    query = select(table.codepoint_dec)
    if filter_params.name:
        query = query.where(column("name").regexp_match(f"\\b{filter_params.name.upper()}\\b"))
    if filter_params.cjk_definition:
        query = query.where(column("description").regexp_match(f"\\b{filter_params.cjk_definition.lower()}\\b"))
    if filter_params.blocks:
        query = query.where(column("block_id").in_(filter_params.blocks))
    if filter_params.categories:
        query = query.where(column("general_category_id").in_(filter_params.categories))
    if filter_params.age_list:
        query = query.where(column("age_id").in_(filter_params.age_list))
    if filter_params.scripts:
        names, ids = filter_params.scripts
        script_conditions = [column("script_extensions").contains(s) for s in names] + [column("script_id").in_(ids)]
        query = query.where(or_(*script_conditions))
    if filter_params.bidi_class_list:
        query = query.where(column("bidi_class_id").in_(filter_params.bidi_class_list))
    if filter_params.decomp_types:
        query = query.where(column("decomposition_type_id").in_(filter_params.decomp_types))
    if filter_params.line_break_types:
        query = query.where(column("line_break_id").in_(filter_params.line_break_types))
    if filter_params.ccc_list:
        query = query.where(column("combining_class_id").in_(filter_params.ccc_list))
    if filter_params.num_types:
        query = query.where(column("numeric_type_id").in_(filter_params.num_types))
    if filter_params.join_types:
        query = query.where(column("joining_type_id").in_(filter_params.join_types))
    if filter_params.flags and len(filter_params.flags) > 0:
        flag_conditions = [column(flag.db_column_name) == true() for flag in filter_params.flags if flag]
        query = query.where(or_(*flag_conditions))

    return query
