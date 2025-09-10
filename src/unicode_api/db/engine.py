"""
Database engine configuration module for SQLite with SQLAlchemy.

This module sets up two separate database engine configurations:
1. A read-write (rw) connection optimized for write operations
2. A read-only (ro) connection optimized for read performance

Both engines connect to the same database URL but with different connection
parameters and PRAGMA settings to optimize for their specific use cases.

The module configures SQLite connections with custom event listeners that:
- Enable foreign key constraints
- Adjust caching and memory settings
- Configure transaction control mechanisms
- Set locking modes

These optimizations help improve performance for their respective operation types
while maintaining appropriate safety levels for each use case.
"""

from sqlite3 import LEGACY_TRANSACTION_CONTROL
from sqlite3 import Connection as SQLite3Connection
from typing import Any

from sqlalchemy import event
from sqlmodel import create_engine

from unicode_api.config.api_settings import get_settings


def setup_rw_db_conn(db_conn: SQLite3Connection, _: Any) -> None:  # pragma: no cover
    """
    Set up a SQLite database connection with optimized settings for read-write operations.
    This function configures SQLite connection parameters to optimize for performance in a read-write
    context. It enables foreign key constraints and sets various pragmas to improve performance.

    Parameters
    ----------
    db_conn : SQLite3Connection
        The SQLite database connection to configure
    _ : Any
        Unused parameter (maintained for compatibility with connection event listeners)

    Notes
    -----
    Performance optimizations include:
    - Enabling foreign key constraints
    - Disabling journaling mode
    - Setting synchronous mode to OFF (improves speed but reduces crash safety)
    - Increasing cache size to 100000 pages
    - Setting exclusive locking mode
    - Storing temporary tables in memory
    Warning: Some of these settings prioritize performance over durability. Not recommended
    for applications where data integrity after crashes is critical.
    """

    db_conn.autocommit = True
    cursor = db_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.execute("PRAGMA journal_mode=OFF;")
    cursor.execute("PRAGMA synchronous=OFF;")
    cursor.execute("PRAGMA cache_size=100000;")
    cursor.execute("PRAGMA locking_mode=EXCLUSIVE;")
    cursor.execute("PRAGMA temp_store=MEMORY;")
    cursor.close()


def setup_ro_db_conn(db_conn: SQLite3Connection, _: Any) -> None:
    """
    Configure a read-only SQLite database connection with optimized settings.

    This function applies performance-optimized settings to a SQLite connection,
    including enabling foreign key constraints, increasing cache size, setting
    exclusive locking mode, and configuring a larger page size.

    Parameters
    ----------
    db_conn : SQLite3Connection
        The SQLite database connection to configure
    _ : Any
        Unused parameter (maintained for compatibility with connection event listeners)

    Notes
    -----
    - Sets autocommit to LEGACY_TRANSACTION_CONTROL
    - Sets isolation_level to None
    - Enables foreign key constraints
    - Sets cache size to 100,000 pages
    - Uses exclusive locking mode
    - Sets page size to 32KB (32,768 bytes)
    """
    db_conn.autocommit = LEGACY_TRANSACTION_CONTROL
    db_conn.isolation_level = None
    cursor = db_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.execute("PRAGMA cache_size=100000;")
    cursor.execute("PRAGMA locking_mode=EXCLUSIVE;")
    cursor.execute("PRAGMA page_size=32768;")
    cursor.close()


settings = get_settings()

rw_db_engine = create_engine(settings.db_url, echo=False, connect_args={"check_same_thread": False})
event.listen(rw_db_engine, "connect", setup_rw_db_conn)

ro_db_engine = create_engine(settings.db_url, echo=False, connect_args={"check_same_thread": False})
event.listen(ro_db_engine, "connect", setup_ro_db_conn)
