from sqlalchemy import Integer
from sqlalchemy_utils import ChoiceType
from sqlmodel import Field, Relationship

from app.schemas.enums import (
    BidirectionalBracketType,
    BidirectionalClass,
    CombiningClassCategory,
    DecompositionType,
    EastAsianWidthType,
    HangulSyllableType,
    JoiningType,
    LineBreakType,
    NumericType,
    ScriptCode,
    TriadicLogic,
    VerticalOrientationType,
)
from app.schemas.models.camel_model import CamelModel


class UnicodeCharacterBase(CamelModel):
    codepoint_dec: int = Field(index=True, primary_key=True)
    codepoint: str = Field(index=True)
    name: str = Field(index=True)
    age: str
    plane_number: int
    general_category: str
    combining_class: CombiningClassCategory = Field(sa_type=ChoiceType(CombiningClassCategory, impl=Integer()))
    bidirectional_class: BidirectionalClass = Field(sa_type=ChoiceType(BidirectionalClass, impl=Integer()))
    bidirectional_is_mirrored: bool
    bidirectional_mirroring_glyph: str
    bidirectional_control: bool
    paired_bracket_type: BidirectionalBracketType = Field(sa_type=ChoiceType(BidirectionalBracketType, impl=Integer()))
    paired_bracket_property: str
    decomposition_type: DecompositionType = Field(sa_type=ChoiceType(DecompositionType, impl=Integer()))
    NFC_QC: TriadicLogic = Field(sa_type=ChoiceType(TriadicLogic, impl=Integer()))
    NFD_QC: TriadicLogic = Field(sa_type=ChoiceType(TriadicLogic, impl=Integer()))
    NFKC_QC: TriadicLogic = Field(sa_type=ChoiceType(TriadicLogic, impl=Integer()))
    NFKD_QC: TriadicLogic = Field(sa_type=ChoiceType(TriadicLogic, impl=Integer()))
    numeric_type: NumericType = Field(sa_type=ChoiceType(NumericType, impl=Integer()))
    numeric_value: str
    joining_type: JoiningType = Field(sa_type=ChoiceType(JoiningType, impl=Integer()))
    joining_group: str
    joining_control: bool
    line_break: LineBreakType = Field(sa_type=ChoiceType(LineBreakType, impl=Integer()))
    east_asian_width: EastAsianWidthType = Field(sa_type=ChoiceType(EastAsianWidthType, impl=Integer()))
    uppercase: bool
    lowercase: bool
    simple_uppercase_mapping: str
    simple_lowercase_mapping: str
    simple_titlecase_mapping: str
    simple_case_folding: str
    script: ScriptCode = Field(sa_type=ChoiceType(ScriptCode, impl=Integer()))
    script_extensions: str
    hangul_syllable_type: HangulSyllableType = Field(sa_type=ChoiceType(HangulSyllableType, impl=Integer()))
    indic_syllabic_category: str
    indic_matra_category: str
    indic_positional_category: str
    ideographic: bool | None = False
    unified_ideograph: bool | None = False
    equivalent_unified_ideograph: str | None = None
    radical: bool | None = False
    dash: bool
    hyphen: bool
    quotation_mark: bool
    terminal_punctuation: bool
    sentence_terminal: bool
    diacritic: bool
    extender: bool
    soft_dotted: bool
    alphabetic: bool
    math: bool
    hex_digit: bool
    ascii_hex_digit: bool
    default_ignorable_code_point: bool
    logical_order_exception: bool
    prepended_concatenation_mark: bool
    white_space: bool
    vertical_orientation: VerticalOrientationType = Field(sa_type=ChoiceType(VerticalOrientationType, impl=Integer()))
    regional_indicator: bool
    emoji: bool
    emoji_presentation: bool
    emoji_modifier: bool
    emoji_modifier_base: bool
    emoji_component: bool
    extended_pictographic: bool

    block_id: int = Field(foreign_key="block.id")
    plane_id: int = Field(foreign_key="plane.id")


class UnicodeCharacter(UnicodeCharacterBase, table=True):
    __tablename__ = "character"  # type: ignore  # noqa: PGH003

    block: "UnicodeBlock" = Relationship(back_populates="characters")  # type: ignore  # noqa: PGH003
    plane: "UnicodePlane" = Relationship(back_populates="characters")  # type: ignore  # noqa: PGH003


class UnicodeCharacterUnihan(UnicodeCharacterBase, table=True):
    __tablename__ = "character_unihan"  # type: ignore  # noqa: PGH003

    block: "UnicodeBlock" = Relationship(back_populates="characters_unihan")  # type: ignore  # noqa: PGH003
    plane: "UnicodePlane" = Relationship(back_populates="characters_unihan")  # type: ignore  # noqa: PGH003

    description: str | None = None
    ideo_frequency: int | None = None
    ideo_grade_level: int | None = None
    rs_count_unicode: str | None = None
    rs_count_kangxi: str | None = None
    total_strokes: str | None = None
    traditional_variant: str | None = None
    simplified_variant: str | None = None
    z_variant: str | None = None
    compatibility_variant: str | None = None
    semantic_variant: str | None = None
    specialized_semantic_variant: str | None = None
    spoofing_variant: str | None = None
    accounting_numeric: str | None = None
    primary_numeric: str | None = None
    other_numeric: str | None = None
    hangul: str | None = None
    cantonese: str | None = None
    mandarin: str | None = None
    japanese_kun: str | None = None
    japanese_on: str | None = None
    vietnamese: str | None = None


class UnicodeCharacterResponse(CamelModel):
    character: str = ""
    name: str = ""
    description: str | None = None
    codepoint: str = ""
    uri_encoded: str = ""
    block: str = ""
    plane: str = ""
    age: str = ""
    general_category: str = ""
    combining_class: str = ""
    html_entities: list[str] = []
    ideo_frequency: int | None = None
    ideo_grade_level: int | None = None
    rs_count_unicode: str | None = None
    rs_count_kangxi: str | None = None
    total_strokes: list[int] | None = None
    score: float = 0.0
    utf8: str = ""
    utf8_hex_bytes: list[str] = []
    utf8_dec_bytes: list[int] = []
    utf16: str = ""
    utf16_hex_bytes: list[str] = []
    utf16_dec_bytes: list[int] = []
    utf32: str = ""
    utf32_hex_bytes: list[str] = []
    utf32_dec_bytes: list[int] = []
    bidirectional_class: str = ""
    bidirectional_is_mirrored: bool = False
    bidirectional_mirroring_glyph: str = ""
    bidirectional_control: bool = False
    paired_bracket_type: str = ""
    paired_bracket_property: str = ""
    decomposition_type: str = ""
    NFC_QC: str = ""
    NFD_QC: str = ""
    NFKC_QC: str = ""
    NFKD_QC: str = ""
    numeric_type: str = ""
    numeric_value: list[str] | None = []
    numeric_value_parsed: list[float] | None = []
    joining_type: str = ""
    joining_group: str = ""
    joining_control: bool = False
    line_break: str = ""
    east_asian_width: str = ""
    uppercase: bool = False
    lowercase: bool = False
    simple_uppercase_mapping: str = ""
    simple_lowercase_mapping: str = ""
    simple_titlecase_mapping: str = ""
    simple_case_folding: str = ""
    script: str = ""
    script_extensions: list[str] = []
    hangul_syllable_type: str = ""
    indic_syllabic_category: str = ""
    indic_matra_category: str = ""
    indic_positional_category: str = ""
    ideographic: bool | None = False
    unified_ideograph: bool | None = False
    radical: bool | None = False
    equivalent_unified_ideograph: str | None = None
    traditional_variant: list[str] | None = None
    simplified_variant: list[str] | None = None
    z_variant: list[str] | None = None
    compatibility_variant: list[str] | None = None
    semantic_variant: list[str] | None = None
    specialized_semantic_variant: list[str] | None = None
    spoofing_variant: list[str] | None = None
    accounting_numeric: str | None = None
    primary_numeric: str | None = None
    other_numeric: str | None = None
    hangul: str | None = None
    cantonese: str | None = None
    mandarin: str | None = None
    japanese_kun: str | None = None
    japanese_on: str | None = None
    vietnamese: str | None = None
    dash: bool = False
    hyphen: bool = False
    quotation_mark: bool = False
    terminal_punctuation: bool = False
    sentence_terminal: bool = False
    diacritic: bool = False
    extender: bool = False
    soft_dotted: bool = False
    alphabetic: bool = False
    math: bool = False
    hex_digit: bool = False
    ascii_hex_digit: bool = False
    default_ignorable_code_point: bool = False
    logical_order_exception: bool = False
    prepended_concatenation_mark: bool = False
    white_space: bool = False
    vertical_orientation: str = ""
    regional_indicator: bool = False
    emoji: bool = False
    emoji_presentation: bool = False
    emoji_modifier: bool = False
    emoji_modifier_base: bool = False
    emoji_component: bool = False
    extended_pictographic: bool = False


class UnicodeCharacterResult(CamelModel):
    character: str
    name: str
    description: str | None = None
    codepoint: str
    uri_encoded: str
    score: float | None = None
