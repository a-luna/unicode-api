from sqlmodel import Session

from unicode_api.db.engine import ro_db_engine as engine
from unicode_api.db.session import DBSession


def test_get_all_unicode_versions():
    unicode_versions = []
    with Session(engine) as session:
        db_session = DBSession(session, engine)
        unicode_versions = db_session.all_unicode_versions()
    assert len(unicode_versions) == 25
    assert unicode_versions[0] == "1.1"
    assert unicode_versions[-1] == "15.0"
