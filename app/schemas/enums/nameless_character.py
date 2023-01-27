from enum import auto, IntEnum


class NamelessCharacterType(IntEnum):

    NONCHARACTER = auto()
    SURROGATE = auto()
    PRIVATE_USE = auto()
    RESERVED = auto()

    def __str__(self):
        return self.name.replace("_", "-").lower()

    @property
    def display_name(self) -> str:
        return str(self)
