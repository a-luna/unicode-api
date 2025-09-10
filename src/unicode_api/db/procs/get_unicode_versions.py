from sqlalchemy.exc import OperationalError
from sqlmodel import Session, col, distinct, select

import unicode_api.db.models as db


def get_all_unicode_versions(session: Session) -> list[str]:
    """
    Retrieve a sorted list of all unique Unicode versions available in the database.

    This function queries all character tables in the database to find the distinct age_id values,
    then retrieves the corresponding short_name values from the Age table, converts them to float
    for sorting, and finally returns them as strings.

    Args:
        session (Session): SQLAlchemy database session

    Returns:
        list[str]: A sorted list of unique Unicode versions as strings
               or an empty list if a database error occurs

    Raises:
        OperationalError: If there is a database connection issue (handled internally)
    """
    try:
        versions: list[float] = []
        for query in [select(distinct(table.age_id)) for table in db.CHAR_TABLES]:
            results = session.scalars(query).all()
            v_query = select(db.Age).where(col(db.Age.id).in_(results))
            v_results = session.exec(v_query).all()
            versions.extend(float(ver.short_name) for ver in v_results)
        return [str(ver) for ver in sorted(set(versions))]
    except OperationalError:  # pragma: no cover
        return []
