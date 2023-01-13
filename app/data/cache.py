import json
from functools import cache, cached_property

from app.core.config import BLOCKS_JSON, CHAR_NAME_MAP, CHAR_NO_NAME_MAP, PLANES_JSON
from app.core.result import Result
from app.core.util import get_codepoint_string
from app.data.constants import (
    CJK_COMPATIBILITY_BLOCKS,
    CJK_UNIFIED_BLOCKS,
    MAX_CODEPOINT,
    NON_CHARACTER_CODEPOINTS,
    NULL_BLOCK,
    NULL_PLANE,
    PRIVATE_USE_BLOCK_IDS,
    SINGLE_NO_NAME_BLOCKS,
    SURROGATE_BLOCK_IDS,
    TANGUT_BLOCKS,
)
from app.schemas.enums import NamelessCharacterType

UnicodeBlockDict = dict[str, int | str]
UnicodePlaneDict = dict[str, int | str]


class UnicodeDataCache:
    @cached_property
    def char_unique_name_map(self) -> dict[int, str]:
        json_map = json.loads(CHAR_NAME_MAP.read_text())
        return {int(codepoint): name for (codepoint, name) in json_map.items()}

    @cached_property
    def char_unique_name_search_choices(self) -> dict[int, str]:
        return {codepoint: name.lower() for (codepoint, name) in self.char_unique_name_map.items()}

    @property
    def total_char_unique_name_search_choices(self) -> int:
        return len(self.char_unique_name_map)

    @cached_property
    def char_generic_name_map(self) -> dict[int, str]:
        return json.loads(CHAR_NO_NAME_MAP.read_text())

    @cached_property
    def char_generic_name_search_choices(self) -> dict[int, str]:
        return {codepoint: name.lower() for (codepoint, name) in self.char_generic_name_map.items()}

    @property
    def total_char_generic_name_search_choices(self) -> int:
        return len(self.char_generic_name_map)

    @property
    def all_assigned_codepoints(self) -> set[int]:
        return set(list(self.char_unique_name_map.keys()) + list(self.char_generic_name_map.keys()))

    @cached_property
    def blocks(self) -> list[UnicodeBlockDict]:
        return json.loads(BLOCKS_JSON.read_text())

    @cached_property
    def block_id_map(self) -> dict[int, UnicodeBlockDict]:
        return {int(block["id"]): block for block in self.blocks}

    @cached_property
    def block_name_map(self) -> dict[str, UnicodeBlockDict]:
        return {str(block["name"]): block for block in self.blocks}

    @cached_property
    def block_name_search_choices(self) -> dict[int, str]:
        return {int(block["id"]): str(block["name"]).lower() for block in self.blocks}

    @property
    def total_block_name_search_choices(self) -> int:
        return len(self.block_name_search_choices)

    @cached_property
    def planes(self) -> list[UnicodePlaneDict]:
        return json.loads(PLANES_JSON.read_text())

    @cached_property
    def plane_number_map(self) -> dict[int, UnicodePlaneDict]:
        return {int(plane["number"]): plane for plane in self.planes}

    @cached_property
    def plane_name_map(self) -> dict[str, UnicodePlaneDict]:
        return {str(plane["name"]): plane for plane in self.planes}

    def codepoint_is_in_unicode_range(self, codepoint: int) -> bool:
        return codepoint >= 0 and codepoint <= MAX_CODEPOINT

    def codepoint_is_assigned(self, codepoint: int) -> bool:
        return codepoint in self.all_assigned_codepoints

    def codepoint_is_surrogate(self, codepoint: int) -> bool:
        block = self.get_unicode_block_containing_codepoint(codepoint)
        return block["id"] in SURROGATE_BLOCK_IDS

    def character_is_uniquely_named(self, codepoint: int) -> bool:
        return codepoint in self.char_unique_name_map

    def get_unicode_block_containing_codepoint(self, codepoint: int) -> UnicodeBlockDict:
        found = [
            block
            for block in self.blocks
            if int(block["start_dec"]) <= codepoint and codepoint <= int(block["finish_dec"])
        ]
        return found[0] if found else NULL_BLOCK

    @cache
    def get_character_name(self, codepoint: int) -> str:
        if not self.codepoint_is_assigned(codepoint):
            return self.get_codepoint_label_for_nameless_character(codepoint)
        block = self.get_unicode_block_containing_codepoint(codepoint)
        char_name = (
            f"CJK UNIFIED IDEOGRAPH-{codepoint:04X}"
            if block["id"] in CJK_UNIFIED_BLOCKS
            else f"CJK COMPATIBILITY IDEOGRAPH-{codepoint:04X}"
            if block["id"] in CJK_COMPATIBILITY_BLOCKS
            else f"TANGUT IDEOGRAPH-{codepoint:04X}"
            if block["id"] in TANGUT_BLOCKS
            else f"{block} ({get_codepoint_string(codepoint)})"
            if block["id"] in SINGLE_NO_NAME_BLOCKS
            else cached_data.char_unique_name_map.get(codepoint)
        )
        return char_name or f"Undefined Codepoint ({get_codepoint_string(codepoint)}) (Reserved for {block})"

    def get_codepoint_label_for_nameless_character(self, codepoint: int) -> str:
        result = self.get_nameless_character_type(codepoint)
        if result.success:
            charType = result.value
            return f"{charType} ({get_codepoint_string(codepoint)})"
        return f"Invalid Codepoint ({get_codepoint_string(codepoint)})"

    def get_nameless_character_type(self, codepoint: int) -> Result[NamelessCharacterType]:
        if not self.codepoint_is_in_unicode_range(codepoint):
            return Result.Fail(f"{get_codepoint_string(codepoint)} is not a valid codepoint in the Unicode Standard")
        block = self.get_unicode_block_containing_codepoint(codepoint)
        charType = (
            NamelessCharacterType.NONCHARACTER
            if f"{codepoint:X}" in NON_CHARACTER_CODEPOINTS
            else NamelessCharacterType.SURROGATE
            if block["id"] in SURROGATE_BLOCK_IDS
            else NamelessCharacterType.PRIVATE_USE
            if block["id"] in PRIVATE_USE_BLOCK_IDS
            else NamelessCharacterType.RESERVED
        )
        return Result.Ok(charType)

    def get_unicode_block(self, block_id: int) -> dict:
        return self.block_id_map.get(block_id, NULL_BLOCK)

    def get_unicode_plane_containing_block_id(self, block_id: int) -> dict[str, int | str]:
        found = [
            plane
            for plane in self.planes
            if int(plane["start_block_id"]) <= block_id and block_id <= int(plane["finish_block_id"])
        ]
        return found[0] if found else NULL_PLANE


cached_data = UnicodeDataCache()
