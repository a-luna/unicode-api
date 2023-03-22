from typing import Any

from app.core.result import Result


def paginate_search_results(
    codepoints: list[int],
    per_page: int,
    page_number: int,
) -> Result[dict[str, Any]]:
    (full_page_count, final_page_length) = divmod(len(codepoints), per_page)
    total_pages = full_page_count if final_page_length == 0 else (full_page_count + 1)
    if page_number > total_pages:
        needs_plural = total_pages > 1
        return Result.Fail(
            f"Request for page #{page_number} is invalid since there {'are' if needs_plural else 'is only'} "
            f"{total_pages} total page{'s' if needs_plural else ''}."
        )
    has_more = page_number < total_pages
    page_start = per_page * (page_number - 1)
    page_end = min(len(codepoints), page_start + per_page)
    paginated = {
        "total_results": len(codepoints),
        "has_more": has_more,
        "current_page": page_number,
        "start": page_start,
        "end": page_end,
    }
    if has_more:
        paginated["next_page"] = page_number + 1
    return Result.Ok(paginated)
