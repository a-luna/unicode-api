from enum import Enum

from app.data.cache import cached_data

UnicodeAge = Enum("UnicodeAge", {f'V{ver.replace(".", "_")}': ver for ver in cached_data.all_unicode_versions})


@classmethod
def match_loosely_unicode_version(cls, ver: str):
    version_map = {e.value: e.value for e in cls}
    return version_map.get(ver)


UnicodeAge.match_loosely = match_loosely_unicode_version
