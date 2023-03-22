NAME_SPIRITUS_CATEGORY_MN_SCRIPT_COPT = {
    "url": "/v1/characters/filter",
    "hasMore": False,
    "currentPage": 1,
    "totalResults": 2,
    "results": [
        {"character": "⳰", "name": "COPTIC COMBINING SPIRITUS ASPER", "codepoint": "U+2CF0", "uriEncoded": "%E2%B3%B0"},
        {"character": "⳱", "name": "COPTIC COMBINING SPIRITUS LENIS", "codepoint": "U+2CF1", "uriEncoded": "%E2%B3%B1"},
    ],
}

INVALID_PAGE_NUMBER = {"detail": "Request for page #2 is invalid since there is only 1 total page."}

NO_CHARS_MATCH_SETTINGS = {
    "url": "/v1/characters/filter",
    "hasMore": False,
    "currentPage": 0,
    "totalResults": 0,
    "results": [],
}

FILTER_BY_UNICODE_AGE = {
    "url": "/v1/characters/filter",
    "hasMore": False,
    "currentPage": 1,
    "totalResults": 4,
    "results": [
        {"character": "࢈", "name": "ARABIC RAISED ROUND DOT", "codepoint": "U+0888", "uriEncoded": "%E0%A2%88"},
        {"character": "꭪", "name": "MODIFIER LETTER LEFT TACK", "codepoint": "U+AB6A", "uriEncoded": "%EA%AD%AA"},
        {"character": "꭫", "name": "MODIFIER LETTER RIGHT TACK", "codepoint": "U+AB6B", "uriEncoded": "%EA%AD%AB"},
        {"character": "﯂", "name": "ARABIC SYMBOL WASLA ABOVE", "codepoint": "U+FBC2", "uriEncoded": "%EF%AF%82"},
    ],
}
