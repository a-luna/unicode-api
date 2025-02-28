import itertools
import re

UNDERSCORE_RE = re.compile(r"(?<=[^\-_])[\-_]+[^\-_]")


def normalize_string_lm3(s: str) -> str:
    # https://www.unicode.org/reports/tr44/#UAX44-LM3
    s = s.lower().strip()
    if s.startswith("is") and len(s) > 2:  # pragma: no cover
        s = s[2:]
    return re.compile(r"\s+").sub("", s).replace("-", "").replace("_", "")


def to_lower_camel(input: str) -> str:
    s = "" if input is None else re.sub(r"\s+", "", str(input))
    if s.isupper() or s.isnumeric():
        return input
    if len(s) != 0 and not s[:2].isupper():  # pragma: no cover
        s = s[0].lower() + s[1:]
    return UNDERSCORE_RE.sub(lambda m: m.group(0)[-1].upper(), s)


def flatten_list2d[T](list2d: list[list[T]]) -> list[T]:
    return list(itertools.chain(*list2d))
