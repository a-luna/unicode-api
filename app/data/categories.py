GENERAL_CATEGORIES = [
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

BIDIRECTIONAL_CATEGORIES = [
    {"abbreviation": "L", "category": "Left To Right"},
    {"abbreviation": "R", "category": "Right To Left"},
    {"abbreviation": "AL", "category": "Arabic Letter"},
    {"abbreviation": "EN", "category": "European Number"},
    {"abbreviation": "ES", "category": "European Separator"},
    {"abbreviation": "ET", "category": "European Terminator"},
    {"abbreviation": "AN", "category": "Arabic Number"},
    {"abbreviation": "CS", "category": "Common Separator"},
    {"abbreviation": "NSM", "category": "Nonspacing Mark"},
    {"abbreviation": "BN", "category": "Boundary Neutral"},
    {"abbreviation": "B", "category": "Paragraph Separator"},
    {"abbreviation": "S", "category": "Segment Separator"},
    {"abbreviation": "WS", "category": "White Space"},
    {"abbreviation": "ON", "category": "Other Neutral"},
    {"abbreviation": "LRE", "category": "Left To Right Embedding"},
    {"abbreviation": "LRO", "category": "Left To Right Override"},
    {"abbreviation": "RLE", "category": "Right To Left Embedding"},
    {"abbreviation": "RLO", "category": "Right To Left Override"},
    {"abbreviation": "PDF", "category": "Pop Directional Format"},
    {"abbreviation": "LRI", "category": "Left To Right Isolate"},
    {"abbreviation": "RLI", "category": "Right To Left Isolate"},
    {"abbreviation": "FSI", "category": "First Strong Isolate"},
    {"abbreviation": "PDI", "category": "Pop Directional Isolate"},
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


def get_character_general_category(abbrev: str) -> str:
    found = [cat for cat in GENERAL_CATEGORIES if cat["abbreviation"] == abbrev]
    return found[0]["category"] if found else ""


def get_character_bidirectional_category(abbrev: str) -> str:
    found = [cat for cat in BIDIRECTIONAL_CATEGORIES if cat["abbreviation"] == abbrev]
    return found[0]["category"] if found else ""


def get_combining_class_category(value: int) -> str:
    found = [cat for cat in COMBINING_CLASS_CATEGORIES if cat["value"] == value]
    return found[0]["category"] if found else ""
