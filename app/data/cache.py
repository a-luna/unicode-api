import json
from functools import cached_property

from app.core.config import BLOCKS_JSON, CHAR_NAME_MAP, CHAR_NO_NAME_MAP, PLANES_JSON
from app.core.result import Result
from app.core.util import get_codepoint_string
from app.data.constants import (
    CJK_COMPATIBILITY_BLOCKS,
    CJK_UNIFIED_BLOCKS,
    NON_CHARACTER_CODEPOINTS,
    PRIVATE_USE_BLOCK_IDS,
    SINGLE_NO_NAME_BLOCKS,
    SURROGATE_BLOCK_IDS,
    TANGUT_BLOCKS,
)
from app.schemas.enums import NamelessCharacterType


class UnicodeDataCache:
    @cached_property
    def char_name_map(self) -> dict[int, str]:
        json_map = json.loads(CHAR_NAME_MAP.read_text())
        return {int(codepoint): name for (codepoint, name) in json_map.items()}

    @cached_property
    def name_search_choices(self) -> dict[int, str]:
        return {codepoint: name.lower() for (codepoint, name) in self.char_name_map.items()}

    @property
    def total_name_choices(self) -> int:
        return len(self.name_search_choices)

    @cached_property
    def char_no_name_map(self) -> dict[int, str]:
        json_map = json.loads(CHAR_NO_NAME_MAP.read_text())
        return {int(codepoint): name for (codepoint, name) in json_map.items()}

    @property
    def all_codepoints(self) -> set[int]:
        return set(list(self.char_name_map.keys()) + list(self.char_no_name_map.keys()))

    @cached_property
    def block_id_map(self) -> dict[int, dict[str, int | str]]:
        return {int(block["id"]): block for block in json.loads(BLOCKS_JSON.read_text())}

    @cached_property
    def block_name_map(self) -> dict[str, dict[str, int | str]]:
        return {block["name"]: block for block in json.loads(BLOCKS_JSON.read_text())}

    @property
    def blocks(self) -> list[dict[str, int | str]]:
        return list(self.block_name_map.values())

    @cached_property
    def plane_number_map(self) -> dict[int, dict[str, int | str]]:
        return {int(plane["number"]): plane for plane in json.loads(PLANES_JSON.read_text())}

    @cached_property
    def plane_name_map(self) -> dict[str, dict[str, int | str]]:
        return {plane["name"]: plane for plane in json.loads(PLANES_JSON.read_text())}

    @property
    def planes(self) -> list[dict[str, int | str]]:
        return list(self.plane_name_map.values())

    def codepoint_is_in_unicode_range(self, codepoint: int) -> bool:
        return codepoint >= 0 and codepoint <= 1114111

    def codepoint_is_assigned(self, codepoint: int) -> bool:
        return codepoint in self.all_codepoints

    def codepoint_is_surrogate(self, codepoint: int) -> bool:
        if block := self.get_unicode_block_containing_codepoint(codepoint):
            return block["id"] in SURROGATE_BLOCK_IDS
        return False

    def get_nameless_character_type(self, codepoint: int) -> Result[NamelessCharacterType]:
        if f"{codepoint:X}" in NON_CHARACTER_CODEPOINTS:
            return Result.Ok(NamelessCharacterType.NONCHARACTER)
        if block := self.get_unicode_block_containing_codepoint(codepoint):
            if block["id"] in SURROGATE_BLOCK_IDS:
                return Result.Ok(NamelessCharacterType.SURROGATE)
            if block["id"] in PRIVATE_USE_BLOCK_IDS:
                return Result.Ok(NamelessCharacterType.PRIVATE_USE)
        return (
            Result.Ok(NamelessCharacterType.RESERVED)
            if self.codepoint_is_in_unicode_range(codepoint)
            else Result.Fail(f"{get_codepoint_string(codepoint)} is not a valid codepoint in the Unicode Standard")
        )

    def get_unicode_block_containing_codepoint(self, codepoint: int) -> dict[str, str | int] | None:
        found = [
            block
            for block in self.blocks
            if int(block["start_dec"]) <= codepoint and codepoint <= int(block["finish_dec"])
        ]
        return found[0] if found else None

    def get_unicode_char_name(self, codepoint: int) -> str:
        if not self.codepoint_is_assigned(codepoint):
            return self.get_codepoint_label_for_nameless_character(codepoint)
        if block := self.get_unicode_block_containing_codepoint(codepoint):
            if block["id"] in CJK_UNIFIED_BLOCKS:
                return f"CJK UNIFIED IDEOGRAPH-{codepoint:04X}"
            if block["id"] in CJK_COMPATIBILITY_BLOCKS:
                return f"CJK COMPATIBILITY IDEOGRAPH-{codepoint:04X}"
            if block["id"] in TANGUT_BLOCKS:
                return f"TANGUT IDEOGRAPH-{codepoint:04X}"
            if block["id"] in SINGLE_NO_NAME_BLOCKS:
                return f"{block} ({get_codepoint_string(codepoint)})"
        return cached_data.char_name_map.get(
            codepoint, f"Undefined Codepoint ({get_codepoint_string(codepoint)}) (Reserved for {block})"
        )

    def get_codepoint_label_for_nameless_character(self, codepoint: int) -> str:
        result = self.get_nameless_character_type(codepoint)
        if result.success:
            charType = result.value
            return f"{charType} ({get_codepoint_string(codepoint)})"
        return f"Invalid Codepoint ({get_codepoint_string(codepoint)})"


cached_data = UnicodeDataCache()
