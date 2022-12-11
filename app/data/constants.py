import re
from html.entities import html5

from app.schemas import (
    UnicodeBlockInternal,
    UnicodeCharacter,
    UnicodeCharacterResult,
    UnicodePlaneInternal,
)

# REGEX
CODEPOINT_REGEX = re.compile(
    r"(?:U\+(?P<codepoint_prefix>[A-Fa-f0-9]{4,6}))|(?:(0x)?(?P<codepoint>[A-Fa-f0-9]{2,6}))"
)

# MAGIC NUMBERS
MAX_CODEPOINT = 1114111

# NULL OBJECTS
NULL_PLANE = UnicodePlaneInternal(
    number=-1,
    name="Invalid Codepoint",
    abbreviation="N/A",
    start="",
    start_dec=0,
    finish="",
    finish_dec=0,
    start_block_id=0,
    finish_block_id=0,
    total_allocated=0,
    total_defined=0,
)

NULL_BLOCK = UnicodeBlockInternal(
    id=0,
    name="",
    plane="",
    start="",
    start_dec=0,
    finish="",
    finish_dec=0,
    total_allocated=0,
    total_defined=0,
)

NULL_CHARACTER_RESULT = UnicodeCharacterResult(
    character="", name="", codepoint="", link=""
)
NULL_CHARACTER = UnicodeCharacter(
    name="",
    character="",
    codepoint=0,
    codepoint_dec="",
    block="",
    plane="",
    age="",
    html_entities=[],
    uri_encoded="",
    utf8_dec_bytes=[],
    utf8_hex_bytes=[],
    utf8="",
    utf16="",
    utf32="",
    general_category="",
    combining_class=0,
    bidirectional_class="",
    bidirectional_is_mirrored=False,
    bidirectional_mirroring_glyph="",
    bidirectional_control=False,
    paired_bracket_type="",
    paired_bracket_property="",
    decomposition_type="",
    decomposition_mapping=[],
    composition_exclusion=False,
    full_composition_exclusion=False,
    numeric_type="",
    numeric_value="",
    joining_class="",
    joining_group="",
    joining_control=False,
    line_break="",
    east_asian_width="",
    uppercase=False,
    lowercase=False,
    simple_uppercase_mapping="",
    simple_lowercase_mapping="",
    simple_titlecase_mapping="",
    simple_case_folding="",
    other_uppercase=False,
    other_lowercase=False,
    other_uppercase_mapping="",
    other_lowercase_mapping="",
    other_titlecase_mapping="",
    other_case_folding="",
    script="",
    script_extension=[],
    hangul_syllable_type="",
    jamo_short_name="",
    indic_syllabic_category="",
    indic_matra_category="",
    indic_positional_category="",
    dash=False,
    hyphen=False,
    quotation_mark=False,
    terminal_punctuation=False,
    sentence_terminal=False,
    diacritic=False,
    extender=False,
    soft_dotted=False,
    alphabetic=False,
    other_alphabetic=False,
    math=False,
    other_math=False,
    hex_digit=False,
    ascii_hex_digit=False,
    default_ignorable_code_point=False,
    other_default_ignorable_code_point=False,
    logical_order_exception=False,
    prepended_concatenation_mark=False,
    white_space=False,
    vertical_orientation="",
    regional_indicator=False,
    emoji=False,
    emoji_presentation=False,
    emoji_modifier=False,
    emoji_modifier_base=False,
    emoji_component=False,
    extended_pictographic=False,
)

# HTML ENTITY MAP
HTML_ENTITY_MAP = {
    cp: entity
    for (cp, entity) in sorted(
        [
            (ord(uni_char), entity)
            for (entity, uni_char) in html5.items()
            if len(uni_char) == 1
        ],
        key=lambda x: x[0],
    )
}

# SPECIAL BLOCK NAMES
CJK_COMPATIBILITY_BLOCKS = [
    "CJK Compatibility Ideographs",
    "CJK Compatibility Ideographs Supplement",
]

TANGUT_BLOCKS = ["Tangut", "Tangut Supplement"]
VAR_SELECTOR_BLOCKS = ["Variation Selectors Supplement"]

CJK_UNIFIED_BLOCKS = [
    "CJK Unified Ideographs",
    "CJK Unified Ideographs Extension A",
    "CJK Unified Ideographs Extension B",
    "CJK Unified Ideographs Extension C",
    "CJK Unified Ideographs Extension D",
    "CJK Unified Ideographs Extension E",
    "CJK Unified Ideographs Extension F",
    "CJK Unified Ideographs Extension G",
    "CJK Unified Ideographs Extension H",
]

VIRTUAL_CHAR_BLOCKS = (
    CJK_COMPATIBILITY_BLOCKS + TANGUT_BLOCKS + VAR_SELECTOR_BLOCKS + CJK_UNIFIED_BLOCKS
)

# CHARACTER PROPERTY GROUPS
BASIC_PROPERTIES = [
    ["character", ""],
    ["name", "na"],
    ["codepoint", "cp"],            # codepoint
    ["block", ""],
    ["plane", ""],
    ["age", "age"],                 # version in which the codepoint was assigned
    ["general_category", "gc"],     # general category, see https://www.unicode.org/reports/tr44/#General_Category_Values
]

COMBINING_PROPERTIES = [
    ["combining_class", "ccc"]      # combining class, see https://www.unicode.org/reports/tr44/#Canonical_Combining_Class_Values. Specifies, with a numeric code, how a diacritic mark is positioned with respect to the base character. This is used in the Canonical Ordering Algorithm and in normalization. The order of the numbers is significant, but not the absolute values.
]

BIDIRECTIONALITY_PROPERTIES = [
    ["bidirectional_class", "bc"],          # bidirectional class, see https://www.unicode.org/reports/tr44/#Bidi_Class_Values
    ["bidirectional_is_mirrored", "Bidi_M"],              # bidirectional mirrored, boolean value
    ["bidirectional_mirroring_glyph","bmg"],              # bidirectional mirroring glyph, the codepoint of the character whose glyph is typically a mirrored image of the glyph for the current character
    ["bidirectional_control", "Bidi_C"],             # bidirectional control, indicates whether the character has a special function in the bidirectional algorithm
    ["paired_bracket_type", "bpt"],         # bidirectional paired bracket type, see https://www.unicode.org/Public/15.0.0/ucd/BidiBrackets.txt
    ["paired_bracket_property", "bpb"],     # bidirectional paired bracket property, see https://www.unicode.org/Public/15.0.0/ucd/BidiBrackets.txt
]

DECOMPOSITION_PROPERTIES = [
    ["decomposition_type", "dt"],               # decomposition type, see 
    ["decomposition_mapping", "dm"],            #
    ["composition_exclusion", "CE"],            #
    ["full_composition_exclusion", "Comp_Ex"],  #
]

NUMERIC_PROPERTIES = [
    ["numeric_type", "nt"],         #
    ["numeric_value", "nv"],        #
]

JOINING_PROPERTIES = [
    ["joining_class", "jt"],        #
    ["joining_group", "jg"],        #
    ["joining_control", "Join_C"],  #
]

LINEBREAK_PROPERTIES = [
    ["line_break", "lb"],           #
]

EAST_ASIAN_WIDTH_PROPERTIES = [
    ["east_asian_width", "ea"],     #
]

CASE_PROPERTIES = [
    ["uppercase", "Upper"],                 #
    ["lowercase", "Lower"],                 #
    ["simple_uppercase_mapping", "suc"],    #
    ["simple_lowercase_mapping", "slc"],    #
    ["simple_titlecase_mapping", "stc"],    #
    ["simple_case_folding", "scf"],         #
    ["other_uppercase", "OUpper"],          #
    ["other_lowercase", "OLower"],          #
    ["other_uppercase_mapping", "uc"],      #
    ["other_lowercase_mapping", "lc"],      #
    ["other_titlecase_mapping", "tc"],      #
    ["other_case_folding", "cf"],           #
]

SCRIPT_PROPERTIES = [
    ["script", "sc"],                   #
    ["script_extension", "scx"],        #
]

HANGUL_PROPERTIES = [
    ["hangul_syllable_type", "hst"],    #
    ["jamo_short_name", "JSN"],         #
]

INDIC_PROPERTIES = [
    ["indic_syllabic_category", "InSC"],        #
    ["indic_matra_category", "NA"],             #
    ["indic_positional_category", "InPC"],      #
]

FUNCTION_AND_GRAPHIC_PROPERTIES = [
    ["dash", "Dash"],                                   #
    ["hyphen", "Hyphen"],                               #
    ["quotation_mark", "QMark"],                        #
    ["terminal_punctuation", "Term"],                   #
    ["sentence_terminal", "STerm"],                     #
    ["diacritic", "Dia"],                               #
    ["extender", "Ext"],                                #
    ["soft_dotted", "PCM"],                             #
    ["alphabetic", "SD"],                               #
    ["other_alphabetic", "Alpha"],                      #
    ["math", "OAlpha"],                                 #
    ["other_math", "Math"],                             #
    ["hex_digit", "OMath"],                             #
    ["ascii_hex_digit", "Hex"],                         #
    ["default_ignorable_code_point", "AHex"],           #
    ["other_default_ignorable_code_point", "DI"],       #
    ["logical_order_exception", "ODI"],                 #
    ["prepended_concatenation_mark", "LOE"],            #
    ["white_space", "WSpace"],                          #
    ["vertical_orientation_value", "vo"],               #
    ["vertical_orientation", "vo"],                     #
    ["regional_indicator", "RI"],                       #
]

EMOJI_PROPERTIES = [
    ["emoji", "Emoji"],                         #
    ["emoji_presentation", "EPres"],            #
    ["emoji_modifier", "EMod"],                 #
    ["emoji_modifier_base", "EBase"],           #
    ["emoji_component", "EComp"],               #
    ["extended_pictographic", "ExtPict"],       #
]
