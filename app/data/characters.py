import json
import unicodedata
from html.entities import html5
from http import HTTPStatus
from typing import Dict, List

from fastapi import HTTPException

from app.core.constants import DATA_FOLDER
from app.core.string_util import get_codepoint_string
from app.data.blocks import get_unicode_block_containing_character
from app.data.categories import get_unicode_character_category
from app.data.planes import get_unicode_plane_containing_codepoint
from app.schemas import UnicodeCharacterInternal


def build_unicode_char_map() -> Dict[int, UnicodeCharacterInternal]:
    char_json_file = DATA_FOLDER.joinpath("characters.json")
    char_data = json.loads(char_json_file.read_text())
    return {int(d["codepoint"]): d["name"] for d in char_data}


def build_html_entity_map():
    codepoint_entity_map = [(ord(uni_char), entity) for (entity, uni_char) in html5.items() if len(uni_char) == 1]
    return {cp: entity for (cp, entity) in sorted(codepoint_entity_map, key=lambda x: x[0])}


unicode_char_map = build_unicode_char_map()
html_entity_map = build_html_entity_map()


def get_character_details(uni_char: str) -> UnicodeCharacterInternal:
    if len(uni_char) != 1:
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail="This operation is only valid for strings containing a single character",
        )
    codepoint = ord(uni_char)
    return UnicodeCharacterInternal(
        character=uni_char,
        name=unicode_char_map.get(codepoint),
        codepoint_dec=codepoint,
        codepoint=get_codepoint_string(codepoint),
        block=get_unicode_block_containing_character(uni_char).block,
        plane=get_unicode_plane_containing_codepoint(uni_char).abbreviation,
        category=get_unicode_character_category(unicodedata.category(uni_char)),
        bidirectional_class=unicodedata.bidirectional(uni_char),
        combining_class=unicodedata.combining(uni_char),
        is_mirrored=unicodedata.mirrored(uni_char),
        html_entities=get_html_entities(uni_char),
        utf_8=get_utf8_value(uni_char),
        utf_16=get_utf16_value(uni_char),
        utf_32=get_utf32_value(uni_char),
    )


def get_html_entities(uni_char: str) -> List[str]:
    if len(uni_char) != 1:
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail="This operation is only valid for strings containing a single character",
        )
    codepoint = ord(uni_char)
    cp_hex = hex(codepoint)[2:].upper()
    return [f"&#{codepoint};", f"&#x{cp_hex};"]


def get_utf8_value(uni_char: str) -> str:
    if len(uni_char) != 1:
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail="This operation is only valid for strings containing a single character",
        )
    hex_bytes = [hex(x)[2:].upper() for x in uni_char.encode()]
    return " ".join([f"0x{byte}" for byte in hex_bytes])


def get_utf16_value(uni_char: str) -> str:
    if len(uni_char) != 1:
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail="This operation is only valid for strings containing a single character",
        )
    hex_bytes = [padded(hex(x)[2:]) for x in uni_char.encode("utf_16_be")]
    if len(hex_bytes) == 2:
        return f"0x{hex_bytes[0]}{hex_bytes[1]}"
    if len(hex_bytes) == 4:
        return f"0x{hex_bytes[0]}{hex_bytes[1]} 0x{hex_bytes[2]}{hex_bytes[3]}"


def padded(hex_str: str) -> str:
    pad_length = 2 - len(hex_str)
    return f"{'0'*pad_length}{hex_str.upper()}"


def get_utf32_value(uni_char: str) -> str:
    if len(uni_char) != 1:
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail="This operation is only valid for strings containing a single character",
        )
    cp_hex = hex(ord(uni_char))[2:]
    pad_length = 8 - len(cp_hex)
    return f"0x{'0'*pad_length}{cp_hex.upper()}"
