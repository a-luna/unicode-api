from sqlalchemy import Column, Integer
from sqlalchemy_utils import ChoiceType
from sqlmodel import Field, Relationship

from app.data.encoding import (
    get_html_entities,
    get_uri_encoded_value,
    get_utf16_dec_bytes,
    get_utf16_hex_bytes,
    get_utf16_value,
    get_utf32_dec_bytes,
    get_utf32_hex_bytes,
    get_utf32_value,
    get_utf8_dec_bytes,
    get_utf8_hex_bytes,
    get_utf8_value,
)
from app.models.enums import CharPropertyGroup
from app.models.enums import (
    GeneralCategory,
    CombiningClassCategory,
    BidirectionalClass,
    BidirectionalBracketType,
    DecompositionType,
    NumericType,
    JoiningClass,
    LineBreakType,
    EastAsianWidthType,
    ScriptCode,
    HangulSyllableType,
    VerticalOrientationType,
)
from app.schemas.camel_model import CamelModel

import snoop


class UnicodeCharacterBase(CamelModel):
    name: str = Field(index=True)
    codepoint: str = Field(index=True)
    codepoint_dec: int = Field(index=True)
    plane_number: int
    age: str
    general_category: GeneralCategory = Field(
        sa_column=Column(ChoiceType(GeneralCategory, impl=Integer()), nullable=False)
    )
    combining_class: CombiningClassCategory = Field(
        sa_column=Column(ChoiceType(CombiningClassCategory, impl=Integer()), nullable=False)
    )
    bidirectional_class: BidirectionalClass = Field(
        sa_column=Column(ChoiceType(BidirectionalClass, impl=Integer()), nullable=False)
    )
    bidirectional_is_mirrored: bool
    bidirectional_mirroring_glyph: str
    bidirectional_control: bool
    paired_bracket_type: BidirectionalBracketType = Field(
        sa_column=Column(ChoiceType(BidirectionalBracketType, impl=Integer()), nullable=False)
    )
    paired_bracket_property: str
    decomposition_type: DecompositionType = Field(
        sa_column=Column(ChoiceType(DecompositionType, impl=Integer()), nullable=False)
    )
    decomposition_mapping: str
    composition_exclusion: bool
    full_composition_exclusion: bool
    numeric_type: NumericType = Field(sa_column=Column(ChoiceType(NumericType, impl=Integer()), nullable=False))
    numeric_value: str
    numeric_value_parsed: float | None
    joining_class: JoiningClass = Field(sa_column=Column(ChoiceType(JoiningClass, impl=Integer()), nullable=False))
    joining_group: str
    joining_control: bool
    line_break: LineBreakType = Field(sa_column=Column(ChoiceType(LineBreakType, impl=Integer()), nullable=False))
    east_asian_width: EastAsianWidthType = Field(
        sa_column=Column(ChoiceType(EastAsianWidthType, impl=Integer()), nullable=False)
    )
    uppercase: bool
    lowercase: bool
    simple_uppercase_mapping: str
    simple_lowercase_mapping: str
    simple_titlecase_mapping: str
    simple_case_folding: str
    other_uppercase: bool
    other_lowercase: bool
    other_uppercase_mapping: str
    other_lowercase_mapping: str
    other_titlecase_mapping: str
    other_case_folding: str
    script: ScriptCode = Field(sa_column=Column(ChoiceType(ScriptCode, impl=Integer()), nullable=False))
    script_extension: str
    hangul_syllable_type: HangulSyllableType = Field(
        sa_column=Column(ChoiceType(HangulSyllableType, impl=Integer()), nullable=False)
    )
    jamo_short_name: str
    indic_syllabic_category: str
    indic_matra_category: str
    indic_positional_category: str
    dash: bool
    hyphen: bool
    quotation_mark: bool
    terminal_punctuation: bool
    sentence_terminal: bool
    diacritic: bool
    extender: bool
    soft_dotted: bool
    alphabetic: bool
    other_alphabetic: bool
    math: bool
    other_math: bool
    hex_digit: bool
    ascii_hex_digit: bool
    default_ignorable_code_point: bool
    other_default_ignorable_code_point: bool
    logical_order_exception: bool
    prepended_concatenation_mark: bool
    white_space: bool
    vertical_orientation: VerticalOrientationType = Field(
        sa_column=Column(ChoiceType(VerticalOrientationType, impl=Integer()), nullable=False)
    )
    regional_indicator: bool
    emoji: bool
    emoji_presentation: bool
    emoji_modifier: bool
    emoji_modifier_base: bool
    emoji_component: bool
    extended_pictographic: bool

    block_id: int = Field(foreign_key="block.id")
    plane_id: int = Field(foreign_key="plane.id")


class UnicodeCharacterResponse(CamelModel):
    character: str | None
    name: str | None
    codepoint: str | None
    block: str | None
    plane: str | None
    age: str | None
    general_category: str | None
    combining_class: str | None
    bidirectional_class: str | None
    bidirectional_is_mirrored: bool | None
    bidirectional_mirroring_glyph: str | None
    bidirectional_control: bool | None
    paired_bracket_type: str | None
    paired_bracket_property: str | None
    decomposition_type: str | None
    decomposition_mapping: list[str] | None
    composition_exclusion: bool | None
    full_composition_exclusion: bool | None
    numeric_type: str | None
    numeric_value: str | None
    numeric_value_parsed: float | None
    joining_class: str | None
    joining_group: str | None
    joining_control: bool | None
    line_break: str | None
    east_asian_width: str | None
    uppercase: bool | None
    lowercase: bool | None
    simple_uppercase_mapping: str | None
    simple_lowercase_mapping: str | None
    simple_titlecase_mapping: str | None
    simple_case_folding: str | None
    other_uppercase: bool | None
    other_lowercase: bool | None
    other_uppercase_mapping: str | None
    other_lowercase_mapping: str | None
    other_titlecase_mapping: str | None
    other_case_folding: str | None
    script: str | None
    script_extension: list[str] | None
    hangul_syllable_type: str | None
    jamo_short_name: str | None
    indic_syllabic_category: str | None
    indic_matra_category: str | None
    indic_positional_category: str | None
    dash: bool | None
    hyphen: bool | None
    quotation_mark: bool | None
    terminal_punctuation: bool | None
    sentence_terminal: bool | None
    diacritic: bool | None
    extender: bool | None
    soft_dotted: bool | None
    alphabetic: bool | None
    other_alphabetic: bool | None
    math: bool | None
    other_math: bool | None
    hex_digit: bool | None
    ascii_hex_digit: bool | None
    default_ignorable_code_point: bool | None
    other_default_ignorable_code_point: bool | None
    logical_order_exception: bool | None
    prepended_concatenation_mark: bool | None
    white_space: bool | None
    vertical_orientation: str | None
    regional_indicator: bool | None
    emoji: bool | None
    emoji_presentation: bool | None
    emoji_modifier: bool | None
    emoji_modifier_base: bool | None
    emoji_component: bool | None
    extended_pictographic: bool | None
    utf8: str | None
    utf16: str | None
    utf32: str | None
    uri_encoded: str | None
    html_entities: list[str] | None
    utf8_bytes: list[str] | None
    utf16_bytes: list[str] | None
    utf32_bytes: list[str] | None


class UnicodeCharacter(UnicodeCharacterBase, table=True):

    __tablename__ = "character"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)

    block: "UnicodeBlock" = Relationship(back_populates="characters")  # type: ignore
    plane: "UnicodePlane" = Relationship(back_populates="characters")  # type: ignore

    @classmethod
    def responsify(
        cls, char: "UnicodeCharacter", prop_groups: list[CharPropertyGroup] = [CharPropertyGroup.BASIC]
    ) -> "UnicodeCharacterResponse":
        char_dict = update_all_char_properties(char)
        response_dict = {}
        if CharPropertyGroup.BASIC not in prop_groups:
            prop_groups = [CharPropertyGroup.BASIC] + prop_groups
        if CharPropertyGroup.ALL in prop_groups:
            prop_groups = [group for group in CharPropertyGroup if group != CharPropertyGroup.ALL]
        for group in prop_groups:
            prop_group = get_all_properties_in_group(char_dict, group)
            response_dict = response_dict | prop_group
        response_dict = prune_superfluous_properties(char, response_dict, prop_groups)
        return UnicodeCharacterResponse(**response_dict)


class UnicodeCharacterResult(CamelModel):
    character: str
    name: str
    codepoint: str
    score: float | None
    link: str

    def __str__(self):
        return (
            "UnicodeCharacterResult<"
            f"score={self.score}, "
            f"character={self.character}, "
            f"name={self.name}, "
            f"codepoint={self.codepoint}"
            ">"
        )


CHARACTER_PROPERTY_GROUPS = {
    CharPropertyGroup.BASIC: [
        ["character", ""],
        ["name", "na"],
        ["codepoint", "cp"],  # codepoint
        ["block", ""],
        ["plane", ""],
        ["age", "age"],  # version in which the codepoint was assigned
        [
            "generalCategory",
            "gc",
        ],  # general category, see https://www.unicode.org/reports/tr44/#General_Category_Values
    ],
    CharPropertyGroup.COMBINING: [
        [
            "combiningClass",
            "ccc",
        ]  # combining class, see https://www.unicode.org/reports/tr44/#Canonical_Combining_Class_Values. Specifies, with a numeric code, how a diacritic mark is positioned with respect to the base character. This is used in the Canonical Ordering Algorithm and in normalization. The order of the numbers is significant, but not the absolute values.
    ],
    CharPropertyGroup.BIDIRECTIONALITY: [
        [
            "bidirectionalClass",
            "bc",
        ],  # bidirectional class, see https://www.unicode.org/reports/tr44/#Bidi_Class_Values
        ["bidirectionalIsMirrored", "Bidi_M"],  # bidirectional mirrored, boolean value
        [
            "bidirectionalMirroringGlyph",
            "bmg",
        ],  # bidirectional mirroring glyph, the codepoint of the character whose glyph is typically a mirrored image of the glyph for the current character
        [
            "bidirectionalControl",
            "Bidi_C",
        ],  # bidirectional control, indicates whether the character has a special function in the bidirectional algorithm
        [
            "pairedBracketType",
            "bpt",
        ],  # bidirectional paired bracket type, see https://www.unicode.org/Public/15.0.0/ucd/BidiBrackets.txt
        [
            "pairedBracketProperty",
            "bpb",
        ],  # bidirectional paired bracket property, see https://www.unicode.org/Public/15.0.0/ucd/BidiBrackets.txt
    ],
    CharPropertyGroup.DECOMPOSITION: [
        ["decompositionType", "dt"],  # decomposition type, see
        ["decompositionMapping", "dm"],  #
        ["compositionExclusion", "CE"],  #
        ["fullCompositionExclusion", "Comp_Ex"],  #
    ],
    CharPropertyGroup.NUMERIC: [
        ["numericType", "nt"],  #
        ["numericValue", "nv"],  #
        ["numericValueParsed", ""],  #
    ],
    CharPropertyGroup.JOINING: [
        ["joiningClass", "jt"],  #
        ["joiningGroup", "jg"],  #
        ["joiningControl", "Join_C"],  #
    ],
    CharPropertyGroup.LINEBREAK: [
        ["lineBreak", "lb"],  #
    ],
    CharPropertyGroup.EAST_ASIAN_WIDTH: [
        ["eastAsianWidth", "ea"],  #
    ],
    CharPropertyGroup.CASE: [
        ["uppercase", "Upper"],  #
        ["lowercase", "Lower"],  #
        ["simpleUppercaseMapping", "suc"],  #
        ["simpleLowercaseMapping", "slc"],  #
        ["simpleTitlecaseMapping", "stc"],  #
        ["simpleCaseFolding", "scf"],  #
        ["otherUppercase", "OUpper"],  #
        ["otherLowercase", "OLower"],  #
        ["otherUppercaseMapping", "uc"],  #
        ["otherLowercaseMapping", "lc"],  #
        ["otherTitlecaseMapping", "tc"],  #
        ["otherCaseFolding", "cf"],  #
    ],
    CharPropertyGroup.SCRIPT: [
        ["script", "sc"],  #
        ["scriptExtension", "scx"],  #
    ],
    CharPropertyGroup.HANGUL: [
        ["hangulSyllableType", "hst"],  #
        ["jamoShortName", "JSN"],  #
    ],
    CharPropertyGroup.INDIC: [
        ["indicSyllabicCategory", "InSC"],  #
        ["indicMatraCategory", "NA"],  #
        ["indicPositionalCategory", "InPC"],  #
    ],
    CharPropertyGroup.FUNCTION_AND_GRAPHIC: [
        ["dash", "Dash"],  #
        ["hyphen", "Hyphen"],  #
        ["quotationMark", "QMark"],  #
        ["terminalPunctuation", "Term"],  #
        ["sentenceTerminal", "STerm"],  #
        ["diacritic", "Dia"],  #
        ["extender", "Ext"],  #
        ["softDotted", "PCM"],  #
        ["alphabetic", "SD"],  #
        ["otherAlphabetic", "Alpha"],  #
        ["math", "OAlpha"],  #
        ["otherMath", "Math"],  #
        ["hexDigit", "OMath"],  #
        ["asciiHexDigit", "Hex"],  #
        ["defaultIgnorableCodePoint", "AHex"],  #
        ["otherDefaultIgnorableCodePoint", "DI"],  #
        ["logicalOrderException", "ODI"],  #
        ["prependedConcatenationMark", "LOE"],  #
        ["whiteSpace", "WSpace"],  #
        ["verticalOrientation", "vo"],  #
        ["regionalIndicator", "RI"],  #
    ],
    CharPropertyGroup.EMOJI: [
        ["emoji", "Emoji"],  #
        ["emojiPresentation", "EPres"],  #
        ["emojiModifier", "EMod"],  #
        ["emojiModifierBase", "EBase"],  #
        ["emojiComponent", "EComp"],  #
        ["extendedPictographic", "ExtPict"],  #
    ],
    CharPropertyGroup.ENCODED_STRINGS: [
        ["utf8", ""],
        ["utf16", ""],
        ["utf32", ""],
        ["uriEncoded", ""],
        ["htmlEntities", ""],
    ],
    CharPropertyGroup.ENCODED_BYTES: [
        ["utf8Bytes", ""],
        ["utf16Bytes", ""],
        ["utf32Bytes", ""],
    ],
}


def update_all_char_properties(char: UnicodeCharacter) -> dict[str, bool | int | str | list[int] | list[str]]:
    char_dict = char.dict(by_alias=True)
    char_dict["character"] = chr(char.codepoint_dec)
    char_dict["block"] = char.block.name
    char_dict["plane"] = char.plane.abbreviation
    char_dict["generalCategory"] = char.general_category.display_name
    char_dict["combiningClass"] = char.combining_class.display_name
    char_dict["bidirectionalClass"] = char.bidirectional_class.display_name
    char_dict["pairedBracketType"] = char.paired_bracket_type.display_name
    char_dict["decompositionType"] = char.decomposition_type.display_name
    char_dict["decompositionMapping"] = get_decomposition_mapping(char.decomposition_mapping)
    char_dict["numericType"] = char.numeric_type.display_name
    char_dict["joiningClass"] = char.joining_class.display_name
    char_dict["lineBreak"] = char.line_break.display_name
    char_dict["eastAsianWidth"] = char.east_asian_width.display_name
    char_dict["script"] = char.script.display_name
    char_dict["scriptExtension"] = get_script_extension(char.script_extension)
    char_dict["hangulSyllableType"] = char.hangul_syllable_type.display_name
    char_dict["verticalOrientation"] = char.vertical_orientation.display_name
    char_dict["utf8"] = get_utf8_value(chr(char.codepoint_dec))
    char_dict["utf16"] = get_utf16_value(chr(char.codepoint_dec))
    char_dict["utf32"] = get_utf32_value(chr(char.codepoint_dec))
    char_dict["uriEncoded"] = get_uri_encoded_value(chr(char.codepoint_dec))
    char_dict["htmlEntities"] = get_html_entities(char.codepoint_dec)
    char_dict["utf8Bytes"] = get_utf8_hex_bytes(chr(char.codepoint_dec))
    char_dict["utf16Bytes"] = get_utf16_hex_bytes(chr(char.codepoint_dec))
    char_dict["utf32Bytes"] = get_utf32_hex_bytes(chr(char.codepoint_dec))
    return char_dict


def get_script_extension(value: str) -> list[str]:
    return [ScriptCode.from_code(script).display_name for script in value.split(" ")]


def get_decomposition_mapping(value: str) -> list[str]:
    return [f"{chr(int(hex_str, 16))} (U+{int(hex_str, 16):04X})" for hex_str in value.split(" ")]


def get_all_properties_in_group(
    char_dict: dict[str, bool | int | str | list[int] | list[str]], group: CharPropertyGroup
) -> dict[str, bool | int | str | list[int] | list[str]]:
    return {propName: char_dict[propName] for [propName, _] in CHARACTER_PROPERTY_GROUPS[group]}


def prune_superfluous_properties(
    char: UnicodeCharacter, char_dict: dict[str, bool | int | str | list[int] | list[str]], prop_groups: list[CharPropertyGroup]
) -> dict[str, bool | int | str | list[int] | list[str]]:
    if CharPropertyGroup.BIDIRECTIONALITY in prop_groups and not char.bidirectional_is_mirrored:
        char_dict.pop("bidirectionalMirroringGlyph")
    if CharPropertyGroup.BIDIRECTIONALITY in prop_groups and "n" in char.paired_bracket_type.code:
        char_dict.pop("pairedBracketProperty")
    if CharPropertyGroup.NUMERIC in prop_groups and char.numeric_value == "NaN":
        char_dict.pop("numericValue")
        char_dict.pop("numericValueParsed")
    return char_dict
