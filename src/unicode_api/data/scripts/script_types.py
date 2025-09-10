import unicode_api.db.models as db

AllParsedUnicodeData = tuple[
    list[db.UnicodePlane],
    list[db.UnicodeBlock],
    list[db.UnicodeCharacter],
    list[db.UnicodeCharacter],
    list[db.UnicodeCharacterUnihan],
]
CharUnicodeModel = db.UnicodeCharacter | db.UnicodeCharacterUnihan
UnicodeModel = db.UnicodePlane | db.UnicodeBlock | CharUnicodeModel
UnicodePropertyGroupType = (
    type[db.Age]
    | type[db.Bidi_Class]
    | type[db.Bidi_Paired_Bracket_Type]
    | type[db.Canonical_Combining_Class]
    | type[db.Decomposition_Type]
    | type[db.East_Asian_Width]
    | type[db.General_Category]
    | type[db.Grapheme_Cluster_Break]
    | type[db.Hangul_Syllable_Type]
    | type[db.Indic_Conjunct_Break]
    | type[db.Indic_Positional_Category]
    | type[db.Indic_Syllabic_Category]
    | type[db.Jamo_Short_Name]
    | type[db.Joining_Group]
    | type[db.Joining_Type]
    | type[db.Line_Break]
    | type[db.Numeric_Type]
    | type[db.Script]
    | type[db.Sentence_Break]
    | type[db.Vertical_Orientation]
    | type[db.Word_Break]
)
