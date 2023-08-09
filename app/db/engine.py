# flake8: noqa
import app.db.models as db
from sqlalchemy import event
from sqlmodel import create_engine

from app.core.config import settings


def _fk_pragma_on_connect(dbapi_con, _):
    dbapi_con.execute("pragma journal_mode=OFF")
    dbapi_con.execute("PRAGMA synchronous=OFF")
    dbapi_con.execute("PRAGMA cache_size=100000")


engine = create_engine(settings.DB_URL, echo=False, connect_args={"check_same_thread": False})
event.listen(engine, "connect", _fk_pragma_on_connect)
