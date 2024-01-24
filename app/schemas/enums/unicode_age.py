from enum import Enum
from typing import Self

from app.data.constants import UNICODE_VERSION_RELEASE_DATES

UnicodeAge = Enum(
    "UnicodeAge", {f'V{ver.replace(".", "_")}': ver[:-2] for ver in list(UNICODE_VERSION_RELEASE_DATES.keys())}
)


@classmethod
def match_loosely_unicode_version(cls, value: str) -> Self:
    version_map = {}
    for e in cls:
        version_map[e.value] = e.value
        if e.value.endswith(".0"):
            version_map[e.value[:-2]] = e.value
    return version_map.get(value)


def __str__(self) -> str:  # noqa: N807
    return self.value


UnicodeAge.match_loosely = match_loosely_unicode_version
UnicodeAge.__str__ = __str__
