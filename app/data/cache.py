import itertools
import json
from functools import cache, cached_property

from rapidfuzz import process
from sqlalchemy import distinct, select
from sqlmodel import Session

import app.db.models as db
from app.core.config import settings
from app.data.constants import (
    ALL_CONTROL_CHARACTERS,
    C0_CONTROL_CHARACTERS,
    MAX_CODEPOINT,
    NON_CHARACTER_CODEPOINTS,
    NULL_BLOCK,
    NULL_PLANE,
)
from app.data.encoding import get_codepoint_string
from app.db.engine import engine
from app.schemas.enums import UnassignedCharacterType

CHAR_TABLES = [db.UnicodeCharacter, db.UnicodeCharacterUnihan]


class UnicodeDataCache:
    @cached_property
    def unique_name_character_map(self) -> dict[int, str]:
        json_map = json.loads(settings.CHAR_NAME_MAP.read_text())
        return {int(codepoint): name for (codepoint, name) in json_map.items()}

    @property
    def unique_name_character_choices(self) -> dict[int, str]:
        return {codepoint: name.lower() for (codepoint, name) in self.unique_name_character_map.items()}

    @cached_property
    def blocks(self) -> list[db.UnicodeBlock]:
        if not settings.BLOCKS_JSON.exists():  # pragma: no cover
            return []
        blocks = [db.UnicodeBlock(**block) for block in json.loads(settings.BLOCKS_JSON.read_text())]
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
        return set(b.id for b in self.blocks if "cjk unified ideographs" in b.name.lower() and b.id)

    @property
    def cjk_compatibility_block_ids(self) -> set[int]:
        return set(b.id for b in self.blocks if "cjk compatibility ideographs" in b.name.lower() and b.id)

    @property
    def tangut_character_block_ids(self) -> set[int]:
        return set(
            b.id for b in self.blocks if "tangut" in b.name.lower() and "component" not in b.name.lower() and b.id
        )

    @property
    def surrogate_block_ids(self) -> set[int]:
        return set(b.id for b in self.blocks if "surrogate" in b.name.lower() and b.id)

    @property
    def private_use_block_ids(self) -> set[int]:
        return set(
            b.id for b in self.blocks if "private use" in b.name.lower() and "surrogate" not in b.name.lower() and b.id
        )

    @property
    def all_cjk_ideograph_block_ids(self) -> set[int]:
        return set(list(self.cjk_unified_ideograph_block_ids) + list(self.cjk_compatibility_block_ids))

    @cached_property
    def planes(self) -> list[db.UnicodePlane]:
        return [db.UnicodePlane(**plane) for plane in json.loads(settings.PLANES_JSON.read_text())]

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
        return set(range(0, MAX_CODEPOINT + 1))

    @property
    def all_control_character_codepoints(self) -> set[int]:
        return set(ALL_CONTROL_CHARACTERS)

    @property
    def all_noncharacter_codepoints(self) -> set[int]:
        return set(NON_CHARACTER_CODEPOINTS)

    @property
    def all_named_characters(self) -> set[int]:
        return set(self.unique_name_character_map.keys())

    @property
    def all_cjk_ideograph_codepoints(self):
        cjk_blocks = [self.get_unicode_block_by_id(block_id) for block_id in sorted(self.all_cjk_ideograph_block_ids)]
        cjk_codepoints = [list(range(b.start_dec, b.finish_dec + 1)) for b in cjk_blocks]
        return set(itertools.chain(*cjk_codepoints)) - self.all_noncharacter_codepoints

    @property
    def all_tangut_codepoints(self):
        tangut_blocks = [self.get_unicode_block_by_id(block_id) for block_id in self.tangut_character_block_ids]
        tangut_codepoints = [list(range(b.start_dec, b.finish_dec + 1)) for b in tangut_blocks]
        return set(itertools.chain(*tangut_codepoints)) - self.all_noncharacter_codepoints

    @property
    def all_surrogate_codepoints(self) -> set[int]:
        su_blocks = [self.get_unicode_block_by_id(block_id) for block_id in self.surrogate_block_ids]
        su_codepoints = [list(range(b.start_dec, b.finish_dec + 1)) for b in su_blocks]
        return set(itertools.chain(*su_codepoints)) - self.all_noncharacter_codepoints

    @property
    def all_private_use_codepoints(self) -> set[int]:
        pu_blocks = [self.get_unicode_block_by_id(block_id) for block_id in self.private_use_block_ids]
        pu_codepoints = [list(range(b.start_dec, b.finish_dec + 1)) for b in pu_blocks]
        return set(itertools.chain(*pu_codepoints)) - self.all_noncharacter_codepoints

    @property
    def all_assigned_codepoints(self) -> set[int]:
        return set(
            list(self.all_named_characters)
            + list(self.all_cjk_ideograph_codepoints)
            + list(self.all_tangut_codepoints)
            + list(self.all_surrogate_codepoints)
            + list(self.all_private_use_codepoints)
        )

    @property
    def all_reserved_codepoints(self) -> set[int]:
        return (
            self.all_codepoints_in_unicode_space
            - self.all_assigned_codepoints
            - self.all_noncharacter_codepoints
            - self.all_surrogate_codepoints
            - self.all_private_use_codepoints
        )

    @property
    def official_number_of_unicode_characters(self) -> int:
        # The "official" number of characters listed for each version of Unicode is the total number
        # of graphic and format characters (i.e., excluding private-use characters, control characters,
        # noncharacters and surrogate code points).
        # source: https://en.wikipedia.org/wiki/Unicode#cite_ref-25
        return sum(plane.total_defined for plane in self.planes) - len(self.all_control_character_codepoints)

    @cached_property
    def all_unicode_versions(self):
        with Session(engine) as session:
            versions = []
            for query in [select(distinct(table.age)) for table in CHAR_TABLES]:
                results = session.execute(query).scalars().all()
                versions.extend(float(ver) for ver in results)
            return [str(ver) for ver in sorted(list(set(versions)))]

    @property
    def unicode_version(self) -> str:
        return self.all_unicode_versions[-1]

    def search_characters_by_name(self, query: str, score_cutoff: int = 80) -> list[tuple[int, float]]:
        score_cutoff = max(70, score_cutoff)
        fuzzy_search_results = process.extract(
            query.lower(), self.unique_name_character_choices, limit=len(self.unique_name_character_map)
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

    def codepoint_is_in_unicode_range(self, codepoint: int) -> bool:
        return codepoint in self.all_codepoints_in_unicode_space

    def codepoint_is_assigned(self, codepoint: int) -> bool:
        return codepoint in self.all_assigned_codepoints

    def codepoint_is_noncharacter(self, codepoint: int) -> bool:
        return codepoint in self.all_noncharacter_codepoints

    def codepoint_is_surrogate(self, codepoint: int) -> bool:
        return codepoint in self.all_surrogate_codepoints

    def codepoint_is_private_use(self, codepoint: int) -> bool:
        return codepoint in self.all_private_use_codepoints

    def codepoint_is_reserved(self, codepoint: int) -> bool:
        return codepoint in self.all_reserved_codepoints

    def codepoint_is_ascii_control_character(self, codepoint: int) -> bool:
        return codepoint in C0_CONTROL_CHARACTERS

    def character_is_uniquely_named(self, codepoint: int) -> bool:
        return codepoint in self.unique_name_character_map

    def character_is_unihan(self, codepoint: int) -> bool:
        return codepoint in self.all_cjk_ideograph_codepoints

    def character_is_tangut(self, codepoint: int) -> bool:
        return codepoint in self.all_tangut_codepoints

    def character_is_generically_named(self, codepoint: int) -> bool:
        return self.character_is_unihan(codepoint) or self.character_is_tangut(codepoint)

    @cache
    def get_character_name(self, codepoint: int) -> str:
        return (
            self.get_unique_name_for_codepoint(codepoint)
            if self.character_is_uniquely_named(codepoint)
            else self.get_generic_name_for_codepoint(codepoint)
            if self.character_is_generically_named(codepoint)
            else self.get_label_for_unassigned_codepoint(codepoint)
        )

    def get_unique_name_for_codepoint(self, codepoint: int) -> str:
        return self.unique_name_character_map.get(codepoint, "")

    def get_generic_name_for_codepoint(self, codepoint: int) -> str:
        block = self.get_unicode_block_containing_codepoint(codepoint)
        return (
            f"CJK UNIFIED IDEOGRAPH-{codepoint:04X}"
            if block.id in self.cjk_unified_ideograph_block_ids
            else f"CJK COMPATIBILITY IDEOGRAPH-{codepoint:04X}"
            if block.id in self.cjk_compatibility_block_ids
            else f"TANGUT IDEOGRAPH-{codepoint:04X}"
            if block.id in self.tangut_character_block_ids
            else ""
        )

    def get_label_for_unassigned_codepoint(self, codepoint: int) -> str:
        if (char_type := self.get_unassigned_character_type(codepoint)) != UnassignedCharacterType.INVALID:
            return f"<{char_type}-{codepoint:04X}>"
        return f"Invalid Codepoint ({get_codepoint_string(codepoint)})"

    def get_unassigned_character_type(self, codepoint: int) -> UnassignedCharacterType:
        return (
            UnassignedCharacterType.NONCHARACTER
            if self.codepoint_is_noncharacter(codepoint)
            else UnassignedCharacterType.SURROGATE
            if self.codepoint_is_surrogate(codepoint)
            else UnassignedCharacterType.PRIVATE_USE
            if self.codepoint_is_private_use(codepoint)
            else UnassignedCharacterType.RESERVED
            if self.codepoint_is_reserved(codepoint)
            else UnassignedCharacterType.INVALID
        )


cached_data = UnicodeDataCache()
