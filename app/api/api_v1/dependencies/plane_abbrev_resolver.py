from http import HTTPStatus

from fastapi import HTTPException, Query

from app.data.cache import cached_data
from app.docs.dependencies.custom_parameters import PLANE_NAME_DESCRIPTION


class UnicodePlaneResolver:
    def __init__(
        self,
        plane: str | None = Query(default=None, description=PLANE_NAME_DESCRIPTION),
    ):
        self.plane = cached_data.get_unicode_plane_by_abbreviation(plane) if plane else cached_data.all_characters_plane
        if self.plane.name != "None":
            self.start_block_id = self.plane.start_block_id
            self.finish_block_id = self.plane.finish_block_id
        else:
            raise HTTPException(
                status_code=int(HTTPStatus.BAD_REQUEST),
                detail=(f"{plane} does not match any Unicode plane abbreviation: {get_all_plane_abbreviations()}."),
            )


def get_all_plane_abbreviations() -> str:
    return ", ".join([p.abbreviation for p in cached_data.planes])
