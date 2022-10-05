import json
import unicodedata
from html.entities import html5
from http import HTTPStatus

from fastapi import HTTPException
from rapidfuzz import process

from app.core.constants import DATA_FOLDER
from app.core.string_util import get_code_point_string
from app.data.blocks import (
    CJK_COMPATIBILITY_BLOCKS,
    CJK_UNIFIED_BLOCKS,
    get_unicode_block_containing_character,
    TANGUT_BLOCKS,
)
from app.data.categories import (
    get_character_bidirectional_category,
    get_character_general_category,
    get_combining_class_category,
)
from app.data.planes import get_unicode_plane_containing_code_point
from app.schemas import FuzzySearchResult, UnicodeCharacterInternal


def build_unicode_char_map() -> dict[int, UnicodeCharacterInternal]:
    char_json_file = DATA_FOLDER.joinpath("json/characters.json")
    char_data = json.loads(char_json_file.read_text())
    return {int(d["code_point"]): d["name"] for d in char_data}


def build_html_entity_map():
    code_point_entity_map = [(ord(uni_char), entity) for (entity, uni_char) in html5.items() if len(uni_char) == 1]
    return {cp: entity for (cp, entity) in sorted(code_point_entity_map, key=lambda x: x[0])}


unicode_char_map = build_unicode_char_map()
html_entity_map = build_html_entity_map()


def fuzzy_character_search(query: str, score_cutoff=80):
    results = [
        FuzzySearchResult(character=chr(result), score=score, details=get_character_details(chr(result)))
        for (_, score, result) in process.extract(query, unicode_char_map)
    ]
    return [match for match in results if match.score >= score_cutoff] if results else []


def get_character_details(uni_char: str) -> UnicodeCharacterInternal:
    if len(uni_char) != 1:
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail="This operation is only valid for strings containing a single character",
        )
    block_name = get_unicode_block_containing_character(uni_char).block
    return UnicodeCharacterInternal(
        character=uni_char,
        name=get_unicode_char_name(ord(uni_char), block_name),
        code_point_dec=ord(uni_char),
        code_point=get_code_point_string(ord(uni_char)),
        block=block_name,
        plane=get_unicode_plane_containing_code_point(ord(uni_char)).abbreviation,
        category_value=unicodedata.category(uni_char),
        category=get_character_general_category(unicodedata.category(uni_char)),
        bidirectional_class_value=unicodedata.bidirectional(uni_char),
        bidirectional_class=get_character_bidirectional_category(unicodedata.bidirectional(uni_char)),
        combining_class_value=unicodedata.combining(uni_char),
        combining_class=get_combining_class_category(unicodedata.combining(uni_char)),
        is_mirrored=unicodedata.mirrored(uni_char),
        html_entities=get_html_entities(ord(uni_char)) if block_name != "Undefined Codepoint" else [],
        encoded=get_encoded_value(uni_char) if block_name != "Undefined Codepoint" else "",
        utf_8=get_utf8_value(uni_char) if block_name != "Undefined Codepoint" else "",
        utf_16=get_utf16_value(uni_char) if block_name != "Undefined Codepoint" else "",
        utf_32=get_utf32_value(uni_char) if block_name != "Undefined Codepoint" else "",
        dec_bytes=get_utf8_dec_bytes(uni_char) if block_name != "Undefined Codepoint" else "",
        hex_bytes=get_utf8_hex_bytes(uni_char) if block_name != "Undefined Codepoint" else "",
    )


def get_unicode_char_name(code_point: int, block_name: str) -> str:
    if block_name == "Undefined Codepoint":
        return f"Undefined Codepoint ({get_code_point_string(code_point)})"
    if block_name in CJK_UNIFIED_BLOCKS:
        return f"CJK UNIFIED IDEOGRAPH-{code_point:04X}"
    if block_name in CJK_COMPATIBILITY_BLOCKS:
        return f"CJK COMPATIBILITY IDEOGRAPH-{code_point:04X}"
    if block_name in TANGUT_BLOCKS:
        return f"TANGUT IDEOGRAPH-{code_point:04X}"
    if block_name == "Variation Selectors Supplement":
        return f"VARIATION SELECTOR-{code_point - 917743}"
    char_name = unicode_char_map.get(code_point)
    return char_name if char_name else f"Unassigned Reserved Codepoint ({get_code_point_string(code_point)})"


def get_html_entities(code_point: int) -> list[str]:
    html_entities = [f"&#{code_point};", f"&#x{code_point:02X};"]
    named_entity = html_entity_map.get(code_point)
    if named_entity:
        html_entities.append(f"&{named_entity}")
    return html_entities


def get_utf8_dec_bytes(uni_char: str) -> list[int]:
    return [x for x in uni_char.encode()]


def get_utf8_hex_bytes(uni_char: str) -> list[str]:
    return [f"{x:02X}" for x in uni_char.encode()]


def get_encoded_value(uni_char: str) -> str:
    return "".join(f"%{hex_byte}" for hex_byte in get_utf8_hex_bytes(uni_char))


def get_utf8_value(uni_char: str) -> str:
    return " ".join(f"0x{hex_byte}" for hex_byte in get_utf8_hex_bytes(uni_char))


def get_utf16_value(uni_char: str) -> str:
    hex_bytes = [f"{x:02X}" for x in uni_char.encode("utf_16_be")]
    if len(hex_bytes) == 2:
        return f"0x{hex_bytes[0]}{hex_bytes[1]}"
    if len(hex_bytes) == 4:
        return f"0x{hex_bytes[0]}{hex_bytes[1]} 0x{hex_bytes[2]}{hex_bytes[3]}"


def get_utf32_value(uni_char: str) -> str:
    return f"0x{ord(uni_char):08X}"
