from fastapi import APIRouter, Depends, Path
from sqlmodel import Session

import app.core.db as db
from app.core.config import settings

router = APIRouter()


@router.get("", response_model=db.PaginatedList[db.UnicodePlaneResponse])
def list_all_unicode_planes(session: Session = Depends(db.get_session)):
    planes = [db.UnicodePlane.responsify(plane) for plane in session.query(db.UnicodePlane).all()]
    return {
        "url": f"{settings.API_VERSION}/planes",
        "total_results": len(planes),
        "has_more": False,
        "data": planes,
    }


@router.get(
    "/{number}",
    response_model=db.UnicodePlaneResponse,
    response_model_exclude_unset=True,
)
def get_unicode_plane_details(number: int = Path(ge=0, le=16), session: Session = Depends(db.get_session)):
    plane = session.query(db.UnicodePlane).filter(db.UnicodePlane.number == number).first()
    return db.UnicodePlane.responsify(plane) if plane else get_undefined_plane(number)


def get_undefined_plane(plane_number: int) -> db.UnicodePlane:
    return db.UnicodePlane(
        name="Unassigned Plane",
        number=plane_number,
        abbreviation="N/A",
        start=f"U+{plane_number:X}0000",
        start_dec=int(f"{plane_number:X}0000", 16),
        finish=f"U+{plane_number:X}FFFF",
        finish_dec=int(f"{plane_number:X}FFFF", 16),
        start_block_id=0,
        finish_block_id=0,
        total_allocated=0,
        total_defined=0,
    )
