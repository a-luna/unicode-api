import re


def normalize_string_lm3(s: str) -> str:
    # https://www.unicode.org/reports/tr44/#UAX44-LM3
    s = s.lower().strip()
    if s.startswith("is") and len(s) > 2:  # pragma: no cover
        s = s[2:]
    return re.compile(r"\s+").sub("", s).replace("-", "").replace("_", "")
