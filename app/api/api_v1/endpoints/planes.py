from typing import Annotated

from fastapi import APIRouter, Path

import app.db.models as db
from app.core.config import get_settings
from app.data.cache import cached_data

router = APIRouter()


@router.get("", response_model=db.PaginatedList[db.UnicodePlaneResponse])
def list_all_unicode_planes():
    planes = [db.UnicodePlane.responsify(plane) for plane in cached_data.planes]
    return {
        "url": f"{get_settings().API_VERSION}/planes",
        "total_results": len(planes),
        "has_more": False,
        "data": planes,
    }


@router.get(
    "/{number}",
    response_model=db.UnicodePlaneResponse,
    response_model_exclude_unset=True,
)
def get_unicode_plane_details(number: Annotated[int, Path(ge=0, le=16)]):
    plane = cached_data.get_unicode_plane_by_number(number)
    return db.UnicodePlane.responsify(plane)
