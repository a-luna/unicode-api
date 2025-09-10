"""
This module provides database session management and access functionality for the Unicode API.

It defines a session generator function and a DBSession class that wraps database
interactions for Unicode character queries, filtering, and version information.

Functions:
    get_session(): Generator function that yields a DBSession instance with an active
                  database connection.

Classes:
    DBSession: Encapsulates database operations specific to Unicode data access,
              providing methods for character properties, filtering, and version information.
"""

from collections.abc import Generator
from typing import TYPE_CHECKING, Any

from sqlalchemy.engine import Engine
from sqlmodel import Session

import unicode_api.db.procs.filter_characters as proc_filter
import unicode_api.db.procs.get_char_details as proc_char
import unicode_api.db.procs.get_unicode_versions as proc_ver
from unicode_api.config.api_settings import get_settings
from unicode_api.db.engine import ro_db_engine as engine
from unicode_api.enums.property_group import CharPropertyGroup

if TYPE_CHECKING:  # pragma: no cover
    from unicode_api.api.api_v1.dependencies.filter_settings import FilterParameters


def get_session() -> Generator["DBSession", None, None]:
    """
    Creates a database session generator.

    This function generates a database session that's wrapped in a transaction.
    It yields a `DBSession` instance that encapsulates both the SQLAlchemy session
    and engine objects.

    Yields:
        DBSession: An object containing the active database session and engine.

    Note:
        The session is automatically closed when the generator is exhausted,
        ensuring proper resource cleanup.
    """
    with Session(engine) as session:
        yield DBSession(session, engine)


class DBSession:
    """
    A database session wrapper for Unicode database operations.

    This class encapsulates a SQLAlchemy session and engine to provide
    a simplified interface for accessing Unicode character data and metadata
    from the database.

    Attributes:
        session (Session): The SQLAlchemy session object for database operations.
        engine (Engine): The SQLAlchemy engine instance.
        api_settings: Application settings retrieved from the configuration.

    The class provides methods for retrieving Unicode version information,
    accessing character properties by codepoint, and filtering Unicode
    characters based on various criteria.
    """

    def __init__(self, session: Session, engine: Engine) -> None:
        self.session = session
        self.engine = engine
        self.api_settings = get_settings()

    def all_unicode_versions(self) -> list[str]:
        """
        Retrieves all available Unicode versions from the database.

        Returns:
            list[str]: A list of Unicode version strings (e.g., ['1.0.0', '1.1.0', ...]).
        """
        return proc_ver.get_all_unicode_versions(self.session)

    def get_character_properties(
        self, codepoint: int, show_props: list[CharPropertyGroup], verbose: bool
    ) -> dict[str, Any]:
        """
        Retrieves properties of a Unicode character identified by its codepoint.

        Parameters:
            codepoint (int): The Unicode codepoint of the character.
            show_props (list[CharPropertyGroup] | None): List of character property groups to include.
                If None, all properties are included.
            verbose (bool): If True, provides more detailed property information.

        Returns:
            dict[str, Any]: A dictionary of character properties where keys are property names
                and values are the corresponding property values.
        """
        return proc_char.get_character_properties(self.engine, codepoint, show_props, verbose)

    def filter_all_characters(self, filter_params: "FilterParameters") -> list[int]:
        """
        Filter Unicode characters based on specified parameters.

        This method queries the database to find all Unicode character code points
        that match the criteria specified in the filter parameters.

        Args:
            filter_params (FilterParameters): Parameters to filter Unicode characters by.
                This can include properties such as block, category, age, etc.

        Returns:
            list[int]: A list of Unicode code points (integers) that match the filter criteria.
        """
        return proc_filter.filter_all_characters(self.session, filter_params)
