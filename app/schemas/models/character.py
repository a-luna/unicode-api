from sqlalchemy import Column, Integer
from sqlalchemy_utils import ChoiceType
from sqlmodel import Field, Relationship

import app.schemas.enums as enum
from app.schemas.models.camel_model import CamelModel


class UnicodeCharacterBase(CamelModel):
    codepoint_dec: int = Field(index=True, primary_key=True)
    codepoint: str = Field(index=True)
    name: str = Field(index=True)
    age: str
    plane_number: int
    general_category: enum.GeneralCategory = Field(
        sa_column=Column(ChoiceType(enum.GeneralCategory, impl=Integer()), nullable=False)
    )
    combining_class: enum.CombiningClassCategory = Field(
        sa_column=Column(ChoiceType(enum.CombiningClassCategory, impl=Integer()), nullable=False)
    )
    bidirectional_class: enum.BidirectionalClass = Field(
        sa_column=Column(ChoiceType(enum.BidirectionalClass, impl=Integer()), nullable=False)
    )
    bidirectional_is_mirrored: bool
    bidirectional_mirroring_glyph: str
    bidirectional_control: bool
    paired_bracket_type: enum.BidirectionalBracketType = Field(
        sa_column=Column(ChoiceType(enum.BidirectionalBracketType, impl=Integer()), nullable=False)
    )
    paired_bracket_property: str
    decomposition_type: enum.DecompositionType = Field(
        sa_column=Column(ChoiceType(enum.DecompositionType, impl=Integer()), nullable=False)
    )
    NFC_QC: enum.TriadicLogic = Field(sa_column=Column(ChoiceType(enum.TriadicLogic, impl=Integer()), nullable=False))
    NFD_QC: enum.TriadicLogic = Field(sa_column=Column(ChoiceType(enum.TriadicLogic, impl=Integer()), nullable=False))
    NFKC_QC: enum.TriadicLogic = Field(sa_column=Column(ChoiceType(enum.TriadicLogic, impl=Integer()), nullable=False))
    NFKD_QC: enum.TriadicLogic = Field(sa_column=Column(ChoiceType(enum.TriadicLogic, impl=Integer()), nullable=False))
    numeric_type: enum.NumericType = Field(
        sa_column=Column(ChoiceType(enum.NumericType, impl=Integer()), nullable=False)
    )
    numeric_value: str
    numeric_value_parsed: float | None
    joining_type: enum.JoiningType = Field(
        sa_column=Column(ChoiceType(enum.JoiningType, impl=Integer()), nullable=False)
    )
    joining_group: str
    joining_control: bool
    line_break: enum.LineBreakType = Field(
        sa_column=Column(ChoiceType(enum.LineBreakType, impl=Integer()), nullable=False)
    )
    east_asian_width: enum.EastAsianWidthType = Field(
        sa_column=Column(ChoiceType(enum.EastAsianWidthType, impl=Integer()), nullable=False)
    )
    uppercase: bool
    lowercase: bool
    simple_uppercase_mapping: str
    simple_lowercase_mapping: str
    simple_titlecase_mapping: str
    simple_case_folding: str
    script: enum.ScriptCode = Field(sa_column=Column(ChoiceType(enum.ScriptCode, impl=Integer()), nullable=False))
    script_extensions: str
    hangul_syllable_type: enum.HangulSyllableType = Field(
        sa_column=Column(ChoiceType(enum.HangulSyllableType, impl=Integer()), nullable=False)
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
    vertical_orientation: enum.VerticalOrientationType = Field(
        sa_column=Column(ChoiceType(enum.VerticalOrientationType, impl=Integer()), nullable=False)
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
    character: str = ""
    name: str = ""
    codepoint: str = ""
    uri_encoded: str = ""
    block: str = ""
    plane: str = ""
    age: str = ""
    general_category: str = ""
    combining_class: str = ""
    html_entities: list[str] = []
    score: float = 0.0
    utf8: str = ""
    utf8_hex_bytes: list[str] = []
    utf8_dec_bytes: list[str] = []
    utf16: str = ""
    utf16_hex_bytes: list[str] = []
    utf16_dec_bytes: list[str] = []
    utf32: str = ""
    utf32_hex_bytes: list[str] = []
    utf32_dec_bytes: list[str] = []
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
    numeric_value: str = ""
    numeric_value_parsed: float | None = 0.0
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
    score: float | None
