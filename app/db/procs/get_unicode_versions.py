from sqlalchemy import column
from sqlalchemy.exc import OperationalError
from sqlmodel import Session, distinct, select

import app.db.models as db


def get_all_unicode_versions(session: Session):
    try:
        versions = []
        for query in [select(distinct(table.age_id)) for table in db.CHAR_TABLES]:
            results = session.scalars(query).all()
            v_query = select(column("short_name")).select_from(db.Age).where(column("id").in_(results))
            v_results = session.scalars(v_query).all()
            versions.extend(float(ver) for ver in v_results)
        return [str(ver) for ver in sorted(set(versions))]
    except OperationalError:  # pragma: no cover
        return []
