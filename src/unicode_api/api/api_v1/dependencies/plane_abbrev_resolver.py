from typing import Annotated

from fastapi import HTTPException, Query, status

from unicode_api.core.cache import cached_data
from unicode_api.docs.dependencies.custom_parameters import PLANE_NAME_DESCRIPTION


class UnicodePlaneResolver:
    def __init__(
        self,
        plane: Annotated[str | None, Query(description=PLANE_NAME_DESCRIPTION)] = None,
    ):
        self.plane = cached_data.get_unicode_plane_by_abbreviation(plane) if plane else cached_data.all_characters_plane
        if self.plane.name != "None":
            self.start_block_id = self.plane.start_block_id
            self.finish_block_id = self.plane.finish_block_id
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(f"{plane} does not match any Unicode plane abbreviation: {get_all_plane_abbreviations()}."),
            )


def get_all_plane_abbreviations() -> str:
    return ", ".join([p.abbreviation for p in cached_data.planes])
