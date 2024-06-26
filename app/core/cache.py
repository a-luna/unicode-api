import itertools
from functools import cache, cached_property

from rapidfuzz import process

import app.db.models as db
from app.config.api_settings import get_settings
from app.constants import (
    ALL_CONTROL_CHARACTERS,
    ALL_UNICODE_CODEPOINTS,
    ASCII_HEX,
    C0_CONTROL_CHARACTERS,
    MAX_CODEPOINT,
    NON_CHARACTER_CODEPOINTS,
    NULL_BLOCK,
    NULL_PLANE,
)
from app.schemas.enums import CharacterType


class UnicodeDataCache:
    def __init__(self):
        self.settings = get_settings()

    @cached_property
    def non_unihan_character_name_map(self) -> dict[int, str]:
        return self.settings.get_non_unihan_character_name_map()

    @property
    def non_unihan_character_name_choices(self) -> dict[int, str]:
        return {codepoint: name.lower() for (codepoint, name) in self.non_unihan_character_name_map.items()}

    @cached_property
    def blocks(self) -> list[db.UnicodeBlock]:
        blocks = self.settings.get_unicode_blocks_data()
        for block in blocks:
            block.plane = self.get_unicode_plane_containing_block_id(block.id if block.id else 0)
        return blocks

    @property
    def block_id_map(self) -> dict[int, db.UnicodeBlock]:
        return {block.id: block for block in self.blocks if block and block.id}

    @property
    def block_name_choices(self) -> dict[int, str]:
        return {block.id: block.name.lower() for block in self.blocks if block and block.id}

    @property
    def all_characters_block(self) -> db.UnicodeBlock:
        block = db.UnicodeBlock(
            id=0,
            name="All Unicode Characters",
            plane_id=-1,
            start_dec=0,
            start="0000",
            finish_dec=MAX_CODEPOINT,
            finish="10FFFF",
            total_allocated=(MAX_CODEPOINT + 1),
            total_defined=self.official_number_of_unicode_characters,
        )
        block.plane = self.all_characters_plane
        return block

    @property
    def cjk_unified_ideograph_block_ids(self) -> set[int]:
        return {b.id for b in self.blocks if "cjk unified ideographs" in b.name.lower() and b.id}

    @property
    def cjk_compatibility_block_ids(self) -> set[int]:
        return {b.id for b in self.blocks if "cjk compatibility ideographs" in b.name.lower() and b.id}

    @property
    def tangut_ideograph_block_ids(self) -> set[int]:
        return {b.id for b in self.blocks if "tangut" in b.name.lower() and "component" not in b.name.lower() and b.id}

    @property
    def tangut_component_block_ids(self) -> set[int]:
        return {b.id for b in self.blocks if "tangut components" in b.name.lower() and b.id}

    @property
    def surrogate_block_ids(self) -> set[int]:
        return {b.id for b in self.blocks if "surrogate" in b.name.lower() and b.id}

    @property
    def private_use_block_ids(self) -> set[int]:
        return {
            b.id for b in self.blocks if "private use" in b.name.lower() and "surrogate" not in b.name.lower() and b.id
        }

    @cached_property
    def planes(self) -> list[db.UnicodePlane]:
        return self.settings.get_unicode_planes_data()

    @property
    def plane_number_map(self) -> dict[int, db.UnicodePlane]:
        return {plane.number: plane for plane in self.planes}

    @property
    def plane_abbreviation_map(self) -> dict[str, db.UnicodePlane]:
        return {plane.abbreviation: plane for plane in self.planes}

    @property
    def all_characters_plane(self) -> db.UnicodePlane:
        return db.UnicodePlane(
            number=-1,
            name="All Unicode Characters",
            abbreviation="ALL",
            start="0000",
            start_dec=0,
            finish="10FFFF",
            finish_dec=MAX_CODEPOINT,
            start_block_id=1,
            finish_block_id=327,
            total_allocated=(MAX_CODEPOINT + 1),
            total_defined=self.official_number_of_unicode_characters,
        )

    @property
    def all_codepoints_in_unicode_space(self) -> set[int]:
        return set(ALL_UNICODE_CODEPOINTS)

    @property
    def all_control_character_codepoints(self) -> set[int]:
        return set(ALL_CONTROL_CHARACTERS)

    @property
    def all_noncharacter_codepoints(self) -> set[int]:
        return set(NON_CHARACTER_CODEPOINTS)

    @cached_property
    def all_non_unihan_codepoints(self) -> set[int]:
        return set(self.settings.get_non_unihan_character_name_map().keys())

    @cached_property
    def all_cjk_codepoints(self) -> set[int]:
        return set(self.settings.get_unihan_character_name_map().keys())

    @cached_property
    def all_tangut_ideograph_codepoints(self) -> set[int]:
        return {
            cp
            for cp, block_id in self.settings.get_tangut_character_name_map().items()
            if block_id in self.tangut_ideograph_block_ids
        }

    @cached_property
    def all_tangut_component_codepoints(self) -> set[int]:
        return {
            cp
            for cp, block_id in self.settings.get_tangut_character_name_map().items()
            if block_id in self.tangut_component_block_ids
        }

    @property
    def all_tangut_codepoints(self) -> set[int]:
        return self.all_tangut_ideograph_codepoints | self.all_tangut_component_codepoints

    @property
    def all_surrogate_codepoints(self) -> set[int]:
        return self.get_all_codepoints_in_block_id_list(self.surrogate_block_ids)

    @property
    def all_private_use_codepoints(self) -> set[int]:
        return self.get_all_codepoints_in_block_id_list(self.private_use_block_ids)

    @property
    def official_number_of_unicode_characters(self) -> int:
        # The "official" number of characters listed for each version of Unicode is the total number
        # of graphic and format characters (i.e., excluding private-use characters, control characters,
        # noncharacters and surrogate code points).
        # source: https://en.wikipedia.org/wiki/Unicode#cite_ref-25
        total_defined = (
            len(self.all_non_unihan_codepoints) + len(self.all_cjk_codepoints) + len(self.all_tangut_codepoints)
        )
        return total_defined - len(self.all_control_character_codepoints)

    @property
    def unicode_version(self) -> str:
        return self.settings.UNICODE_VERSION

    def search_characters_by_name(self, query: str, score_cutoff: int = 80) -> list[tuple[int, float]]:
        score_cutoff = max(70, score_cutoff)
        fuzzy_search_results = process.extract(
            query.lower(), self.non_unihan_character_name_choices, limit=len(self.non_unihan_character_name_map)
        )
        return [(result, score) for (_, score, result) in fuzzy_search_results if score >= float(score_cutoff)]

    def get_unicode_block_by_id(self, block_id: int) -> db.UnicodeBlock:
        return self.block_id_map.get(block_id, db.UnicodeBlock(**NULL_BLOCK))

    def get_unicode_block_containing_codepoint(self, codepoint: int) -> db.UnicodeBlock:
        found = [block for block in self.blocks if block.start_dec <= codepoint and codepoint <= block.finish_dec]
        return found[0] if found else db.UnicodeBlock(**NULL_BLOCK)

    def search_blocks_by_name(self, query: str, score_cutoff: int = 80) -> list[tuple[int, float]]:
        score_cutoff = max(70, score_cutoff)
        fuzzy_search_results = process.extract(query.lower(), self.block_name_choices, limit=len(self.blocks))
        return [(result, score) for (_, score, result) in fuzzy_search_results if score >= float(score_cutoff)]

    def get_unicode_plane_by_number(self, plane_number: int) -> db.UnicodePlane:
        plane = self.plane_number_map.get(plane_number)
        return (
            plane
            if plane
            else self.get_undefined_plane(plane_number)
            if plane_number >= 4 and plane_number <= 13
            else db.UnicodePlane(**NULL_PLANE)
        )

    def get_undefined_plane(self, plane_number: int) -> db.UnicodePlane:
        return db.UnicodePlane(
            name="Unassigned Plane",
            number=plane_number,
            abbreviation="N/A",
            start=f"{plane_number:X}0000",
            start_dec=int(f"{plane_number:X}0000", 16),
            finish=f"{plane_number:X}FFFF",
            finish_dec=int(f"{plane_number:X}FFFF", 16),
            start_block_id=0,
            finish_block_id=0,
            total_allocated=0,
            total_defined=0,
        )

    def get_unicode_plane_by_abbreviation(self, plane_abbr: str) -> db.UnicodePlane:
        return self.plane_abbreviation_map.get(plane_abbr, db.UnicodePlane(**NULL_PLANE))

    def get_unicode_plane_containing_block_id(self, block_id: int) -> db.UnicodePlane:
        found = [p for p in self.planes if p.start_block_id <= block_id and block_id <= p.finish_block_id]
        return found[0] if found else db.UnicodePlane(**NULL_PLANE)

    def codepoint_is_in_unicode_space(self, codepoint: int) -> bool:
        return codepoint in self.all_codepoints_in_unicode_space

    def codepoint_is_noncharacter(self, codepoint: int) -> bool:
        return codepoint in self.all_noncharacter_codepoints

    def codepoint_is_surrogate(self, codepoint: int) -> bool:
        return codepoint in self.all_surrogate_codepoints

    def codepoint_is_private_use(self, codepoint: int) -> bool:
        return codepoint in self.all_private_use_codepoints

    def codepoint_is_ascii_control_character(self, codepoint: int) -> bool:
        return codepoint in C0_CONTROL_CHARACTERS

    def character_is_non_unihan(self, codepoint: int) -> bool:
        return codepoint in self.non_unihan_character_name_map

    def character_is_unihan(self, codepoint: int) -> bool:
        return codepoint in self.all_cjk_codepoints

    def character_is_tangut(self, codepoint: int) -> bool:
        return codepoint in self.all_tangut_codepoints

    @cache
    def get_character_name(self, codepoint: int) -> str:
        char_type = self.get_character_type(codepoint)
        match char_type:
            case CharacterType.NON_UNIHAN:
                return self.get_name_for_non_unihan_character(codepoint)
            case CharacterType.UNIHAN | CharacterType.TANGUT:
                return self.get_generic_name_for_codepoint(codepoint)
            case _:
                return self.get_label_for_unnamed_codepoint(codepoint, char_type)

    def get_character_type(self, codepoint: int) -> CharacterType:
        return (
            CharacterType.NON_UNIHAN
            if self.character_is_non_unihan(codepoint)
            else CharacterType.UNIHAN
            if self.character_is_unihan(codepoint)
            else CharacterType.TANGUT
            if self.character_is_tangut(codepoint)
            else CharacterType.NONCHARACTER
            if self.codepoint_is_noncharacter(codepoint)
            else CharacterType.SURROGATE
            if self.codepoint_is_surrogate(codepoint)
            else CharacterType.PRIVATE_USE
            if self.codepoint_is_private_use(codepoint)
            else CharacterType.RESERVED
            if self.codepoint_is_in_unicode_space(codepoint)
            else CharacterType.INVALID
        )

    def get_name_for_non_unihan_character(self, codepoint: int) -> str:
        return self.non_unihan_character_name_map.get(codepoint, "")

    def get_generic_name_for_codepoint(self, codepoint: int) -> str:
        block = self.get_unicode_block_containing_codepoint(codepoint)
        return (
            f"CJK UNIFIED IDEOGRAPH-{codepoint:04X}"
            if block.id in self.cjk_unified_ideograph_block_ids
            else f"CJK COMPATIBILITY IDEOGRAPH-{codepoint:04X}"
            if block.id in self.cjk_compatibility_block_ids
            else f"TANGUT IDEOGRAPH-{codepoint:04X}"
            if block.id in self.tangut_ideograph_block_ids
            else f"TANGUT COMPONENT-{self.get_tangut_component_index(codepoint):03}"
            if block.id in self.tangut_component_block_ids
            else ""
        )

    def get_tangut_component_index(self, codepoint: int) -> int:
        tangut_components_block = self.get_unicode_block_by_id(list(self.tangut_component_block_ids)[0])
        # The Tangut component characters are one-indexed
        return (codepoint - tangut_components_block.start_dec) + 1

    def get_label_for_unnamed_codepoint(self, codepoint: int, char_type: CharacterType) -> str:
        match char_type:
            case CharacterType.INVALID:
                return f"Invalid Codepoint (U+{codepoint:04X})"
            case _:
                return f"<{char_type}-{codepoint:04X}>"

    def get_mapped_codepoint_from_hex(self, codepoint_hex: str) -> str:  # pragma: no cover
        if not codepoint_hex:
            return ""
        if codepoint_hex.startswith(("U+", "0x")):
            codepoint_hex = codepoint_hex[2:]
        if any(char not in ASCII_HEX for char in codepoint_hex):
            return f"Invalid Codepoint ({codepoint_hex} is not a valid hex value)"
        return self.get_mapped_codepoint_from_int(int(codepoint_hex, 16))

    def get_mapped_codepoint_from_int(self, codepoint_dec: int) -> str:  # pragma: no cover
        if not codepoint_dec:
            return ""
        if not self.codepoint_is_in_unicode_space(codepoint_dec):
            return f"Invalid Codepoint ({codepoint_dec} is not within the Unicode codespace)"
        return f"{chr(codepoint_dec)} (U+{codepoint_dec:04X} {cached_data.get_character_name(codepoint_dec)})"

    def get_all_codepoints_in_block_id_list(self, block_id_list: list[int]) -> set[int]:
        blocks = [self.get_unicode_block_by_id(block_id) for block_id in block_id_list]
        return set(itertools.chain(*[list(range(block.start_dec, block.finish_dec + 1)) for block in blocks]))


cached_data = UnicodeDataCache()
