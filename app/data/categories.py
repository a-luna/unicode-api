GENERAL_CATEGORIES = [
    {"value": "Lu", "category": "Uppercase Letter"},
    {"value": "Ll", "category": "Lowercase Letter"},
    {"value": "Lt", "category": "Titlecase Letter"},
    {"value": "LC", "category": "Cased Letter"},
    {"value": "Lm", "category": "Modifier Letter"},
    {"value": "Lo", "category": "Other Letter"},
    {"value": "L", "category": "Letter"},
    {"value": "Mn", "category": "Nonspacing Mark"},
    {"value": "Mc", "category": "Spacing Mark"},
    {"value": "Me", "category": "Enclosing Mark"},
    {"value": "M", "category": "Mark"},
    {"value": "Nd", "category": "Decimal Number"},
    {"value": "Nl", "category": "Letter Number"},
    {"value": "No", "category": "Other Number"},
    {"value": "N", "category": "Number"},
    {"value": "Pc", "category": "Connector Punctuation"},
    {"value": "Pd", "category": "Dash Punctuation"},
    {"value": "Ps", "category": "Open Punctuation"},
    {"value": "Pe", "category": "Close Punctuation"},
    {"value": "Pi", "category": "Initial Punctuation"},
    {"value": "Pf", "category": "Final Punctuation"},
    {"value": "Po", "category": "Other Punctuation"},
    {"value": "P", "category": "Punctuation"},
    {"value": "Sm", "category": "Math Symbol"},
    {"value": "Sc", "category": "Currency Symbol"},
    {"value": "Sk", "category": "Modifier Symbol"},
    {"value": "So", "category": "Other Symbol"},
    {"value": "S", "category": "Symbol"},
    {"value": "Zs", "category": "Space Separator"},
    {"value": "Zl", "category": "Line Separator"},
    {"value": "Zp", "category": "Paragraph Separator"},
    {"value": "Z", "category": "Separator"},
    {"value": "Cc", "category": "Control"},
    {"value": "Cf", "category": "Format"},
    {"value": "Cs", "category": "Surrogate"},
    {"value": "Co", "category": "Private Use"},
    {"value": "Cn", "category": "Unassigned"},
    {"value": "C", "category": "Other"},
]

BIDIRECTIONAL_CATEGORIES = [
    {"value": "L", "category": "Left To Right"},
    {"value": "R", "category": "Right To Left"},
    {"value": "AL", "category": "Arabic Letter"},
    {"value": "EN", "category": "European Number"},
    {"value": "ES", "category": "European Separator"},
    {"value": "ET", "category": "European Terminator"},
    {"value": "AN", "category": "Arabic Number"},
    {"value": "CS", "category": "Common Separator"},
    {"value": "NSM", "category": "Nonspacing Mark"},
    {"value": "BN", "category": "Boundary Neutral"},
    {"value": "B", "category": "Paragraph Separator"},
    {"value": "S", "category": "Segment Separator"},
    {"value": "WS", "category": "White Space"},
    {"value": "ON", "category": "Other Neutral"},
    {"value": "LRE", "category": "Left To Right Embedding"},
    {"value": "LRO", "category": "Left To Right Override"},
    {"value": "RLE", "category": "Right To Left Embedding"},
    {"value": "RLO", "category": "Right To Left Override"},
    {"value": "PDF", "category": "Pop Directional Format"},
    {"value": "LRI", "category": "Left To Right Isolate"},
    {"value": "RLI", "category": "Right To Left Isolate"},
    {"value": "FSI", "category": "First Strong Isolate"},
    {"value": "PDI", "category": "Pop Directional Isolate"},
]

COMBINING_CLASS_CATEGORIES = [
    {"value": 0, "category": "Not Reordered"},
    {"value": 1, "category": "Overlay"},
    {"value": 6, "category": "Han Reading"},
    {"value": 7, "category": "Nukta"},
    {"value": 8, "category": "Kana Voicing"},
    {"value": 9, "category": "Virama"},
    {"value": 200, "category": "Attached Below Left"},
    {"value": 202, "category": "Attached Below"},
    {"value": 204, "category": "Attached Below Right"},
    {"value": 208, "category": "Attached Left"},
    {"value": 210, "category": "Attached Right"},
    {"value": 212, "category": "Attached Above Left"},
    {"value": 214, "category": "Attached Above"},
    {"value": 216, "category": "Attached Above Right"},
    {"value": 218, "category": "Below Left"},
    {"value": 220, "category": "Below"},
    {"value": 222, "category": "Below Right"},
    {"value": 224, "category": "Left"},
    {"value": 226, "category": "Right"},
    {"value": 228, "category": "Above Left"},
    {"value": 230, "category": "Above"},
    {"value": 232, "category": "Above Right"},
    {"value": 233, "category": "Double Below"},
    {"value": 234, "category": "Double Above"},
    {"value": 240, "category": "Iota Subscript"},
]


def get_category(categories: list[dict[str, int | str]], value: str) -> str:
    found = [cat for cat in categories if cat["value"] == value]
    if not found:
        return ""
    category = found[0]["category"]
    value = found[0]["value"]
    return f"{category} ({value})"


def get_character_general_category(value: str) -> str:
    return get_category(GENERAL_CATEGORIES, value)


def get_character_bidirectional_category(value: str) -> str:
    return get_category(BIDIRECTIONAL_CATEGORIES, value)


def get_combining_class_category(value: int) -> str:
    return get_category(COMBINING_CLASS_CATEGORIES, value)
