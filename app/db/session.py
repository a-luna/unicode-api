from typing import TYPE_CHECKING, Any

from sqlalchemy.engine import Engine
from sqlmodel import Session

import app.db.procs.filter_characters as proc_filter_all_characters
import app.db.procs.get_char_details as proc_get_character_properties
import app.db.procs.get_unicode_versions as proc_get_all_unicode_versions
from app.db.engine import engine
from app.schemas.enums import CharPropertyGroup

if TYPE_CHECKING:  # pragma: no cover
    from app.api.api_v1.dependencies.filter_params import FilterParameters


def get_session():
    with Session(engine) as session:
        yield DBSession(session, engine)


class DBSession:
    def __init__(self, session: Session, engine: Engine):
        self.session = session
        self.engine = engine

    def all_unicode_versions(self):
        return proc_get_all_unicode_versions.get_all_unicode_versions(self.session)

    def get_character_properties(
        self, codepoint: int, show_props: list[CharPropertyGroup] | None, verbose: bool
    ) -> dict[str, Any]:
        return proc_get_character_properties.get_character_properties(self.engine, codepoint, show_props, verbose)

    def filter_all_characters(self, filter_params: "FilterParameters") -> list[int]:
        return proc_filter_all_characters.filter_all_characters(self.session, filter_params)
