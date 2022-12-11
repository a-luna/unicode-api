import json
from functools import cached_property

from rapidfuzz import process

from app.core.config import BLOCKS_JSON, CHARACTERS_JSON, PLANES_JSON, settings
from app.core.enums.block_name import UnicodeBlockName
from app.core.util import get_codepoint_string
from app.data.constants import NULL_BLOCK, NULL_CHARACTER, NULL_CHARACTER_RESULT
from app.data.encoding import get_uri_encoded_value
from app.schemas import (
    UnicodeBlockInternal,
    UnicodeBlockResult,
    UnicodeCharacterInternal,
    UnicodeCharacterResult,
    UnicodePlaneInternal,
)


class Unicode:
    @cached_property
    def planes(self) -> list[UnicodePlaneInternal]:
        planes = [UnicodePlaneInternal(**plane) for plane in json.loads(PLANES_JSON.read_text())]
        return planes

    @property
    def plane_number_map(self) -> dict[int, UnicodePlaneInternal]:
        return {plane.number: plane for plane in self.planes}

    @property
    def plane_name_map(self) -> dict[int, UnicodePlaneInternal]:
        return {plane.name: plane for plane in self.planes}

    @property
    def total_defined_planes(self) -> int:
        return len(self.planes)

    def get_plane_details(self, plane_number: int) -> UnicodePlaneInternal:
        return self.plane_number_map.get(plane_number, self._get_undefined_plane(plane_number))

    @property
    def all_characters_plane(self) -> UnicodePlaneInternal:
        return UnicodePlaneInternal(
            number=-1,
            name="All Unicode Characters",
            abbreviation="ALL",
            start="U+0000",
            start_dec=0,
            finish="U+10FFFF",
            finish_dec=1114111,
            start_block_id=1,
            finish_block_id=327,
            total_allocated=1114112,
            total_defined=sum(plane.total_defined for plane in self.planes),
        )

    @cached_property
    def blocks(self) -> list[UnicodeBlockInternal]:
        blocks = [UnicodeBlockInternal(**block) for block in json.loads(BLOCKS_JSON.read_text())]
        return blocks

    @property
    def total_blocks(self) -> int:
        return len(self.blocks)

    @property
    def block_map(self) -> dict[int, UnicodeBlockInternal]:
        return {block.id: block for block in self.blocks}

    @cached_property
    def block_name_map(self) -> dict[int, str]:
        return {block.id: block.name for block in self.blocks}

    @property
    def all_characters_block(self) -> UnicodeBlockInternal:
        return UnicodeBlockInternal(
            id=0,
            name="All Unicode Characters",
            plane="ALL",
            start_dec=0,
            start="U+0000",
            finish_dec=1114111,
            finish="U+10FFFF",
            total_allocated=1114112,
            total_defined=sum(block.total_defined for block in self.blocks),
        )

    @cached_property
    def characters(self) -> list[UnicodeCharacterInternal]:
        characters = [UnicodeCharacterInternal(**char) for char in json.loads(CHARACTERS_JSON.read_text())]
        return characters

    @property
    def total_defined_characters(self) -> int:
        return len(self.characters)

    @property
    def character_map(self) -> dict[int, UnicodeCharacterInternal]:
        return {char.codepoint_dec: char for char in self.characters}

    @cached_property
    def char_name_map(self) -> dict[int, str]:
        return {char.codepoint_dec: char.name.lower().replace("_", " ") for char in self.characters}

    def get_character_details(
        self, codepoint: int, min_details: bool
    ) -> UnicodeCharacterResult | UnicodeCharacterInternal:
        if codepoint not in self.character_map:
            return NULL_CHARACTER_RESULT if min_details else NULL_CHARACTER
        return self._get_min_char_details(codepoint) if min_details else self.character_map.get(codepoint)

    def search_characters_by_name(self, query: str, score_cutoff: int = 80) -> list[UnicodeCharacterResult]:
        return [
            UnicodeCharacterResult(
                character=chr(result),
                name=self.char_name_map.get(result),
                codepoint=get_codepoint_string(result),
                score=float(f"{score:.1f}"),
                link=f"{settings.API_VERSION}/characters/{get_uri_encoded_value(chr(result))}",
            )
            for (_, score, result) in process.extract(
                query.lower(), self.char_name_map, limit=self.total_defined_characters
            )
            if score >= float(score_cutoff)
        ]

    def search_blocks_by_name(self, query: str, score_cutoff: int = 80) -> list[UnicodeBlockResult]:
        return [
            UnicodeBlockResult(
                id=result,
                name=self.block_map.get(result, NULL_BLOCK).name,
                plane=self.block_map.get(result, NULL_BLOCK).plane,
                start=self.block_map.get(result, NULL_BLOCK).start,
                finish=self.block_map.get(result, NULL_BLOCK).finish,
                score=float(f"{score:.1f}"),
                link=f"{settings.API_VERSION}/blocks/{UnicodeBlockName.from_block_id(result).name}",
            )
            for (_, score, result) in process.extract(query, self.block_name_map, limit=self.total_blocks)
            if score >= float(score_cutoff)
        ]

    def _get_min_char_details(self, codepoint) -> UnicodeCharacterResult:
        if codepoint not in self.character_map:
            return NULL_CHARACTER_RESULT
        char = self.character_map.get(codepoint)
        return UnicodeCharacterResult(
            character=char.character,
            name=char.name,
            codepoint=get_codepoint_string(codepoint),
            link=f"{settings.API_VERSION}/characters/{char.uri_encoded}",
        )

    def _get_undefined_plane(self, plane_number: int) -> UnicodePlaneInternal:
        return UnicodePlaneInternal(
            number=plane_number,
            name="Unassigned Plane",
            abbreviation="N/A",
            start=f"U+{plane_number:X}0000",
            start_dec=int(f"{plane_number:X}0000", 16),
            finish=f"U+{plane_number:X}FFFF",
            finish_dec=int(f"{plane_number:X}FFFF", 16),
            start_block_id=0,
            finish_block_id=0,
            total_allocated=0,
            total_defined=0,
        )