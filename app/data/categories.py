ALL_CATEGORIES = [
    {"abbreviation": "Lu", "category": "Uppercase Letter"},
    {"abbreviation": "Ll", "category": "Lowercase Letter"},
    {"abbreviation": "Lt", "category": "Titlecase Letter"},
    {"abbreviation": "LC", "category": "Cased Letter"},
    {"abbreviation": "Lm", "category": "Modifier Letter"},
    {"abbreviation": "Lo", "category": "Other Letter"},
    {"abbreviation": "L", "category": "Letter"},
    {"abbreviation": "Mn", "category": "Nonspacing Mark"},
    {"abbreviation": "Mc", "category": "Spacing Mark"},
    {"abbreviation": "Me", "category": "Enclosing Mark"},
    {"abbreviation": "M", "category": "Mark"},
    {"abbreviation": "Nd", "category": "Decimal Number"},
    {"abbreviation": "Nl", "category": "Letter Number"},
    {"abbreviation": "No", "category": "Other Number"},
    {"abbreviation": "N", "category": "Number"},
    {"abbreviation": "Pc", "category": "Connector Punctuation"},
    {"abbreviation": "Pd", "category": "Dash Punctuation"},
    {"abbreviation": "Ps", "category": "Open Punctuation"},
    {"abbreviation": "Pe", "category": "Close Punctuation"},
    {"abbreviation": "Pi", "category": "Initial Punctuation"},
    {"abbreviation": "Pf", "category": "Final Punctuation"},
    {"abbreviation": "Po", "category": "Other Punctuation"},
    {"abbreviation": "P", "category": "Punctuation"},
    {"abbreviation": "Sm", "category": "Math Symbol"},
    {"abbreviation": "Sc", "category": "Currency Symbol"},
    {"abbreviation": "Sk", "category": "Modifier Symbol"},
    {"abbreviation": "So", "category": "Other Symbol"},
    {"abbreviation": "S", "category": "Symbol"},
    {"abbreviation": "Zs", "category": "Space Separator"},
    {"abbreviation": "Zl", "category": "Line Separator"},
    {"abbreviation": "Zp", "category": "Paragraph Separator"},
    {"abbreviation": "Z", "category": "Separator"},
    {"abbreviation": "Cc", "category": "Control"},
    {"abbreviation": "Cf", "category": "Format"},
    {"abbreviation": "Cs", "category": "Surrogate"},
    {"abbreviation": "Co", "category": "Private Use"},
    {"abbreviation": "Cn", "category": "Unassigned"},
    {"abbreviation": "C", "category": "Other"},
]


def get_unicode_character_category(abbrev: str) -> str:
    found = [cat for cat in ALL_CATEGORIES if cat["abbreviation"] == abbrev]
    return found[0]["category"] if found else ""