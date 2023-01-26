from sqlalchemy import Column, Integer
from sqlalchemy_utils import ChoiceType
from sqlmodel import Field, Relationship

from app.schemas.enums import (
    BidirectionalBracketType,
    BidirectionalClass,
    CombiningClassCategory,
    DecompositionType,
    EastAsianWidthType,
    GeneralCategory,
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
    NFC_QC: TriadicLogic = Field(sa_column=Column(ChoiceType(TriadicLogic, impl=Integer()), nullable=False))
    NFD_QC: TriadicLogic = Field(sa_column=Column(ChoiceType(TriadicLogic, impl=Integer()), nullable=False))
    NFKC_QC: TriadicLogic = Field(sa_column=Column(ChoiceType(TriadicLogic, impl=Integer()), nullable=False))
    NFKD_QC: TriadicLogic = Field(sa_column=Column(ChoiceType(TriadicLogic, impl=Integer()), nullable=False))
    numeric_type: NumericType = Field(sa_column=Column(ChoiceType(NumericType, impl=Integer()), nullable=False))
    numeric_value: str
    numeric_value_parsed: float | None
    joining_type: JoiningType = Field(sa_column=Column(ChoiceType(JoiningType, impl=Integer()), nullable=False))
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
    script: ScriptCode = Field(sa_column=Column(ChoiceType(ScriptCode, impl=Integer()), nullable=False))
    script_extension: str
    hangul_syllable_type: HangulSyllableType = Field(
        sa_column=Column(ChoiceType(HangulSyllableType, impl=Integer()), nullable=False)
    )
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
    math: bool
    hex_digit: bool
    ascii_hex_digit: bool
    default_ignorable_code_point: bool
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
    uri_encoded: str | None
    block: str | None
    plane: str | None
    age: str | None
    general_category: str | None
    combining_class: str | None
    html_entities: list[str] | None
    score: float | None
    utf8: str | None
    utf8_hex_bytes: list[str] | None
    utf8_dec_bytes: list[str] | None
    utf16: str | None
    utf16_hex_bytes: list[str] | None
    utf16_dec_bytes: list[str] | None
    utf32: str | None
    utf32_hex_bytes: list[str] | None
    utf32_dec_bytes: list[str] | None
    bidirectional_class: str | None
    bidirectional_is_mirrored: bool | None
    bidirectional_mirroring_glyph: str | None
    bidirectional_control: bool | None
    paired_bracket_type: str | None
    paired_bracket_property: str | None
    decomposition_type: str | None
    NFC_QC: str | None
    NFD_QC: str | None
    NFKC_QC: str | None
    NFKD_QC: str | None
    numeric_type: str | None
    numeric_value: str | None
    numeric_value_parsed: float | None
    joining_type: str | None
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
    script: str | None
    script_extension: list[str] | None
    hangul_syllable_type: str | None
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
    math: bool | None
    hex_digit: bool | None
    ascii_hex_digit: bool | None
    default_ignorable_code_point: bool | None
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


class UnicodeCharacter(UnicodeCharacterBase, table=True):

    __tablename__ = "character"  # type: ignore

    block: "UnicodeBlock" = Relationship(back_populates="characters")  # type: ignore
    plane: "UnicodePlane" = Relationship(back_populates="characters")  # type: ignore


class UnicodeCharacterNoName(UnicodeCharacterBase, table=True):

    __tablename__ = "character_no_name"  # type: ignore

    block: "UnicodeBlock" = Relationship(back_populates="characters_no_name")  # type: ignore
    plane: "UnicodePlane" = Relationship(back_populates="characters_no_name")  # type: ignore


class UnicodeCharacterResult(CamelModel):
    character: str
    name: str
    codepoint: str
    uri_encoded: str
    score: float
