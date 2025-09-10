import itertools
import json
import re
from collections.abc import Callable
from functools import cache, cached_property
from typing import TYPE_CHECKING, Any, TypedDict

from pydantic import ValidationError
from rapidfuzz import process

from unicode_api.config.api_settings import get_settings
from unicode_api.constants import (
    ALL_CONTROL_CHARACTERS,
    ALL_UNICODE_CODEPOINTS,
    ASCII_HEX,
    C0_CONTROL_CHARACTERS,
    DEFAULT_BC_AL_CODEPOINTS,
    DEFAULT_BC_ET_CODEPOINTS,
    DEFAULT_BC_R_CODEPOINTS,
    DEFAULT_VO_U_BLOCK_NAMES,
    DEFAULT_VO_U_PLANE_NUMBERS,
    MAX_CODEPOINT,
    NON_CHARACTER_CODEPOINTS,
    PROP_GROUP_INVALID_FOR_VERSION_ROW_ID,
    UNICODE_PLANES_DEFAULT,
)
from unicode_api.core.result import Result
from unicode_api.enums.character_type import CharacterType
from unicode_api.models.block import UnicodeBlock
from unicode_api.models.character import UnicodeCharacter
from unicode_api.models.plane import UnicodePlane
from unicode_api.models.util import normalize_string_lm3

if TYPE_CHECKING:  # pragma: no cover
    from unicode_api.custom_types import UnicodePropertyGroupMap, UnicodePropertyGroupValues


class ApiRouteDetails(TypedDict):
    name: str
    path: str
    path_regex: re.Pattern[str]


NULL_BLOCK = UnicodeBlock(
    id=0,
    long_name="None",
    short_name="None",
    plane_id=-1,
    start="",
    start_dec=0,
    finish="",
    finish_dec=0,
    total_allocated=0,
    total_defined=0,
)

NULL_PLANE = UnicodePlane(
    id=-1,
    number=-1,
    name="None",
    abbreviation="None",
    start="",
    start_dec=0,
    finish="",
    finish_dec=0,
    start_block_id=0,
    finish_block_id=0,
    total_allocated=0,
    total_defined=0,
)


class UnicodeDataCache:
    """
    UnicodeDataCache provides a cached interface to Unicode data and metadata.

    This class centralizes access to Unicode-related data, supporting efficient lookups,
    fuzzy searches, and property value resolution for codepoints. It leverages cached
    properties and methods to minimize redundant computation and file I/O, and exposes
    utility methods for querying Unicode blocks, planes, character types, and property values.

    Attributes:
        settings: Settings
            Application settings object providing access to Unicode data files and configuration.
        api_routes: list[ApiRouteDetails]
            List of API route details for path matching.

    Cached Properties:
        property_value_id_map: UnicodePropertyGroupMap
            Mapping of property group names to their value ID maps.
        missing_property_groups: list[str]
            List of property groups missing in the current Unicode version.
        character_flag_names: list[str]
            List of boolean character property names present in the UnicodeCharacter model.
        non_unihan_character_name_map: dict[int, str]
            Mapping of codepoints to names for non-Unihan characters.
        blocks: list[UnicodeBlock]
            List of UnicodeBlock objects loaded from JSON.
        planes: list[UnicodePlane]
            List of UnicodePlane objects loaded from JSON or defaults.
        all_non_unihan_codepoints: set[int]
            Set of codepoints for non-Unihan characters.
        all_cjk_codepoints: set[int]
            Set of codepoints for CJK Unihan characters.
        all_tangut_ideograph_codepoints: set[int]
            Set of codepoints for Tangut ideographs.
        all_tangut_component_codepoints: set[int]
            Set of codepoints for Tangut components.

    Properties:
        non_unihan_character_name_choices: dict[int, str]
            Lowercased mapping of codepoints to names for non-Unihan characters.
        block_id_map: dict[int, UnicodeBlock]
            Mapping of block IDs to UnicodeBlock objects.
        block_name_choices: dict[int, str]
            Mapping of block IDs to lowercased block long names.
        all_characters_block: UnicodeBlock
            UnicodeBlock representing all Unicode characters.
        cjk_unified_ideograph_block_ids: set[int]
            Set of block IDs for CJK Unified Ideographs.
        cjk_compatibility_block_ids: set[int]
            Set of block IDs for CJK Compatibility Ideographs.
        tangut_ideograph_block_ids: set[int]
            Set of block IDs for Tangut ideographs.
        tangut_component_block_ids: set[int]
            Set of block IDs for Tangut components.
        surrogate_block_ids: set[int]
            Set of block IDs for surrogate codepoints.
        private_use_block_ids: set[int]
            Set of block IDs for private use areas.
        plane_number_map: dict[int, UnicodePlane]
            Mapping of plane numbers to UnicodePlane objects.
        plane_abbreviation_map: dict[str, UnicodePlane]
            Mapping of plane abbreviations to UnicodePlane objects.
        all_characters_plane: UnicodePlane
            UnicodePlane representing all Unicode characters.
        all_codepoints_in_unicode_space: set[int]
            Set of all valid Unicode codepoints.
        all_control_character_codepoints: set[int]
            Set of all control character codepoints.
        all_noncharacter_codepoints: set[int]
            Set of all noncharacter codepoints.
        all_tangut_codepoints: set[int]
            Set of all Tangut codepoints (ideographs and components).
        all_surrogate_codepoints: set[int]
            Set of all surrogate codepoints.
        all_private_use_codepoints: set[int]
            Set of all private use codepoints.
        official_number_of_unicode_characters: int
            The official count of Unicode characters, excluding private-use, control, noncharacters, and surrogates.
        unicode_version: str
            The Unicode version string.
        constant_default_property_value_map: dict[str, str]
            Mapping of property groups to their constant default values.
        variable_default_property_value_map: dict[str, Callable[[int], str]]
            Mapping of property groups to callables for variable default values.

    Methods:
        search_characters_by_name(query: str, score_cutoff: int = 80) -> list[tuple[int, float]]
            Fuzzy search for character names.
        get_unicode_block_by_id(block_id: int) -> UnicodeBlock
            Retrieve a UnicodeBlock by its ID.
        get_unicode_block_containing_codepoint(codepoint: int) -> UnicodeBlock
            Find the block containing a codepoint.
        search_blocks_by_name(query: str, score_cutoff: int = 80) -> list[tuple[int, float]]
            Fuzzy search for block names.
        loose_match_block_name(block_name: str) -> int | None
            Loosely match a block name to its ID.
        get_unicode_plane_by_number(plane_number: int) -> UnicodePlane
            Retrieve a UnicodePlane by its number.
        get_undefined_plane(plane_number: int) -> UnicodePlane
            Create a placeholder for an undefined plane.
        get_unicode_plane_by_abbreviation(plane_abbr: str) -> UnicodePlane
            Retrieve a UnicodePlane by its abbreviation.
        get_unicode_plane_containing_block_id(block_id: int) -> UnicodePlane
            Find the plane containing a block ID.
        codepoint_is_in_unicode_space(codepoint: int) -> bool
            Check if a codepoint is valid in Unicode.
        codepoint_is_noncharacter(codepoint: int) -> bool
            Check if a codepoint is a noncharacter.
        codepoint_is_surrogate(codepoint: int) -> bool
            Check if a codepoint is a surrogate.
        codepoint_is_private_use(codepoint: int) -> bool
            Check if a codepoint is in a private use area.
        codepoint_is_ascii_control_character(codepoint: int) -> bool
            Check if a codepoint is an ASCII control character.
        character_is_non_unihan(codepoint: int) -> bool
            Check if a codepoint is a non-Unihan character.
        character_is_unihan(codepoint: int) -> bool
            Check if a codepoint is a Unihan character.
        character_is_tangut(codepoint: int) -> bool
            Check if a codepoint is a Tangut character.
        get_character_name(codepoint: int) -> str
            Get the display name for a codepoint.
        get_character_type(codepoint: int) -> CharacterType
            Determine the type of a codepoint.
        get_generic_name_for_codepoint(codepoint: int) -> str
            Get a generic name for CJK, Tangut, or component codepoints.
        get_tangut_component_index(codepoint: int) -> int
            Get the index of a Tangut component codepoint.
        get_mapped_codepoint_from_hex(codepoint_hex: str) -> str
            Map a hex string to a codepoint display string.
        get_mapped_codepoint_from_int(codepoint_dec: int) -> str
            Map an integer codepoint to a display string.
        get_all_codepoints_in_block_id_list(block_id_list: set[int]) -> set[int]
            Get all codepoints in a set of block IDs.
        get_all_values_for_property_group(prop_group: str) -> list[UnicodePropertyGroupValues]
            Get all values for a property group.
        get_property_value_ids_by_name(prop_group: str, prop_values: list[str]) -> list[Result[int]]
            Get property value IDs for a list of names.
        get_property_value_id_by_name(prop_group: str, prop_value: str) -> Result[int]
            Get the property value ID for a name.
        get_name_value_map_for_property_group(prop_group: str) -> dict[str, int] | None
            Get a mapping of property value names to IDs.
        get_display_name_for_property_value(
            prop_group: str, prop_value_id: int | None = None, codepoint: int | None = None
        ) -> str
            Get the display name for a property value.
        get_default_value_id_for_property_group(prop_group: str, codepoint: int | None) -> int
            Get the default value ID for a property group.
        get_default_age(codepoint: int) -> str
            Get the default Age property value for a codepoint.
        get_default_bidi_class(codepoint: int) -> str
            Get the default Bidi_Class property value for a codepoint.
        get_default_eaw(codepoint: int) -> str
            Get the default East_Asian_Width property value for a codepoint.
        get_default_general_category(codepoint: int) -> str
            Get the default General_Category property value for a codepoint.
        get_default_vo(codepoint: int) -> str
            Get the default Vertical_Orientation property value for a codepoint.
        get_default_vert_orient_upright_block_ids() -> set[int]
            Get block IDs with default upright vertical orientation.
        get_api_route_from_requested_path(requested_path: str) -> tuple[ApiRouteDetails, str]
            Match a requested path to an API route.

    Exceptions:
        Raises ValueError for invalid data or property group lookups.
    """

    def __init__(self):
        self.settings = get_settings()
        self.api_routes: list[ApiRouteDetails] = []

    @cached_property
    def property_value_id_map(self) -> "UnicodePropertyGroupMap":
        return self.settings.property_value_id_map

    @cached_property
    def missing_property_groups(self) -> list[str]:
        return self.settings.missing_property_group_names

    @cached_property
    def character_flag_names(self) -> list[str]:
        all_flag_names = [p.lower() for p in self.settings.boolean_character_property_names]
        return sorted(set(all_flag_names) & set(UnicodeCharacter.model_fields.keys()))

    @cached_property
    def non_unihan_character_name_map(self) -> dict[int, str]:
        return self.settings.non_unihan_character_name_map

    @property
    def non_unihan_character_name_choices(self) -> dict[int, str]:
        return {codepoint: name.lower() for (codepoint, name) in self.non_unihan_character_name_map.items()}

    @cached_property
    def blocks(self) -> list[UnicodeBlock]:
        blocks_json: list[dict[str, Any]] = (
            json.loads(self.settings.blocks_json.read_text()) if self.settings.blocks_json.exists() else []
        )
        try:
            blocks = [UnicodeBlock.model_validate(block) for block in blocks_json]
        except ValidationError as ex:  # pragma: no cover
            raise ValueError(f"Invalid block data: {ex}") from ex
        for block in blocks:
            block.plane = self.get_unicode_plane_containing_block_id(block.id if block.id else 0)
        return blocks

    @property
    def block_id_map(self) -> dict[int, UnicodeBlock]:
        return {block.id: block for block in self.blocks if block and block.id}

    @property
    def block_name_choices(self) -> dict[int, str]:
        return {block.id: block.long_name.lower() for block in self.blocks if block and block.id}

    @property
    def all_characters_block(self) -> UnicodeBlock:
        block = UnicodeBlock(
            id=0,
            long_name="All Unicode Characters",
            short_name="All",
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
        return {b.id for b in self.blocks if "cjk unified ideographs" in b.long_name.lower() and b.id}

    @property
    def cjk_compatibility_block_ids(self) -> set[int]:
        return {b.id for b in self.blocks if "cjk compatibility ideographs" in b.long_name.lower() and b.id}

    @property
    def tangut_ideograph_block_ids(self) -> set[int]:
        return {
            b.id
            for b in self.blocks
            if "tangut" in b.long_name.lower() and "component" not in b.long_name.lower() and b.id
        }

    @property
    def tangut_component_block_ids(self) -> set[int]:
        return {b.id for b in self.blocks if "tangut components" in b.long_name.lower() and b.id}

    @property
    def surrogate_block_ids(self) -> set[int]:
        return {b.id for b in self.blocks if "surrogate" in b.long_name.lower() and b.id}

    @property
    def private_use_block_ids(self) -> set[int]:
        return {
            b.id
            for b in self.blocks
            if "private use" in b.long_name.lower() and "surrogate" not in b.long_name.lower() and b.id
        }

    @cached_property
    def planes(self) -> list[UnicodePlane]:
        plane_data = (
            json.loads(self.settings.planes_json.read_text())
            if self.settings.planes_json.exists()
            else UNICODE_PLANES_DEFAULT
        )
        try:
            return [UnicodePlane.model_validate(plane) for plane in plane_data]
        except ValidationError as ex:  # pragma: no cover
            raise ValueError(f"Invalid plane data: {ex}") from ex

    @property
    def plane_number_map(self) -> dict[int, UnicodePlane]:
        return {plane.number: plane for plane in self.planes}

    @property
    def plane_abbreviation_map(self) -> dict[str, UnicodePlane]:
        return {plane.abbreviation: plane for plane in self.planes}

    @property
    def all_characters_plane(self) -> UnicodePlane:
        return UnicodePlane(
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
        return set(self.settings.non_unihan_character_name_map.keys())

    @cached_property
    def all_cjk_codepoints(self) -> set[int]:
        return set(self.settings.unihan_character_name_map.keys())

    @cached_property
    def all_tangut_ideograph_codepoints(self) -> set[int]:
        return {
            cp
            for cp, block_id in self.settings.tangut_character_name_map.items()
            if block_id in self.tangut_ideograph_block_ids
        }

    @cached_property
    def all_tangut_component_codepoints(self) -> set[int]:
        return {
            cp
            for cp, block_id in self.settings.tangut_character_name_map.items()
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

    @property
    def constant_default_property_value_map(self):
        return {
            "Bidi_Paired_Bracket_Type": "None",
            "Canonical_Combining_Class": "Not_Reordered",
            "Decomposition_Type": "None",
            "Hangul_Syllable_Type": "Not_Applicable",
            "Joining_Type": "Non_Joining",
            "Line_Break": "Unknown",
            "Numeric_Type": "None",
            "Script": "Unknown",
        }

    @property
    def variable_default_property_value_map(self) -> dict[str, Callable[[int], str]]:
        return {
            "Age": self.get_default_age,
            "Bidi_Class": self.get_default_bidi_class,
            "East_Asian_Width": self.get_default_eaw,
            "General_Category": self.get_default_general_category,
            "Vertical_Orientation": self.get_default_vo,
        }

    def search_characters_by_name(self, query: str, score_cutoff: int = 80) -> list[tuple[int, float]]:
        score_cutoff = max(70, score_cutoff)
        fuzzy_search_results = process.extract(
            query.lower(), self.non_unihan_character_name_choices, limit=len(self.non_unihan_character_name_map)
        )
        return [(result, score) for (_, score, result) in fuzzy_search_results if score >= float(score_cutoff)]

    def get_unicode_block_by_id(self, block_id: int) -> UnicodeBlock:
        return self.block_id_map.get(block_id, NULL_BLOCK)

    def get_unicode_block_containing_codepoint(self, codepoint: int) -> UnicodeBlock:
        found = [block for block in self.blocks if block.start_dec <= codepoint and codepoint <= block.finish_dec]
        return found[0] if found else NULL_BLOCK

    def search_blocks_by_name(self, query: str, score_cutoff: int = 80) -> list[tuple[int, float]]:
        score_cutoff = max(70, score_cutoff)
        fuzzy_search_results = process.extract(query.lower(), self.block_name_choices, limit=len(self.blocks))
        return [(result, score) for (_, score, result) in fuzzy_search_results if score >= float(score_cutoff)]

    def loose_match_block_name(self, block_name: str) -> int | None:
        block_name_map = {normalize_string_lm3(b.long_name): b.id for b in self.blocks if b.id}
        block_name_map.update({normalize_string_lm3(b.short_name): b.id for b in self.blocks if b.id})
        return block_name_map.get(normalize_string_lm3(block_name))

    def get_unicode_plane_by_number(self, plane_number: int) -> UnicodePlane:
        plane = self.plane_number_map.get(plane_number)
        if plane:
            return plane
        if plane_number >= 4 and plane_number <= 13:
            return self.get_undefined_plane(plane_number)
        return NULL_PLANE  # pragma: no cover

    def get_undefined_plane(self, plane_number: int) -> UnicodePlane:
        return UnicodePlane(
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

    def get_unicode_plane_by_abbreviation(self, plane_abbr: str) -> UnicodePlane:
        return self.plane_abbreviation_map.get(plane_abbr, NULL_PLANE)

    def get_unicode_plane_containing_block_id(self, block_id: int) -> UnicodePlane:
        found = [p for p in self.planes if p.start_block_id <= block_id and block_id <= p.finish_block_id]
        return found[0] if found else NULL_PLANE

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
                return self.non_unihan_character_name_map.get(codepoint, "")
            case CharacterType.UNIHAN | CharacterType.TANGUT:
                return self.get_generic_name_for_codepoint(codepoint)
            case CharacterType.INVALID:
                return f"Invalid Codepoint (U+{codepoint:04X})"
            case _:
                return f"<{char_type}-{codepoint:04X}>"

    def get_character_type(self, codepoint: int) -> CharacterType:
        if self.character_is_non_unihan(codepoint):
            return CharacterType.NON_UNIHAN
        if self.character_is_unihan(codepoint):
            return CharacterType.UNIHAN
        if self.character_is_tangut(codepoint):
            return CharacterType.TANGUT
        if self.codepoint_is_noncharacter(codepoint):
            return CharacterType.NONCHARACTER
        if self.codepoint_is_surrogate(codepoint):
            return CharacterType.SURROGATE  # pragma: no cover
        if self.codepoint_is_private_use(codepoint):
            return CharacterType.PRIVATE_USE
        if self.codepoint_is_in_unicode_space(codepoint):
            return CharacterType.RESERVED
        return CharacterType.INVALID

    def get_generic_name_for_codepoint(self, codepoint: int) -> str:
        block = self.get_unicode_block_containing_codepoint(codepoint)
        if block.id in self.cjk_unified_ideograph_block_ids:
            return f"CJK UNIFIED IDEOGRAPH-{codepoint:04X}"
        if block.id in self.cjk_compatibility_block_ids:
            return f"CJK COMPATIBILITY IDEOGRAPH-{codepoint:04X}"
        if block.id in self.tangut_ideograph_block_ids:
            return f"TANGUT IDEOGRAPH-{codepoint:04X}"
        if block.id in self.tangut_component_block_ids:
            return f"TANGUT COMPONENT-{self.get_tangut_component_index(codepoint):03}"
        return ""  # pragma: no cover

    def get_tangut_component_index(self, codepoint: int) -> int:
        tangut_components_block = self.get_unicode_block_by_id(list(self.tangut_component_block_ids)[0])
        # The Tangut component characters are one-indexed
        return (codepoint - tangut_components_block.start_dec) + 1

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
        return f"{chr(codepoint_dec)} (U+{codepoint_dec:04X} {self.get_character_name(codepoint_dec)})"

    def get_all_codepoints_in_block_id_list(self, block_id_list: set[int]) -> set[int]:
        blocks = [self.get_unicode_block_by_id(block_id) for block_id in block_id_list]
        return set(itertools.chain(*[list(range(block.start_dec, block.finish_dec + 1)) for block in blocks]))

    def get_all_values_for_property_group(self, prop_group: str) -> list["UnicodePropertyGroupValues"]:
        if prop_group == "Block":
            return json.loads(self.settings.blocks_json.read_text()) if self.settings.blocks_json.exists() else []
        prop_group_values: dict[str, UnicodePropertyGroupValues] | list[str] = self.property_value_id_map.get(
            prop_group, None
        )
        if not prop_group_values or not isinstance(prop_group_values, dict):  # pragma: no cover
            return []
        return [val for val in prop_group_values.values() if all(val["short_name"].lower() != s for s in ["n/a", "na"])]

    def get_property_value_ids_by_name(self, prop_group: str, prop_values: list[str]) -> list[Result[int]]:
        return [self.get_property_value_id_by_name(prop_group, value) for value in prop_values]

    def get_property_value_id_by_name(self, prop_group: str, prop_value: str) -> Result[int]:
        if prop_group in self.missing_property_groups:  # pragma: no cover
            return Result[int].Ok(PROP_GROUP_INVALID_FOR_VERSION_ROW_ID)
        name_value_map = self.get_name_value_map_for_property_group(prop_group)
        if not name_value_map:  # pragma: no cover
            return Result[int].Fail(f"Invalid property group: {prop_group}")
        prop_value_id = name_value_map.get(prop_value)
        if isinstance(prop_value_id, int):
            return Result[int].Ok(prop_value_id)
        return Result[int].Fail(f"Invalid {prop_group} value: {prop_value}")  # pragma: no cover

    def get_name_value_map_for_property_group(self, prop_group: str) -> dict[str, int] | None:
        prop_group_values: dict[str, UnicodePropertyGroupValues] | list[str] = self.property_value_id_map.get(
            prop_group, None
        )
        if not prop_group_values or not isinstance(prop_group_values, dict):  # pragma: no cover
            return None
        short_name_value_map = {value_map["short_name"]: value_map["id"] for value_map in prop_group_values.values()}
        long_name_value_map = {value_map["long_name"]: value_map["id"] for value_map in prop_group_values.values()}
        return short_name_value_map | long_name_value_map

    def get_display_name_for_property_value(
        self, prop_group: str, prop_value_id: int | None = None, codepoint: int | None = None
    ) -> str:
        if prop_group in self.missing_property_groups:  # pragma: no cover
            return "N/A"
        prop_group_values: dict[str, UnicodePropertyGroupValues] | list[str] = self.property_value_id_map.get(
            prop_group, None
        )
        if not prop_group_values or not isinstance(prop_group_values, dict):  # pragma: no cover
            return ""
        if prop_value_id is None:
            prop_value_id = self.get_default_value_id_for_property_group(prop_group, codepoint)
        value_map = prop_group_values.get(str(prop_value_id))
        if not value_map:  # pragma: no cover
            return ""
        return (
            value_map["short_name"] if prop_group == "Age" else f"{value_map['long_name']} ({value_map['short_name']})"
        )

    def get_default_value_id_for_property_group(self, prop_group: str, codepoint: int | None) -> int:
        if prop_group in self.missing_property_groups:  # pragma: no cover
            return PROP_GROUP_INVALID_FOR_VERSION_ROW_ID
        default_value = None
        if prop_group in (default_val_map := self.constant_default_property_value_map):
            default_value = default_val_map[prop_group]
        if not codepoint:  # pragma: no cover
            raise ValueError("Codepoint is required to determine default property value")
        if prop_group in (default_val_fn_map := self.variable_default_property_value_map):
            default_value = default_val_fn_map[prop_group](codepoint)
        if not default_value:  # pragma: no cover
            raise ValueError(f"Invalid property group: {prop_group}")
        result = self.get_property_value_id_by_name(prop_group, default_value)
        if result.success and result.value is not None:
            return result.value
        raise ValueError(result.error)  # pragma: no cover

    def get_default_age(self, codepoint: int) -> str:  # pragma: no cover
        block = self.get_unicode_block_containing_codepoint(codepoint)
        if block.plane and block.plane.abbreviation == "BMP":
            return "V1_1"
        elif block.plane:
            return "V2_0"
        return "NA"

    def get_default_bidi_class(self, codepoint: int) -> str:  # pragma: no cover
        if codepoint in DEFAULT_BC_R_CODEPOINTS:
            return "Right_To_Left"
        elif codepoint in DEFAULT_BC_AL_CODEPOINTS:
            return "Arabic_Letter"
        elif codepoint in DEFAULT_BC_ET_CODEPOINTS:
            return "European_Terminator"
        return "Left_To_Right"

    def get_default_eaw(self, codepoint: int) -> str:
        block = self.get_unicode_block_containing_codepoint(codepoint)
        if self.codepoint_is_private_use(codepoint):
            return "Ambiguous"
        elif (
            block.id in self.cjk_unified_ideograph_block_ids or block.id in self.cjk_compatibility_block_ids
        ):  # pragma: no cover
            return "Wide"
        return "Neutral"

    def get_default_general_category(self, codepoint: int) -> str:
        if self.codepoint_is_surrogate(codepoint):  # pragma: no cover
            return "Surrogate"
        elif self.codepoint_is_private_use(codepoint):
            return "Private_Use"
        return "Unassigned"

    def get_default_vo(self, codepoint: int) -> str:
        block = self.get_unicode_block_containing_codepoint(codepoint)
        if (
            block.plane
            and block.plane.number in DEFAULT_VO_U_PLANE_NUMBERS
            or block.id in self.get_default_vert_orient_upright_block_ids()
        ):
            return "Upright"
        return "Rotated"  # pragma: no cover

    def get_default_vert_orient_upright_block_ids(self) -> set[int]:
        return {
            block_id
            for block_name in DEFAULT_VO_U_BLOCK_NAMES
            if (block_id := self.loose_match_block_name(block_name)) is not None
        }

    def get_api_route_from_requested_path(self, requested_path: str) -> tuple[ApiRouteDetails, str]:
        for route in self.api_routes:
            if not (match := route["path_regex"].search(requested_path)):
                continue
            return (route, match.group(match.lastindex)) if match.lastindex else (route, "")
        return ({"name": "", "path": "", "path_regex": re.compile(r"")}, "")  # pragma: no cover


cached_data = UnicodeDataCache()
