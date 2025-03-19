from enum import EnumType, IntFlag
from typing import ClassVar

from app.core.cache import cached_data
from app.models.util import normalize_string_lm3


class DynamicFlagMeta(EnumType):
    @classmethod
    def __prepare__(_, cls, bases, **kwds):  # type: ignore[reportSelfClsParameterName] # noqa: N804
        return super().__prepare__(cls, bases, **kwds)

    def __init__(cls, *args, **kwds):
        super().__init__(*args)

    def __new__(metacls, cls, bases, clsdict, **kwds):
        members = []
        if "_flag_names" in clsdict:
            flag_names = clsdict.pop("_flag_names")
            if not isinstance(flag_names, tuple | list):
                raise TypeError("_flag_names must be a tuple or list")
            members.append(("NONE", 0))
            members.extend([(name.upper(), 2**i) for i, name in enumerate(flag_names)])

        enum_dict = super().__prepare__(cls, bases, **kwds)
        for name, value in sorted(clsdict.items(), key=lambda p: (0 if p[0][0] == "_" else 1, p)):
            enum_dict[name] = value
        for name, value in members:
            enum_dict[name] = value
        return super().__new__(metacls, cls, bases, enum_dict, **kwds)


DynamicFlag = DynamicFlagMeta("DynamicFlag", (IntFlag,), {})


class CharacterFilterFlag(DynamicFlag):
    _flag_names: ClassVar[list[str]] = cached_data.character_flag_names

    def __int__(self) -> int:
        return self.value  # type: ignore[reportAttributeAccessIssue]

    @property
    def display_name(self) -> str:
        return f"Is_{self.name.replace('_', ' ').title().replace('Ascii', 'ASCII').replace(' ', '_')}"  # type: ignore[reportAttributeAccessIssue]

    @property
    def db_column_name(self) -> str:
        return self.name.lower()  # type: ignore[reportAttributeAccessIssue]

    @property
    def is_emoji_flag(self) -> bool:
        return any(s in self.name.lower() for s in ["emoji", "pictographic"])  # type: ignore[reportAttributeAccessIssue]

    @classmethod
    def match_loosely(cls, value: str) -> "CharacterFilterFlag | None":
        flag_name_map = {normalize_string_lm3(flag.name): flag for flag in cls if int(flag)}  # type: ignore[reportAttributeAccessIssue]
        return flag_name_map.get(normalize_string_lm3(value), None)

    @classmethod
    def get_all_set_flags(cls, set_flags: int) -> list["CharacterFilterFlag"]:
        return [flag for flag in cls if set_flags & int(flag) == int(flag)]
