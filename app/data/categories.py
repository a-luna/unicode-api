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

BIDI_BRACKET_TYPES = [
    {"value": "o", "category": "Open"},
    {"value": "c", "category": "Close"},
    {"value": "n", "category": "None"},
]

DECOMPOSITION_TYPES = [
    {"value": "none", "category": "None"},
    {"value": "can", "category": "Canonical"},
    {"value": "com", "category": "Otherwise unspecified compatibility character"},
    {"value": "enc", "category": "Encircled form"},
    {"value": "fin", "category": "Final presentation form (Arabic)"},
    {"value": "font", "category": "Font variant"},
    {"value": "fra", "category": "Vulgar fraction form"},
    {"value": "init", "category": "Initial presentation form (Arabic)"},
    {"value": "iso", "category": "Isolated presentation form (Arabic)"},
    {"value": "med", "category": "Medial presentation form (Arabic)"},
    {"value": "nar", "category": "Narrow (or hankaku) compatibility character"},
    {"value": "nb", "category": "No No-break version of a space or hyphen"},
    {"value": "sml", "category": "Small variant form (CNS compatibility)"},
    {"value": "sqr", "category": "CJK squared font variant"},
    {"value": "sub", "category": "Subscript form"},
    {"value": "sup", "category": "Superscript form"},
    {"value": "vert", "category": "Vertical layout presentation form"},
    {"value": "wide", "category": "Wide (or zenkaku) compatibility character"},
]

NUMERIC_TYPES = [
    {"value": "None", "category": "None"},
    {"value": "De", "category": "Decimal"},
    {"value": "Di", "category": "Digit"},
    {"value": "Nu", "category": "Numeric"},
]

JOINING_TYPES = [
    {"value": "R", "category": "Right Joining"},
    {"value": "L", "category": "Left Joining"},
    {"value": "D", "category": "Dual Joining"},
    {"value": "C", "category": "Join Causing"},
    {"value": "U", "category": "Non-Joining"},
    {"value": "T", "category": "Transparent"},
]

LINE_BREAK_TYPES = [
    {"value": "AI", "category": "Ambiguous (Alphabetic or Ideographic)"},
    {"value": "AL", "category": "Ordinary Alphabetic and Symbol"},
    {"value": "B2", "category": "Break Opportunity Before and After"},
    {"value": "BA", "category": "Break Opportunity After"},
    {"value": "BB", "category": "Break Opportunity Before"},
    {"value": "BK", "category": "Mandatory Break"},
    {"value": "CB", "category": "Contingent Break Opportunity"},
    {"value": "CL", "category": "Closing Punctuation"},
    {"value": "CM", "category": "Attached Characters and Combining Marks"},
    {"value": "CR", "category": "Carriage Return"},
    {"value": "EX", "category": "Exclamation/Interrogation"},
    {"value": "GL", "category": 'Non-breaking ("Glue")'},
    {"value": "H2", "category": "Hangul LV Syllable"},
    {"value": "H3", "category": "Hangul LVT Syllable"},
    {"value": "HY", "category": "Hyphen"},
    {"value": "ID", "category": "Ideographic"},
    {"value": "IN", "category": "Inseparable"},
    {"value": "IS", "category": "Infix Separator"},
    {"value": "JL", "category": "Hangul L Jamo"},
    {"value": "JT", "category": "Hangul T Jamo"},
    {"value": "JV", "category": "Hangul V Jamo"},
    {"value": "LF", "category": "Line Feed"},
    {"value": "NL", "category": "Next Line"},
    {"value": "NS", "category": "Non Starter"},
    {"value": "NU", "category": "Numeric"},
    {"value": "OP", "category": "Opening Punctuation"},
    {"value": "PO", "category": "Postfix (Numeric)"},
    {"value": "PR", "category": "Prefix (Numeric)"},
    {"value": "QU", "category": "Ambiguous Quotation"},
    {"value": "SA", "category": "Complex Context (South East Asian)"},
    {"value": "SG", "category": "Surrogates"},
    {"value": "SP", "category": "Space"},
    {"value": "SY", "category": "Symbols Allowing Breaks"},
    {"value": "WJ", "category": "Word Joiner"},
    {"value": "XX", "category": "Unknown"},
    {"value": "ZW", "category": "Zero Width Space"},
]

EAST_ASIAN_WIDTH_TYPES = [
    {"value": "A", "category": "East Asian Ambiguous"},
    {"value": "F", "category": "East Asian Fullwidth"},
    {"value": "H", "category": "East Asian Halfwidth"},
    {"value": "N", "category": "Neutral (Not East Asian)"},
    {"value": "Na", "category": "East Asian Narrow"},
    {"value": "W", "category": "East Asian Wide"},
]

SCRIPT_CODES = [
    {"value": "Adlm", "category": "Adlam"},
    {"value": "Ahom", "category": "Ahom"},
    {"value": "Hluw", "category": "Anatolian Hieroglyphs"},
    {"value": "Arab", "category": "Arabic"},
    {"value": "Armn", "category": "Armenian"},
    {"value": "Avst", "category": "Avestan"},
    {"value": "Bali", "category": "Balinese"},
    {"value": "Bamu", "category": "Bamum"},
    {"value": "Bass", "category": "Bassa Vah"},
    {"value": "Batk", "category": "Batak"},
    {"value": "Beng", "category": "Bengali"},
    {"value": "Bhks", "category": "Bhaiksuki"},
    {"value": "Bopo", "category": "Bopomofo"},
    {"value": "Brah", "category": "Brahmi"},
    {"value": "Brai", "category": "Braille"},
    {"value": "Bugi", "category": "Buginese"},
    {"value": "Buhd", "category": "Buhid"},
    {"value": "Cans", "category": "Canadian Aboriginal"},
    {"value": "Cari", "category": "Carian"},
    {"value": "Aghb", "category": "Caucasian Albanian"},
    {"value": "Cakm", "category": "Chakma"},
    {"value": "Cham", "category": "Cham"},
    {"value": "Cher", "category": "Cherokee"},
    {"value": "Chrs", "category": "Chorasmian"},
    {"value": "Zyyy", "category": "Common"},
    {"value": "Copt", "category": "Coptic"},
    {"value": "Xsux", "category": "Cuneiform"},
    {"value": "Cprt", "category": "Cypriot"},
    {"value": "Cpmn", "category": "Cypro Minoan"},
    {"value": "Cyrl", "category": "Cyrillic"},
    {"value": "Dsrt", "category": "Deseret"},
    {"value": "Deva", "category": "Devanagari"},
    {"value": "Diak", "category": "Dives Akuru"},
    {"value": "Dogr", "category": "Dogra"},
    {"value": "Dupl", "category": "Duployan"},
    {"value": "Egyp", "category": "Egyptian Hieroglyphs"},
    {"value": "Elba", "category": "Elbasan"},
    {"value": "Elym", "category": "Elymaic"},
    {"value": "Ethi", "category": "Ethiopic"},
    {"value": "Geok", "category": "Georgian"},
    {"value": "Geor", "category": "Georgian"},
    {"value": "Glag", "category": "Glagolitic"},
    {"value": "Goth", "category": "Gothic"},
    {"value": "Gran", "category": "Grantha"},
    {"value": "Grek", "category": "Greek"},
    {"value": "Gujr", "category": "Gujarati"},
    {"value": "Gong", "category": "Gunjala Gondi"},
    {"value": "Guru", "category": "Gurmukhi"},
    {"value": "Hani", "category": "Han"},
    {"value": "Hang", "category": "Hangul"},
    {"value": "Rohg", "category": "Hanifi Rohingya"},
    {"value": "Hano", "category": "Hanunoo"},
    {"value": "Hatr", "category": "Hatran"},
    {"value": "Hebr", "category": "Hebrew"},
    {"value": "Hira", "category": "Hiragana"},
    {"value": "Armi", "category": "Imperial Aramaic"},
    {"value": "Zinh", "category": "Inherited"},
    {"value": "Phli", "category": "Inscriptional Pahlavi"},
    {"value": "Prti", "category": "Inscriptional Parthian"},
    {"value": "Java", "category": "Javanese"},
    {"value": "Kthi", "category": "Kaithi"},
    {"value": "Knda", "category": "Kannada"},
    {"value": "Kana", "category": "Katakana"},
    {"value": "Hrkt", "category": "Katakana or Hiragana"},
    {"value": "Kawi", "category": "Kawi"},
    {"value": "Kali", "category": "Kayah Li"},
    {"value": "Khar", "category": "Kharoshthi"},
    {"value": "Kits", "category": "Khitan Small Script"},
    {"value": "Khmr", "category": "Khmer"},
    {"value": "Khoj", "category": "Khojki"},
    {"value": "Sind", "category": "Khudawadi"},
    {"value": "Laoo", "category": "Lao"},
    {"value": "Latn", "category": "Latin"},
    {"value": "Lepc", "category": "Lepcha"},
    {"value": "Limb", "category": "Limbu"},
    {"value": "Lina", "category": "Linear A"},
    {"value": "Linb", "category": "Linear B"},
    {"value": "Lisu", "category": "Lisu"},
    {"value": "Lyci", "category": "Lycian"},
    {"value": "Lydi", "category": "Lydian"},
    {"value": "Mahj", "category": "Mahajani"},
    {"value": "Maka", "category": "Makasar"},
    {"value": "Mlym", "category": "Malayalam"},
    {"value": "Mand", "category": "Mandaic"},
    {"value": "Mani", "category": "Manichaean"},
    {"value": "Marc", "category": "Marchen"},
    {"value": "Gonm", "category": "Masaram Gondi"},
    {"value": "Medf", "category": "Medefaidrin"},
    {"value": "Mtei", "category": "Meetei Mayek"},
    {"value": "Mend", "category": "Mende Kikakui"},
    {"value": "Merc", "category": "Meroitic Cursive"},
    {"value": "Mero", "category": "Meroitic Hieroglyphs"},
    {"value": "Plrd", "category": "Miao"},
    {"value": "Modi", "category": "Modi"},
    {"value": "Mong", "category": "Mongolian"},
    {"value": "Mroo", "category": "Mro"},
    {"value": "Mult", "category": "Multani"},
    {"value": "Mymr", "category": "Myanmar"},
    {"value": "Nbat", "category": "Nabataean"},
    {"value": "Nagm", "category": "Nag Mundari"},
    {"value": "Nand", "category": "Nandinagari"},
    {"value": "Talu", "category": "New Tai Lue"},
    {"value": "Newa", "category": "Newa"},
    {"value": "Nkoo", "category": "NKo"},
    {"value": "Nshu", "category": "Nushu"},
    {"value": "Hmnp", "category": "Nyiakeng Puachue Hmong"},
    {"value": "Ogam", "category": "Ogham"},
    {"value": "Olck", "category": "Ol Chiki"},
    {"value": "Hung", "category": "Old Hungarian"},
    {"value": "Ital", "category": "Old Italic"},
    {"value": "Narb", "category": "Old North Arabian"},
    {"value": "Perm", "category": "Old Permic"},
    {"value": "Xpeo", "category": "Old Persian"},
    {"value": "Sogo", "category": "Old Sogdian"},
    {"value": "Sarb", "category": "Old South Arabian"},
    {"value": "Orkh", "category": "Old Turkic"},
    {"value": "Ougr", "category": "Old Uyghur"},
    {"value": "Orya", "category": "Oriya"},
    {"value": "Osge", "category": "Osage"},
    {"value": "Osma", "category": "Osmanya"},
    {"value": "Hmng", "category": "Pahawh Hmong"},
    {"value": "Palm", "category": "Palmyrene"},
    {"value": "Pauc", "category": "Pau Cin Hau"},
    {"value": "Phag", "category": "Phags-pa"},
    {"value": "Phnx", "category": "Phoenician"},
    {"value": "Phlp", "category": "Psalter Pahlavi"},
    {"value": "Rjng", "category": "Rejang"},
    {"value": "Runr", "category": "Runic"},
    {"value": "Samr", "category": "Samaritan"},
    {"value": "Saur", "category": "Saurashtra"},
    {"value": "Shrd", "category": "Sharada"},
    {"value": "Shaw", "category": "Shavian"},
    {"value": "Sidd", "category": "Siddham"},
    {"value": "Sgnw", "category": "SignWriting"},
    {"value": "Sinh", "category": "Sinhala"},
    {"value": "Sogd", "category": "Sogdian"},
    {"value": "Sora", "category": "Sora Sompeng"},
    {"value": "Soyo", "category": "Soyombo"},
    {"value": "Sund", "category": "Sundanese"},
    {"value": "Sylo", "category": "Syloti Nagri"},
    {"value": "Syrc", "category": "Syriac"},
    {"value": "Tglg", "category": "Tagalog"},
    {"value": "Tagb", "category": "Tagbanwa"},
    {"value": "Tale", "category": "Tai Le"},
    {"value": "Lana", "category": "Tai Tham"},
    {"value": "Tavt", "category": "Tai Viet"},
    {"value": "Takr", "category": "Takri"},
    {"value": "Taml", "category": "Tamil"},
    {"value": "Tnsa", "category": "Tangsa"},
    {"value": "Tang", "category": "Tangut"},
    {"value": "Telu", "category": "Telugu"},
    {"value": "Thaa", "category": "Thaana"},
    {"value": "Thai", "category": "Thai"},
    {"value": "Tibt", "category": "Tibetan"},
    {"value": "Tfng", "category": "Tifinagh"},
    {"value": "Tirh", "category": "Tirhuta"},
    {"value": "Toto", "category": "Toto"},
    {"value": "Ugar", "category": "Ugaritic"},
    {"value": "Zzzz", "category": "Unknown"},
    {"value": "Vaii", "category": "Vai"},
    {"value": "Vith", "category": "Vithkuqi"},
    {"value": "Wcho", "category": "Wancho"},
    {"value": "Wara", "category": "Warang Citi"},
    {"value": "Yezi", "category": "Yezidi"},
    {"value": "Yiii", "category": "Yi"},
    {"value": "Zanb", "category": "Zanabazar Square"},
]

HANGUL_SYLLABLE_TYPES = [
    {"value": "NA", "category": "Not Applicable"},
    {"value": "L", "category": "Leading Jamo"},
    {"value": "V", "category": "Vowel Jamo"},
    {"value": "T", "category": "Trailing Jamo"},
    {"value": "LV", "category": "LV Syllable"},
    {"value": "LVT", "category": "LVT Syllable"},
]

VERTICAL_ORIENTATION_TYPES = [
    {"value": "U", "category": "Upright"},
    {"value": "R", "category": "Rotated 90 degrees clockwise"},
    {
        "value": "Tu",
        "category": "Transformed typographically, with fallback to Upright",
    },
    {
        "value": "Tr",
        "category": "Transformed typographically, with fallback to Rotated",
    },
]


def get_category(categories: list[dict[str, int | str]], value: str) -> str:
    found = [cat for cat in categories if cat["value"] == value]
    if not found:
        return ""
    category = found[0]["category"]
    value = found[0]["value"]
    return f"{category} ({value})"


def get_general_category(value: str) -> str:
    return get_category(GENERAL_CATEGORIES, value)


def get_bidirectional_category(value: str) -> str:
    return get_category(BIDIRECTIONAL_CATEGORIES, value)


def get_combining_class_category(value: int) -> str:
    return get_category(COMBINING_CLASS_CATEGORIES, value)


def get_bidi_bracket_type(value: str) -> str:
    return get_category(BIDI_BRACKET_TYPES, value)


def get_decomposition_type(value: str) -> str:
    return get_category(DECOMPOSITION_TYPES, value)


def get_numeric_type(value: str) -> str:
    return get_category(NUMERIC_TYPES, value)


def get_joining_type(value: str) -> str:
    return get_category(JOINING_TYPES, value)


def get_line_break_type(value: str) -> str:
    return get_category(LINE_BREAK_TYPES, value)


def get_east_asian_width_type(value: str) -> str:
    return get_category(EAST_ASIAN_WIDTH_TYPES, value)


def get_script_code_value(value: str) -> str:
    return get_category(SCRIPT_CODES, value)


def get_script_ext_code_values(ext_list: str) -> str:
    return [get_script_code_value(code) for code in ext_list.split(" ")]


def get_hangle_syllable_type(value: str) -> str:
    return get_category(HANGUL_SYLLABLE_TYPES, value)


def get_indic_property_value(value: str) -> str:
    return value.replace("_", " ")


def get_vertical_orientation_type(value: str) -> str:
    return get_category(VERTICAL_ORIENTATION_TYPES, value)
