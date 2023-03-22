from enum import auto, IntEnum


class UnassignedCharacterType(IntEnum):
    NONCHARACTER = auto()
    SURROGATE = auto()
    PRIVATE_USE = auto()
    RESERVED = auto()
    INVALID = auto()

    def __str__(self):
        return self.name.replace("_", "-").lower()
