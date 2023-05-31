from enum import IntEnum, auto

from app.schemas.util import normalize_string_lm3


class DecompositionType(IntEnum):
    NONE = auto()
    CANONICAL = auto()
    OTHERWISE_UNSPECIFIED_COMPATIBILITY_CHARACTER = auto()
    ENCIRCLED_FORM = auto()
    FINAL_PRESENTATION_FORM_ARABIC = auto()
    FONT_VARIANT = auto()
    VULGAR_FRACTION_FORM = auto()
    INITIAL_PRESENTATION_FORM_ARABIC = auto()
    ISOLATED_PRESENTATION_FORM_ARABIC = auto()
    MEDIAL_PRESENTATION_FORM_ARABIC = auto()
    NARROW_OR_HANKAKU_COMPATIBILITY_CHARACTER = auto()
    NO_NO_BREAK_VERSION_OF_A_SPACE_OR_HYPHEN = auto()
    SMALL_VARIANT_FORM_CNS_COMPATIBILITY = auto()
    CJK_SQUARED_FONT_VARIANT = auto()
    SUBSCRIPT_FORM = auto()
    SUPERSCRIPT_FORM = auto()
    VERTICAL_LAYOUT_PRESENTATION_FORM = auto()
    WIDE_OR_ZENKAKU_COMPATIBILITY_CHARACTER = auto()

    def __str__(self):
        return (
            self.name.replace("_", " ")
            .title()
            .replace("Arabic", "(Arabic)")
            .replace("Or Hankaku", "(or Hankaku)")
            .replace("No No Break", "No No-break")
            .replace("Cns Compatibility", "(CNS Compatibility)")
            .replace("Cjk", "CJK")
            .replace("Or Zenkaku", "(or Zenkaku)")
        )

    @property
    def normalized(self) -> str:
        return normalize_string_lm3(self.code)

    @property
    def display_name(self) -> str:
        return f"{self} ({self.code})"

    @property
    def code(self) -> str:
        code_map = {
            "NONE": "none",
            "CANONICAL": "can",
            "OTHERWISE_UNSPECIFIED_COMPATIBILITY_CHARACTER": "com",
            "ENCIRCLED_FORM": "enc",
            "FINAL_PRESENTATION_FORM_ARABIC": "fin",
            "FONT_VARIANT": "font",
            "VULGAR_FRACTION_FORM": "fra",
            "INITIAL_PRESENTATION_FORM_ARABIC": "init",
            "ISOLATED_PRESENTATION_FORM_ARABIC": "iso",
            "MEDIAL_PRESENTATION_FORM_ARABIC": "med",
            "NARROW_OR_HANKAKU_COMPATIBILITY_CHARACTER": "nar",
            "NO_NO_BREAK_VERSION_OF_A_SPACE_OR_HYPHEN": "nb",
            "SMALL_VARIANT_FORM_CNS_COMPATIBILITY": "sml",
            "CJK_SQUARED_FONT_VARIANT": "sqr",
            "SUBSCRIPT_FORM": "sub",
            "SUPERSCRIPT_FORM": "sup",
            "VERTICAL_LAYOUT_PRESENTATION_FORM": "vert",
            "WIDE_OR_ZENKAKU_COMPATIBILITY_CHARACTER": "wide",
        }
        return code_map.get(self.name, "")

    @classmethod
    def from_code(cls, code):  # pragma: no cover
        code_map = {
            "none": cls.NONE,
            "can": cls.CANONICAL,
            "com": cls.OTHERWISE_UNSPECIFIED_COMPATIBILITY_CHARACTER,
            "enc": cls.ENCIRCLED_FORM,
            "fin": cls.FINAL_PRESENTATION_FORM_ARABIC,
            "font": cls.FONT_VARIANT,
            "fra": cls.VULGAR_FRACTION_FORM,
            "init": cls.INITIAL_PRESENTATION_FORM_ARABIC,
            "iso": cls.ISOLATED_PRESENTATION_FORM_ARABIC,
            "med": cls.MEDIAL_PRESENTATION_FORM_ARABIC,
            "nar": cls.NARROW_OR_HANKAKU_COMPATIBILITY_CHARACTER,
            "nb": cls.NO_NO_BREAK_VERSION_OF_A_SPACE_OR_HYPHEN,
            "sml": cls.SMALL_VARIANT_FORM_CNS_COMPATIBILITY,
            "sqr": cls.CJK_SQUARED_FONT_VARIANT,
            "sub": cls.SUBSCRIPT_FORM,
            "sup": cls.SUPERSCRIPT_FORM,
            "vert": cls.VERTICAL_LAYOUT_PRESENTATION_FORM,
            "wide": cls.WIDE_OR_ZENKAKU_COMPATIBILITY_CHARACTER,
        }
        return code_map.get(code, cls.NONE)

    @classmethod
    def match_loosely(cls, name: str):
        prop_names = {e.normalized: e for e in cls if e != e.NONE}
        return prop_names.get(normalize_string_lm3(name))
