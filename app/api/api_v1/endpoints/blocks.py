from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from app.api.api_v1.dependencies import (
    ListParametersDecimal,
    BlockSearchParameters,
    UnicodeBlockPathParamResolver,
    UnicodePlaneResolver,
    get_unicode,
)
from app.core.config import settings
from app.core.util import paginate_search_results
from app.data.unicode import Unicode
from app.schemas import PaginatedList, PaginatedSearchResults, UnicodeBlock, UnicodeBlockResult

router = APIRouter()


@router.get("", response_model=PaginatedList[UnicodeBlock], response_model_exclude_unset=True)
def list_all_unicode_blocks(
    list_params: ListParametersDecimal = Depends(),
    plane: UnicodePlaneResolver = Depends(),
    unicode: Unicode = Depends(get_unicode),
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
        "data": [unicode.block_map.get(id) for id in range(start, stop)],
    }


@router.get(
    "/search",
    response_model=PaginatedSearchResults[UnicodeBlockResult],
    response_model_exclude_unset=True,
)
def search_unicode_blocks_by_name(
    search_params: BlockSearchParameters = Depends(),
    unicode: Unicode = Depends(get_unicode),
):
    params = {
        "url": f"{settings.API_VERSION}/blocks/search",
        "query": search_params.name,
    }
    results = unicode.search_blocks_by_name(search_params.name, search_params.min_score)
    if not results:
        return params | {
            "current_page": 0,
            "total_results": 0,
            "has_more": False,
            "results": [],
        }
    paginate_result = paginate_search_results(results, search_params.per_page, search_params.page)
    if paginate_result.failure:
        raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=paginate_result.error)
    paginated = paginate_result.value
    return params | paginated


@router.get("/{block}", response_model=UnicodeBlock, response_model_exclude_unset=True,)
def get_unicode_block_details(block: UnicodeBlockPathParamResolver = Depends()):
    return block.block
