from sqlite3 import LEGACY_TRANSACTION_CONTROL
from sqlite3 import Connection as SQLite3Connection

from sqlalchemy import event
from sqlmodel import create_engine

from app.config.api_settings import get_settings


def setup_rw_db_conn(db_conn, _):  # pragma: no cover
    if isinstance(db_conn, SQLite3Connection):
        db_conn.autocommit = True
        cursor = db_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.execute("PRAGMA journal_mode=OFF;")
        cursor.execute("PRAGMA synchronous=OFF;")
        cursor.execute("PRAGMA cache_size=100000;")
        cursor.execute("PRAGMA locking_mode=EXCLUSIVE;")
        cursor.execute("PRAGMA temp_store=MEMORY;")
        cursor.close()


def setup_ro_db_conn(db_conn, _):
    if isinstance(db_conn, SQLite3Connection):
        db_conn.autocommit = LEGACY_TRANSACTION_CONTROL
        db_conn.isolation_level = None
        cursor = db_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.execute("PRAGMA cache_size=100000;")
        cursor.execute("PRAGMA locking_mode=EXCLUSIVE;")
        cursor.execute("PRAGMA page_size=32768;")
        cursor.close()


settings = get_settings()

rw_db_engine = create_engine(settings.DB_URL, echo=False, connect_args={"check_same_thread": False})
event.listen(rw_db_engine, "connect", setup_rw_db_conn)

ro_db_engine = create_engine(settings.DB_URL, echo=False, connect_args={"check_same_thread": False})
event.listen(ro_db_engine, "connect", setup_ro_db_conn)
