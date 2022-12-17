from typing import Any
from app.core.result import Result
import app.schemas as schemas


def paginate_search_results(
    results: list[schemas.UnicodeCharacterResult] | list[schemas.UnicodeBlockResult],
    per_page: int,
    page_number: int,
) -> Result[dict[str, Any]]:
    (full_page_count, final_page_length) = divmod(len(results), per_page)
    total_pages = full_page_count if final_page_length == 0 else (full_page_count + 1)
    if page_number > total_pages:
        return Result.Fail(f"Request for page #{page_number} is invalid since there are {total_pages} total pages.")
    has_more = page_number < total_pages
    page_start = per_page * (page_number - 1)
    page_end = min(len(results), page_start + per_page)
    paginated = {}
    paginated["total_results"] = len(results)
    paginated["has_more"] = has_more
    if has_more:
        paginated["next_page"] = page_number + 1
    paginated["results"] = results[page_start:page_end]
    return Result.Ok(paginated)
