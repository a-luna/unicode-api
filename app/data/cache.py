import json
from functools import cached_property

from app.core.config import BLOCKS_JSON, CHAR_NAME_MAP, CHAR_NO_NAME_MAP, PLANES_JSON


class UnicodeDataCache:
    @cached_property
    def char_name_map(self) -> dict[int, str]:
        json_map = json.loads(CHAR_NAME_MAP.read_text())
        return {int(codepoint): name.lower() for (codepoint, name) in json_map.items()}

    @cached_property
    def char_no_name_map(self) -> dict[int, str]:
        json_map = json.loads(CHAR_NO_NAME_MAP.read_text())
        return {int(codepoint): name.lower() for (codepoint, name) in json_map.items()}

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

    def codepoint_is_assigned(self, codepoint: int) -> bool:
        return codepoint in self.all_codepoints


cached_data = UnicodeDataCache()
