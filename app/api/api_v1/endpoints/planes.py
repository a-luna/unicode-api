from fastapi import APIRouter, Depends, Path

from app.api.api_v1.dependencies import get_unicode
from app.core.config import settings
from app.data.unicode import Unicode
from app.schemas import PaginatedList, UnicodePlane

router = APIRouter()


@router.get("", response_model=PaginatedList[UnicodePlane])
def list_all_unicode_planes(unicode: Unicode = Depends(get_unicode)):
    return {
        "url": f"{settings.API_VERSION}/planes",
        "total_results": unicode.total_defined_planes,
        "has_more": False,
        "data": unicode.planes,
    }


@router.get("/{number}", response_model=UnicodePlane, response_model_exclude_unset=True,)
def get_unicode_plane_details(number: int = Path(ge=0, le=16), unicode: Unicode = Depends(get_unicode)):
    return unicode.get_plane_details(number)
