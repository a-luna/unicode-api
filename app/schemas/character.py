from typing import List

from app.schemas.camel_model import CamelModel


class UnicodeCharacterInternal(CamelModel):
    character: str
    name: str
    codepoint_dec: int
    codepoint: str
    block: str
    plane: str
    category_value: str
    category: str
    bidirectional_class_value: str
    bidirectional_class: str
    combining_class_value: int
    combining_class: str
    is_mirrored: bool
    html_entities: List[str]
    encoded: str
    utf_8: str
    utf_16: str
    utf_32: str


class UnicodeCharacter(CamelModel):
    character: str
    name: str
    codepoint: str
    block: str
    plane: str
    category_value: str
    category: str
    bidirectional_class_value: str
    bidirectional_class: str
    combining_class_value: int
    combining_class: str
    is_mirrored: bool
    html_entities: List[str]
    encoded: str
    utf_8: str
    utf_16: str
    utf_32: str


class UnicodeCharacterMinimal(CamelModel):
    character: str
    name: str
    codepoint: str
