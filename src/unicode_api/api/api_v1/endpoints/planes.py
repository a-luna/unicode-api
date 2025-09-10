from typing import Annotated

from fastapi import APIRouter, Path

import unicode_api.db.models as db
from unicode_api.config.api_settings import get_settings
from unicode_api.core.cache import cached_data

router = APIRouter()


@router.get("", response_model=db.PaginatedList[db.UnicodePlaneResponse])
def list_all_unicode_planes():
    planes = [plane.as_response() for plane in cached_data.planes]
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
    return cached_data.get_unicode_plane_by_number(number).as_response()
