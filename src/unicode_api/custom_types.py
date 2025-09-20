from typing import NotRequired, Protocol, Required, Self, TypedDict

type JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


class UnicodePropertyGroupValues(TypedDict):
    id: Required[int]
    short_name: Required[str]
    long_name: Required[str]
    is_group: NotRequired[bool]
    grouped_values: NotRequired[str]


class UnicodePropertyGroupMap(TypedDict):
    Age: dict[str, UnicodePropertyGroupValues]
    Bidi_Class: dict[str, UnicodePropertyGroupValues]
    Bidi_Paired_Bracket_Type: dict[str, UnicodePropertyGroupValues]
    Canonical_Combining_Class: dict[str, UnicodePropertyGroupValues]
    Decomposition_Type: dict[str, UnicodePropertyGroupValues]
    East_Asian_Width: dict[str, UnicodePropertyGroupValues]
    General_Category: dict[str, UnicodePropertyGroupValues]
    Grapheme_Cluster_Break: dict[str, UnicodePropertyGroupValues]
    Hangul_Syllable_Type: dict[str, UnicodePropertyGroupValues]
    Indic_Conjunct_Break: dict[str, UnicodePropertyGroupValues]
    Indic_Positional_Category: dict[str, UnicodePropertyGroupValues]
    Indic_Syllabic_Category: dict[str, UnicodePropertyGroupValues]
    Jamo_Short_Name: dict[str, UnicodePropertyGroupValues]
    Joining_Group: dict[str, UnicodePropertyGroupValues]
    Joining_Type: dict[str, UnicodePropertyGroupValues]
    Line_Break: dict[str, UnicodePropertyGroupValues]
    NFC_Quick_Check: dict[str, UnicodePropertyGroupValues]
    NFD_Quick_Check: dict[str, UnicodePropertyGroupValues]
    NFKC_Quick_Check: dict[str, UnicodePropertyGroupValues]
    NFKD_Quick_Check: dict[str, UnicodePropertyGroupValues]
    Numeric_Type: dict[str, UnicodePropertyGroupValues]
    Script: dict[str, UnicodePropertyGroupValues]
    Sentence_Break: dict[str, UnicodePropertyGroupValues]
    Vertical_Orientation: dict[str, UnicodePropertyGroupValues]
    Word_Break: dict[str, UnicodePropertyGroupValues]
    boolean_properties: list[str]
    missing_prop_groups: list[str]


class IFilterParameter(Protocol):
    id: int | None
    short_name: str
    long_name: str

    @property
    def display_name(self) -> str: ...

    @classmethod
    def from_dict(cls, model_dict: UnicodePropertyGroupValues) -> Self: ...
