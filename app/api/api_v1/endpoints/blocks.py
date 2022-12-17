from functools import lru_cache
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from rapidfuzz import process
from sqlmodel import Session

import app.core.db as db
from app.api.api_v1.dependencies import (
    BlockSearchParameters,
    ListParametersDecimal,
    UnicodeBlockPathParamResolver,
    UnicodePlaneResolver,
)
from app.api.api_v1.pagination import paginate_search_results
from app.core.config import settings
from app.core.enums.block_name import UnicodeBlockName

router = APIRouter()


@router.get("", response_model=db.PaginatedList[db.UnicodeBlockResponse], response_model_exclude_unset=True)
def list_all_unicode_blocks(
    list_params: ListParametersDecimal = Depends(),
    plane: UnicodePlaneResolver = Depends(),
    session: Session = Depends(db.get_session),
):
    start_block_id = plane.start_block_id
    finish_block_id = plane.finish_block_id
    start = start_block_id
    if list_params.starting_after:
        start = list_params.starting_after + 1
    elif list_params.ending_before:
        start = list_params.ending_before - list_params.limit
    stop = min(finish_block_id + 1, start + list_params.limit)
    if start < start_block_id or start > finish_block_id:
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail=(
                f"The starting block id ({start}) is not within the range of blocks which comprise the specified "
                f"Unicode plane ({plane.plane.name}): first block: {start_block_id}, last block: {finish_block_id}"
            ),
        )

    return {
        "url": f"{settings.API_VERSION}/blocks",
        "has_more": stop <= finish_block_id,
        "data": [db.UnicodeBlock.responsify(session.get(db.UnicodeBlock, id)) for id in range(start, stop)],
    }


@router.get(
    "/search",
    response_model=db.PaginatedSearchResults[db.UnicodeBlockResult],
    response_model_exclude_unset=True,
)
def search_unicode_blocks_by_name(
    search_params: BlockSearchParameters = Depends(),
    session: Session = Depends(db.get_session),
):
    params = {
        "url": f"{settings.API_VERSION}/blocks/search",
        "query": search_params.name,
    }
    results = search_blocks_by_name(session, search_params.name, search_params.min_score)
    if results:
        paginate_result = paginate_search_results(results, search_params.per_page, search_params.page)
        if paginate_result.failure:
            raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=paginate_result.error)
        paginated = paginate_result.value
        if paginated:
            return params | paginated
    return params | {
        "current_page": 0,
        "total_results": 0,
        "has_more": False,
        "results": [],
    }


@router.get(
    "/{block}",
    response_model=db.UnicodeBlockResponse,
    response_model_exclude_unset=True,
)
def get_unicode_block_details(block: UnicodeBlockPathParamResolver = Depends()):
    return db.UnicodeBlock.responsify(block.block)


@lru_cache
def get_block_name_map(session: Session) -> dict[int, str]:
    return {block.id: block.name.lower() for block in session.query(db.UnicodeBlock).all()}


def search_blocks_by_name(session: Session, query: str, score_cutoff: int = 80) -> list[db.UnicodeBlockResult]:
    block_name_map = get_block_name_map(session)
    return [
        db.UnicodeBlockResult(
            id=result,
            name=get_block_by_id(session, result).name,
            plane=get_block_by_id(session, result).plane.abbreviation,
            start=f"U+{get_block_by_id(session, result).start}",
            finish=f"U+{get_block_by_id(session, result).finish}",
            start_dec=get_block_by_id(session, result).start_dec,
            finish_dec=get_block_by_id(session, result).finish_dec,
            total_allocated=get_block_by_id(session, result).total_allocated,
            total_defined=get_block_by_id(session, result).total_defined,
            score=float(f"{score:.1f}"),
            link=f"{settings.API_VERSION}/blocks/{UnicodeBlockName.from_block_id(result).name}",
        )
        for (_, score, result) in process.extract(query.lower(), block_name_map, limit=len(block_name_map))
        if score >= float(score_cutoff)
    ]


def get_block_by_id(session: Session, block_id: int) -> db.UnicodeBlock:
    return session.query(db.UnicodeBlock).filter(db.UnicodeBlock.id == block_id).one()
