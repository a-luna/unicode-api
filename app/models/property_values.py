from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:  # pragma: no cover
    from app.custom_types import IFilterParameter
    from app.models.character import UnicodeCharacter, UnicodeCharacterUnihan


def default_display_name(prop_value: "IFilterParameter") -> str:  # pragma: no cover
    return f"{prop_value.long_name} ({prop_value.short_name})"


class Age(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str

    characters: list["UnicodeCharacter"] = Relationship(back_populates="age")
    unihan_characters: list["UnicodeCharacterUnihan"] = Relationship(back_populates="age")

    @property
    def display_name(self) -> str:  # pragma: no cover
        return self.short_name


class Bidi_Class(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str

    characters: list["UnicodeCharacter"] = Relationship(back_populates="bidi_class")
    unihan_characters: list["UnicodeCharacterUnihan"] = Relationship(back_populates="bidi_class")

    @property
    def display_name(self) -> str:  # pragma: no cover
        return default_display_name(self)


class Bidi_Paired_Bracket_Type(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str

    characters: list["UnicodeCharacter"] = Relationship(back_populates="bidi_paired_bracket_type")
    unihan_characters: list["UnicodeCharacterUnihan"] = Relationship(back_populates="bidi_paired_bracket_type")

    @property
    def display_name(self) -> str:  # pragma: no cover
        return default_display_name(self)


class Canonical_Combining_Class(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str

    characters: list["UnicodeCharacter"] = Relationship(back_populates="combining_class")
    unihan_characters: list["UnicodeCharacterUnihan"] = Relationship(back_populates="combining_class")

    @property
    def display_name(self) -> str:  # pragma: no cover
        return default_display_name(self)


class Decomposition_Type(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str

    characters: list["UnicodeCharacter"] = Relationship(back_populates="decomposition_type")
    unihan_characters: list["UnicodeCharacterUnihan"] = Relationship(back_populates="decomposition_type")

    @property
    def display_name(self) -> str:  # pragma: no cover
        return default_display_name(self)


class East_Asian_Width(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str

    characters: list["UnicodeCharacter"] = Relationship(back_populates="east_asian_width")
    unihan_characters: list["UnicodeCharacterUnihan"] = Relationship(back_populates="east_asian_width")

    @property
    def display_name(self) -> str:  # pragma: no cover
        return default_display_name(self)


class General_Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str
    is_group: bool | None = False
    grouped_values: str | None = None

    characters: list["UnicodeCharacter"] = Relationship(back_populates="general_category")
    unihan_characters: list["UnicodeCharacterUnihan"] = Relationship(back_populates="general_category")

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.long_name} ({self.short_name})"

    @property
    def category_values(self) -> list[str]:
        return (
            [v.strip() for v in self.grouped_values.split("|")]
            if self.is_group and self.grouped_values
            else [self.short_name]
        )

    @property
    def display_name(self) -> str:  # pragma: no cover
        return default_display_name(self)


class Grapheme_Cluster_Break(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str


class Hangul_Syllable_Type(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str

    characters: list["UnicodeCharacter"] = Relationship(back_populates="hangul_syllable_type")
    unihan_characters: list["UnicodeCharacterUnihan"] = Relationship(back_populates="hangul_syllable_type")

    @property
    def display_name(self) -> str:  # pragma: no cover
        return default_display_name(self)


class Indic_Conjunct_Break(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str


class Indic_Positional_Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str


class Indic_Syllabic_Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str


class Jamo_Short_Name(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str


class Joining_Group(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str


class Joining_Type(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str

    characters: list["UnicodeCharacter"] = Relationship(back_populates="joining_type")
    unihan_characters: list["UnicodeCharacterUnihan"] = Relationship(back_populates="joining_type")

    @property
    def display_name(self) -> str:  # pragma: no cover
        return default_display_name(self)


class Line_Break(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str

    characters: list["UnicodeCharacter"] = Relationship(back_populates="line_break")
    unihan_characters: list["UnicodeCharacterUnihan"] = Relationship(back_populates="line_break")

    @property
    def display_name(self) -> str:  # pragma: no cover
        return default_display_name(self)


class Numeric_Type(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str

    characters: list["UnicodeCharacter"] = Relationship(back_populates="numeric_type")
    unihan_characters: list["UnicodeCharacterUnihan"] = Relationship(back_populates="numeric_type")

    @property
    def display_name(self) -> str:  # pragma: no cover
        return default_display_name(self)


class Script(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str

    characters: list["UnicodeCharacter"] = Relationship(back_populates="script")
    unihan_characters: list["UnicodeCharacterUnihan"] = Relationship(back_populates="script")

    @property
    def display_name(self) -> str:  # pragma: no cover
        return default_display_name(self)


class Sentence_Break(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str


class Vertical_Orientation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str

    characters: list["UnicodeCharacter"] = Relationship(back_populates="vertical_orientation")
    unihan_characters: list["UnicodeCharacterUnihan"] = Relationship(back_populates="vertical_orientation")

    @property
    def display_name(self) -> str:  # pragma: no cover
        return default_display_name(self)


class Word_Break(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    short_name: str
    long_name: str
