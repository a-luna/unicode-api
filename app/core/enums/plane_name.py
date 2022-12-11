import json
from enum import auto

from fastapi_utils.enums import StrEnum

from app.core.config import PLANES_JSON
from app.schemas import UnicodePlaneInternal

unicode_planes = [
    UnicodePlaneInternal(**plane) for plane in json.loads(PLANES_JSON.read_text())
]
plane_name_map = {plane.name: plane for plane in unicode_planes}


class UnicodePlaneName(StrEnum):

    BASIC_MULTILINGUAL_PLANE = auto()
    SUPPLEMENTARY_MULTILINGUAL_PLANE = auto()
    SUPPLEMENTARY_IDEOGRAPHIC_PLANE = auto()
    TERTIARY_IDEOGRAPHIC_PLANE = auto()
    SUPPLEMENTARY_SPECIAL_PURPOSE_PLANE = auto()
    SUPPLEMENTARY_PRIVATE_USE_AREA_A = auto()
    SUPPLEMENTARY_PRIVATE_USE_AREA_B = auto()

    def __str__(self) -> str:
        plane = plane_name_map.get(self.print_name)
        return plane.abbreviation

    def __repr__(self):
        return f'UnicodePlaneName<name="{self.print_name}">'

    @property
    def abbreviation(self) -> str:
        return str(self)

    @property
    def print_name(self) -> str:
        print_names = {
            "BASIC_MULTILINGUAL_PLANE": "Basic Multilingual Plane",
            "SUPPLEMENTARY_MULTILINGUAL_PLANE": "Supplementary Multilingual Plane",
            "SUPPLEMENTARY_IDEOGRAPHIC_PLANE": "Supplementary Ideographic Plane",
            "TERTIARY_IDEOGRAPHIC_PLANE": "Tertiary Ideographic Plane",
            "SUPPLEMENTARY_SPECIAL_PURPOSE_PLANE": "Supplementary Special-purpose Plane",
            "SUPPLEMENTARY_PRIVATE_USE_AREA_A": "Supplementary Private Use Area-A",
            "SUPPLEMENTARY_PRIVATE_USE_AREA_B": "Supplementary Private Use Area-B",
        }
        return print_names.get(self.name)

    @property
    def number(self) -> int:
        plane = plane_name_map.get(self.print_name)
        return plane.number

    @classmethod
    def from_abbreviation(cls, abbrev):
        for enum_item in cls:
            if abbrev.upper() == str(enum_item):
                return enum_item

    @classmethod
    def from_number(cls, number):
        for enum_item in cls:
            if number == enum_item.number:
                return enum_item
