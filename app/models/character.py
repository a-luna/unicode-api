from typing import TYPE_CHECKING

from sqlalchemy import Integer
from sqlalchemy_utils import ChoiceType
from sqlmodel import Field, Relationship

from app.enums.triadic_logic import TriadicLogic
from app.models.camel_model import CamelModel
from app.models.property_values import Decomposition_Type

if TYPE_CHECKING:  # pragma: no cover
    from app.models.block import UnicodeBlock
    from app.models.plane import UnicodePlane
    from app.models.property_values import (
        Age,
        Bidi_Class,
        Bidi_Paired_Bracket_Type,
        Canonical_Combining_Class,
        East_Asian_Width,
        General_Category,
        Hangul_Syllable_Type,
        Joining_Type,
        Line_Break,
        Numeric_Type,
        Script,
        Vertical_Orientation,
    )


class UnicodeCharacterBase(CamelModel):
    codepoint_dec: int = Field(index=True, primary_key=True)
    codepoint: str = Field(index=True)
    name: str = Field(index=True)
    bidi_mirrored: bool
    bidi_mirroring_glyph: str
    bidi_control: bool
    bidi_paired_bracket_property: str
    NFC_QC: TriadicLogic = Field(sa_type=ChoiceType(TriadicLogic, impl=Integer()))  # type: ignore[reportArgumentType]
    NFD_QC: TriadicLogic = Field(sa_type=ChoiceType(TriadicLogic, impl=Integer()))  # type: ignore[reportArgumentType]
    NFKC_QC: TriadicLogic = Field(sa_type=ChoiceType(TriadicLogic, impl=Integer()))  # type: ignore[reportArgumentType]
    NFKD_QC: TriadicLogic = Field(sa_type=ChoiceType(TriadicLogic, impl=Integer()))  # type: ignore[reportArgumentType]
    numeric_value: str
    joining_group: str
    join_control: bool
    uppercase: bool
    lowercase: bool
    simple_uppercase_mapping: str
    simple_lowercase_mapping: str
    simple_titlecase_mapping: str
    simple_case_folding: str
    script_extensions: str
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
    regional_indicator: bool
    emoji: bool
    emoji_presentation: bool
    emoji_modifier: bool
    emoji_modifier_base: bool
    emoji_component: bool
    extended_pictographic: bool


class UnicodeCharacter(UnicodeCharacterBase, table=True):
    __tablename__ = "character"  # type: ignore  # noqa: PGH003

    block_id: int = Field(foreign_key="block.id")
    plane_id: int = Field(foreign_key="plane.id")
    general_category_id: int = Field(foreign_key="general_category.id")
    age_id: int = Field(foreign_key="age.id")
    combining_class_id: int = Field(foreign_key="canonical_combining_class.id")
    bidi_class_id: int = Field(foreign_key="bidi_class.id")
    bidi_paired_bracket_type_id: int = Field(foreign_key="bidi_paired_bracket_type.id")
    decomposition_type_id: int | None = Field(default=None, foreign_key="decomposition_type.id")
    numeric_type_id: int = Field(foreign_key="numeric_type.id")
    joining_type_id: int = Field(foreign_key="joining_type.id")
    line_break_id: int = Field(foreign_key="line_break.id")
    east_asian_width_id: int = Field(foreign_key="east_asian_width.id")
    script_id: int = Field(foreign_key="script.id")
    hangul_syllable_type_id: int = Field(foreign_key="hangul_syllable_type.id")
    vertical_orientation_id: int = Field(foreign_key="vertical_orientation.id")

    block: "UnicodeBlock" = Relationship(back_populates="characters")  # type: ignore  # noqa: PGH003
    plane: "UnicodePlane" = Relationship(back_populates="characters")  # type: ignore  # noqa: PGH003
    general_category: "General_Category" = Relationship(back_populates="characters")  # type: ignore  # noqa: PGH003
    age: "Age" = Relationship(back_populates="characters")  # type: ignore  # noqa: PGH003
    combining_class: "Canonical_Combining_Class" = Relationship(back_populates="characters")  # type: ignore  # noqa: PGH003
    bidi_class: "Bidi_Class" = Relationship(back_populates="characters")  # type: ignore  # noqa: PGH003
    bidi_paired_bracket_type: "Bidi_Paired_Bracket_Type" = Relationship(back_populates="characters")  # type: ignore  # noqa: PGH003
    decomposition_type: Decomposition_Type | None = Relationship(back_populates="characters")  # type: ignore  # noqa: PGH003
    numeric_type: "Numeric_Type" = Relationship(back_populates="characters")  # type: ignore  # noqa: PGH003
    joining_type: "Joining_Type" = Relationship(back_populates="characters")  # type: ignore  # noqa: PGH003
    line_break: "Line_Break" = Relationship(back_populates="characters")  # type: ignore  # noqa: PGH003
    east_asian_width: "East_Asian_Width" = Relationship(back_populates="characters")  # type: ignore  # noqa: PGH003
    script: "Script" = Relationship(back_populates="characters")  # type: ignore  # noqa: PGH003
    hangul_syllable_type: "Hangul_Syllable_Type" = Relationship(back_populates="characters")  # type: ignore  # noqa: PGH003
    vertical_orientation: "Vertical_Orientation" = Relationship(back_populates="characters")  # type: ignore  # noqa: PGH003


class UnicodeCharacterUnihan(UnicodeCharacterBase, table=True):
    __tablename__ = "character_unihan"  # type: ignore  # noqa: PGH003

    block_id: int = Field(foreign_key="block.id")
    plane_id: int = Field(foreign_key="plane.id")
    general_category_id: int = Field(foreign_key="general_category.id")
    age_id: int = Field(foreign_key="age.id")
    combining_class_id: int = Field(foreign_key="canonical_combining_class.id")
    bidi_class_id: int = Field(foreign_key="bidi_class.id")
    bidi_paired_bracket_type_id: int = Field(foreign_key="bidi_paired_bracket_type.id")
    decomposition_type_id: int | None = Field(default=None, foreign_key="decomposition_type.id")
    numeric_type_id: int = Field(foreign_key="numeric_type.id")
    joining_type_id: int = Field(foreign_key="joining_type.id")
    line_break_id: int = Field(foreign_key="line_break.id")
    east_asian_width_id: int = Field(foreign_key="east_asian_width.id")
    script_id: int = Field(foreign_key="script.id")
    hangul_syllable_type_id: int = Field(foreign_key="hangul_syllable_type.id")
    vertical_orientation_id: int = Field(foreign_key="vertical_orientation.id")

    block: "UnicodeBlock" = Relationship(back_populates="unihan_characters")  # type: ignore  # noqa: PGH003
    plane: "UnicodePlane" = Relationship(back_populates="unihan_characters")  # type: ignore  # noqa: PGH003
    general_category: "General_Category" = Relationship(back_populates="unihan_characters")  # type: ignore  # noqa: PGH003
    age: "Age" = Relationship(back_populates="unihan_characters")  # type: ignore  # noqa: PGH003
    combining_class: "Canonical_Combining_Class" = Relationship(back_populates="unihan_characters")  # type: ignore  # noqa: PGH003
    bidi_class: "Bidi_Class" = Relationship(back_populates="unihan_characters")  # type: ignore  # noqa: PGH003
    bidi_paired_bracket_type: "Bidi_Paired_Bracket_Type" = Relationship(back_populates="unihan_characters")  # type: ignore  # noqa: PGH003
    decomposition_type: Decomposition_Type | None = Relationship(back_populates="unihan_characters")  # type: ignore  # noqa: PGH003
    numeric_type: "Numeric_Type" = Relationship(back_populates="unihan_characters")  # type: ignore  # noqa: PGH003
    joining_type: "Joining_Type" = Relationship(back_populates="unihan_characters")  # type: ignore  # noqa: PGH003
    line_break: "Line_Break" = Relationship(back_populates="unihan_characters")  # type: ignore  # noqa: PGH003
    east_asian_width: "East_Asian_Width" = Relationship(back_populates="unihan_characters")  # type: ignore  # noqa: PGH003
    script: "Script" = Relationship(back_populates="unihan_characters")  # type: ignore  # noqa: PGH003
    hangul_syllable_type: "Hangul_Syllable_Type" = Relationship(back_populates="unihan_characters")  # type: ignore  # noqa: PGH003
    vertical_orientation: "Vertical_Orientation" = Relationship(back_populates="unihan_characters")  # type: ignore  # noqa: PGH003

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
    bidi_class: str = ""
    bidi_mirrored: bool = False
    bidi_mirroring_glyph: str = ""
    bidi_control: bool = False
    bidi_paired_bracket_type: str = ""
    bidi_paired_bracket_property: str = ""
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
    join_control: bool = False
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
