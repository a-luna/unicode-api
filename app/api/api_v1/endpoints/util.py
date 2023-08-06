import app.db.models as db
from app.api.api_v1.dependencies.db_session import DBSession
from app.schemas.enums.property_group import CharPropertyGroup


def get_character_details(
    db_ctx: DBSession,  # noqa: F821
    codepoint: int,
    show_props: list[CharPropertyGroup] | None,
    score: float | None = None,
    verbose: bool = False,
) -> db.UnicodeCharacterResponse:
    response_dict = db_ctx.get_character_properties(codepoint, show_props, verbose)
    if score:
        response_dict["score"] = float(f"{score:.1f}")
    return db.UnicodeCharacterResponse(**response_dict)
