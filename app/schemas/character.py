from app.schemas.camel_model import CamelModel


class UnicodeCharacterBase(CamelModel):
    character: str
    name: str
    code_point: str


class UnicodeCharacterMinimal(UnicodeCharacterBase):
    pass


class UnicodeCharacter(UnicodeCharacterMinimal):
    block: str
    plane: str
    category: str
    bidirectional_class: str
    combining_class: str
    is_mirrored: bool
    html_entities: list[str]
    encoded: str
    utf_8: str
    utf_16: str
    utf_32: str
    hex_bytes: list[str]
    dec_bytes: list[int]


class UnicodeCharacterInternal(UnicodeCharacter):
    code_point_dec: int
    category_value: str
    bidirectional_class_value: str
    combining_class_value: int
