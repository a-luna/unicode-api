from enum import auto

from fastapi_utils.enums import StrEnum


class CharPropertyGroup(StrEnum):

    All = auto()
    Minimum = auto()
    Basic = auto()
    UTF8 = auto()
    UTF16 = auto()
    UTF32 = auto()
    Bidirectionality = auto()
    Decomposition = auto()
    Numeric = auto()
    Joining = auto()
    Linebreak = auto()
    East_Asian_Width = auto()
    Case = auto()
    Script = auto()
    Hangul = auto()
    Indic = auto()
    Function_and_Graphic = auto()
    Emoji = auto()

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
