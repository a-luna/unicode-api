from enum import EnumType, IntFlag, _EnumDict  # type: ignore[reportPrivateUsage]
from typing import Any, ClassVar

from unicode_api.core.cache import cached_data
from unicode_api.models.util import normalize_string_lm3


class DynamicFlagMeta(EnumType):
    """
    DynamicFlagMeta is a metaclass for creating dynamic enumeration classes with flag-like behavior.

    This metaclass extends the functionality of `EnumType` to allow the dynamic generation of
    enumeration members based on a special `_flag_names` attribute. It also ensures that the
    enumeration members are created with unique power-of-two values, suitable for use as bit flags.

    Methods:
        __prepare__(cls, bases, **kwds):
            Prepares the namespace for the class being defined. Overrides the default behavior
            to ensure compatibility with the dynamic member generation process.

        __init__(cls, *args, **kwds):
            Initializes the class. Calls the parent class's `__init__` method.

        __new__(metacls, cls, bases, clsdict, **kwds):
            Creates a new class. Dynamically generates enumeration members based on the `_flag_names`
            attribute, if present. Ensures that `_flag_names` is a tuple or list, and assigns power-of-two
            values to the generated members. Combines the dynamically generated members with any
            explicitly defined members in the class dictionary.

    Attributes:
        _flag_names (optional):
            A tuple or list of strings representing the names of the flags to be dynamically generated.
            Each name will be converted to uppercase and assigned a unique power-of-two value.
            If `_flag_names` is not provided, no dynamic members will be generated.

    Raises:
        TypeError:
            If `_flag_names` is present but is not a tuple or list.
    """

    @classmethod
    def __prepare__(_, cls: str, bases: tuple[type, ...], **kwds: Any):  # type: ignore[reportSelfClsParameterName] # noqa: N804
        return super().__prepare__(cls, bases, **kwds)

    def __init__(cls, *args: Any, **kwds: Any):
        super().__init__(*args, **kwds)

    def __new__(metacls, cls: str, bases: tuple[type, ...], clsdict: _EnumDict, **kwds: Any):
        members: list[tuple[str, int]] = []
        if "_flag_names" in clsdict:
            flag_names: list[str] = clsdict.pop("_flag_names")
            members.append(("NONE", 0))
            members.extend([(name.upper(), 2**i) for i, name in enumerate(flag_names)])

        enum_dict = super().__prepare__(cls, bases, **kwds)
        for name, value in sorted(clsdict.items(), key=lambda p: (0 if p[0][0] == "_" else 1, p)):
            enum_dict[name] = value
        for name, value in members:
            enum_dict[name] = value
        return super().__new__(metacls, cls, bases, enum_dict, **kwds)


DynamicFlag = DynamicFlagMeta("DynamicFlag", (IntFlag,), _EnumDict())


class CharacterFilterFlag(DynamicFlag):
    """
    CharacterFilterFlag is a dynamic enumeration class that represents various character filter flags.
    It provides utility methods and properties for working with these flags, including display names,
    database column names, and emoji-related checks.

    Attributes:
        _flag_names (ClassVar[list[str]]): A list of flag names, typically loaded from cached data.

    Methods:
        __int__() -> int:
            Returns the integer value of the flag.

        display_name -> str:
            A property that returns a formatted display name for the flag. The name is transformed
            to a title-cased string with underscores, and specific terms like "Ascii" are adjusted
            for proper casing.

        db_column_name -> str:
            A property that returns the lowercase version of the flag's name, suitable for use as
            a database column name.

        is_emoji_flag -> bool:
            A property that checks if the flag is related to emojis or pictographic characters.

        match_loosely(value: str) -> CharacterFilterFlag | None:
            A class method that attempts to find a flag that loosely matches the given string value.
            The matching is performed using a normalized string comparison.

        get_all_set_flags(set_flags: int) -> list[CharacterFilterFlag]:
            A class method that returns a list of all flags that are set in the given integer value.
            Flags are included if their integer value is fully contained within the set_flags value.
    """

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
