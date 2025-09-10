from enum import IntEnum, auto


class CharacterType(IntEnum):
    """
    An enumeration representing various types of Unicode characters.

    Attributes:
        NON_UNIHAN (int): Represents a character that is not part of the Unihan database.
        UNIHAN (int): Represents a character that is part of the Unihan database.
        TANGUT (int): Represents a Tangut character.
        NONCHARACTER (int): Represents a noncharacter code point.
        SURROGATE (int): Represents a surrogate code point.
        PRIVATE_USE (int): Represents a private-use code point.
        RESERVED (int): Represents a code point that is within the Unicode space but is not assigned to any character.
        INVALID (int): Represents a code point that is not in the Unicode space.

    Methods:
        __str__(): Returns the name of the enumeration member in lowercase with underscores replaced by hyphens.
    """

    NON_UNIHAN = auto()
    UNIHAN = auto()
    TANGUT = auto()
    NONCHARACTER = auto()
    SURROGATE = auto()
    PRIVATE_USE = auto()
    RESERVED = auto()
    INVALID = auto()

    def __str__(self):
        return self.name.replace("_", "-").lower()
