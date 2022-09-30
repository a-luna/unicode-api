from rapidfuzz import process


def get_codepoint_string(codepoint: int) -> str:
    return f"U+{hex(codepoint)[2:].upper()}"


def fuzzy_match(query, mapped_choices, limit=10, score_cutoff=88):
    best_matches = [
        {"match": match, "score": score, "result": result}
        for (match, score, result) in process.extract(query, mapped_choices, score_cutoff=score_cutoff)
    ]
    return best_matches or [
        {"match": match, "score": score, "result": result}
        for (match, score, result) in process.extract(query, mapped_choices, limit=limit)
    ]
