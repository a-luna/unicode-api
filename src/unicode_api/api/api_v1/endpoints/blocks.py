from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

import unicode_api.db.models as db
from unicode_api.api.api_v1.dependencies import (
    BlockSearchParameters,
    ListParametersDecimal,
    UnicodeBlockPathParamResolver,
    UnicodePlaneResolver,
)
from unicode_api.api.api_v1.pagination import paginate_search_results
from unicode_api.config.api_settings import get_settings
from unicode_api.core.cache import cached_data

router = APIRouter()


@router.get("", response_model=db.PaginatedList[db.UnicodeBlockResponse], response_model_exclude_unset=True)
def list_all_unicode_blocks(
    list_params: Annotated[ListParametersDecimal, Depends()], plane: Annotated[UnicodePlaneResolver, Depends()]
):
    (start, stop) = get_block_list_endpoints(list_params, plane)
    return {
        "url": f"{get_settings().API_VERSION}/blocks",
        "has_more": stop <= plane.finish_block_id,
        "data": [cached_data.get_unicode_block_by_id(id).as_response() for id in range(start, stop)],
    }


@router.get(
    "/search",
    response_model=db.PaginatedSearchResults[db.UnicodeBlockResult],
    response_model_exclude_unset=True,
)
def search_unicode_blocks_by_name(
    search_params: Annotated[BlockSearchParameters, Depends()],
) -> dict[str, Any]:
    params = {
        "url": f"{get_settings().API_VERSION}/blocks/search",
        "query": search_params.name,
    }
    results = cached_data.search_blocks_by_name(search_params.name, search_params.min_score)
    if not results:
        return params | {
            "current_page": 0,
            "total_results": 0,
            "has_more": False,
            "results": [],
        }
    block_ids = [block_id for (block_id, _) in results]
    paginate_result = paginate_search_results(block_ids, search_params.per_page, search_params.page)
    if paginate_result.failure:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=paginate_result.error)
    paginated = paginate_result.value if paginate_result.value else {}
    start = paginated.pop("start", 0)
    end = paginated.pop("end", 0)
    paginated["results"] = [
        cached_data.get_unicode_block_by_id(block_id).as_search_result(score)
        for (block_id, score) in results[start:end]
    ]
    return params | paginated


@router.get(
    "/{name}",
    response_model=db.UnicodeBlockResponse,
    response_model_exclude_unset=True,
)
def get_unicode_block_details(name: Annotated[UnicodeBlockPathParamResolver, Depends()]):
    return name.block.as_response()


def get_block_list_endpoints(list_params: ListParametersDecimal, plane: UnicodePlaneResolver) -> tuple[int, int]:
    start = plane.start_block_id
    if list_params.starting_after:
        start = list_params.starting_after + 1
    if list_params.ending_before:
        start = list_params.ending_before - list_params.limit
    stop = min(plane.finish_block_id + 1, start + list_params.limit)
    if start >= plane.start_block_id and start <= plane.finish_block_id:
        return (start, stop)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=(
            f"The starting block id ({start}) is not within the range of blocks which comprise the "
            f"specified Unicode plane ({plane.plane.name}): first block: {plane.start_block_id}, "
            f"last block: {plane.finish_block_id}"
        ),
    )
