from sqlalchemy.exc import OperationalError
from sqlmodel import Session, distinct, select

import app.db.models as db


def get_all_unicode_versions(session: Session):
    try:
        versions = []
        for query in [select(distinct(table.age)) for table in db.CHAR_TABLES]:
            results = session.scalars(query).all()
            versions.extend(float(ver) for ver in results)
        return [str(ver) for ver in sorted(set(versions))]
    except OperationalError:  # pragma: no cover
        return []
