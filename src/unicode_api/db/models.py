from unicode_api.enums.char_filter_flags import CharacterFilterFlag
from unicode_api.enums.character_type import CharacterType
from unicode_api.enums.property_group import CharPropertyGroup
from unicode_api.enums.triadic_logic import TriadicLogic
from unicode_api.models.block import UnicodeBlock, UnicodeBlockResponse, UnicodeBlockResult
from unicode_api.models.character import (
    UnicodeCharacter,
    UnicodeCharacterBase,
    UnicodeCharacterResponse,
    UnicodeCharacterResult,
    UnicodeCharacterUnihan,
)
from unicode_api.models.pagination import PaginatedList, PaginatedSearchResults, UserFilterSettings
from unicode_api.models.plane import UnicodePlane, UnicodePlaneResponse
from unicode_api.models.property_values import (
    Age,
    Bidi_Class,
    Bidi_Paired_Bracket_Type,
    Canonical_Combining_Class,
    Decomposition_Type,
    East_Asian_Width,
    General_Category,
    Grapheme_Cluster_Break,
    Hangul_Syllable_Type,
    Indic_Conjunct_Break,
    Indic_Positional_Category,
    Indic_Syllabic_Category,
    Jamo_Short_Name,
    Joining_Group,
    Joining_Type,
    Line_Break,
    Numeric_Type,
    Script,
    Sentence_Break,
    Vertical_Orientation,
    Word_Break,
)

CHAR_TABLES = [UnicodeCharacter, UnicodeCharacterUnihan]

type DatabaseCharacterProperty = (
    UnicodeBlock
    | General_Category
    | Age
    | Script
    | Bidi_Class
    | Decomposition_Type
    | Line_Break
    | Canonical_Combining_Class
    | Numeric_Type
    | Joining_Type
)
type CharacterProperty = DatabaseCharacterProperty | CharacterFilterFlag | CharPropertyGroup

__all__ = [
    "CharacterFilterFlag",
    "CharacterProperty",
    "CharacterType",
    "DatabaseCharacterProperty",
    "TriadicLogic",
    "UnicodeBlock",
    "UnicodeBlockResponse",
    "UnicodeBlockResult",
    "UnicodeCharacter",
    "UnicodeCharacterBase",
    "UnicodeCharacterResponse",
    "UnicodeCharacterResult",
    "UnicodeCharacterUnihan",
    "PaginatedList",
    "PaginatedSearchResults",
    "UserFilterSettings",
    "UnicodePlane",
    "UnicodePlaneResponse",
    "CharPropertyGroup",
    "Age",
    "Bidi_Class",
    "Bidi_Paired_Bracket_Type",
    "Canonical_Combining_Class",
    "Decomposition_Type",
    "East_Asian_Width",
    "General_Category",
    "Grapheme_Cluster_Break",
    "Hangul_Syllable_Type",
    "Indic_Conjunct_Break",
    "Indic_Positional_Category",
    "Indic_Syllabic_Category",
    "Jamo_Short_Name",
    "Joining_Group",
    "Joining_Type",
    "Line_Break",
    "Numeric_Type",
    "Script",
    "Sentence_Break",
    "Vertical_Orientation",
    "Word_Break",
]
