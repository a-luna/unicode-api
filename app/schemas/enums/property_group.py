from enum import auto

from fastapi_utils.enums import StrEnum


class CharPropertyGroup(StrEnum):

    ALL = auto()
    BASIC = auto()
    ENCODED_STRINGS = auto()
    ENCODED_BYTES = auto()
    COMBINING = auto()
    BIDIRECTIONALITY = auto()
    DECOMPOSITION = auto()
    NUMERIC = auto()
    JOINING = auto()
    LINEBREAK = auto()
    EAST_ASIAN_WIDTH = auto()
    CASE = auto()
    SCRIPT = auto()
    HANGUL = auto()
    INDIC = auto()
    FUNCTION_AND_GRAPHIC = auto()
    EMOJI = auto()

    def __str__(self):
        return self.name.replace("_", " ").title().replace("And", "and")

    @property
    def display_name(self) -> str:
        return str(self)

    @property
    def index_name(self) -> str:
        if "_" in self.name:
            return "".join([s[0] for s in self.name.split("_") if s != "AND"]).lower()
        return self.name.lower()

    @classmethod
    def get_group_weights(cls):
        return {group.name: i for i, group in enumerate(cls, start=1)}
