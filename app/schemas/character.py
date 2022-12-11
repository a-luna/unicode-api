from app.schemas.camel_model import CamelModel


class UnicodeCharacterBase(CamelModel):
    character: str
    name: str
    codepoint: str


class UnicodeCharacterResult(UnicodeCharacterBase):
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


class UnicodeCharacter(UnicodeCharacterBase):
    block: str
    plane: str
    age: str
    html_entities: list[str] | None
    uri_encoded: str | None
    utf8_hex_bytes: list[str] | None
    utf8_dec_bytes: list[int] | None
    utf8: str | None
    utf16: str | None
    utf32: str | None
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

    def __str__(self):
        return (
            "UnicodeCharacter<"
            f"character={self.character}, "
            f"name={self.name}, "
            f"codepoint={self.codepoint}"
            ">"
        )


class UnicodeCharacterInternal(UnicodeCharacter):
    codepoint_dec: int
    block_id: int
    plane_number: int
    general_category_value: str
    combining_class_value: int
    bidirectional_class_value: str
    paired_bracket_type_value: str
    decomposition_type_value: str
    numeric_type_value: str
    joining_class_value: str
    line_break_value: str
    east_asian_width_value: str
    script_value: str
    script_extension_value: str
    hangul_syllable_type_value: str
    indic_syllabic_category_value: str
    indic_matra_category_value: str
    indic_positional_category_value: str
    vertical_orientation_value: str

    def __str__(self):
        return (
            "UnicodeCharacterInternal<"
            f"character={self.character}, "
            f"name={self.name}, "
            f"codepoint={self.codepoint}, "
            f"codepoint_dec={self.codepoint_dec}"
            ">"
        )
