from typing import Any

import app.db.models as db
from app.db.session import DBSession


def get_character_details(
    db_ctx: DBSession,
    codepoint: int,
    show_props: list[db.CharPropertyGroup] | None,
    score: float | None = None,
    verbose: bool = False,
) -> dict[str, Any]:
    response_dict = db_ctx.get_character_properties(codepoint, show_props, verbose)
    if score:
        response_dict["score"] = float(f"{score:.1f}")
    return response_dict
