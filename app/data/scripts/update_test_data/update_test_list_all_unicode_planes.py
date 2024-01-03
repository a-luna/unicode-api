import json
from typing import Any

import app.db.models as db
from app.api.api_v1.endpoints.planes import list_all_unicode_planes
from app.config.api_settings import UnicodeApiSettings
from app.core.result import Result
from app.data.scripts.update_test_data.util import convert_prop_names_to_camel, pythonize_that_json

STATIC_CONTENT = """
UNASSIGNED_PLANE = {
    "number": 10,
    "name": "Unassigned Plane",
    "abbreviation": "N/A",
    "start": "U+A0000",
    "finish": "U+AFFFF",
    "totalAllocated": 0,
    "totalDefined": 0,
}
"""


def update_test_list_all_unicode_planes(settings: UnicodeApiSettings):
    planes = list_all_unicode_planes()
    planes["data"] = sanitize_planes_data(planes)
    planes = convert_prop_names_to_camel(planes)
    update_test_data_file(settings, planes)
    return Result.Ok()


def sanitize_planes_data(planes: dict[str, Any]) -> dict[str, Any]:
    valid_prop_names = [p for p, _ in db.UnicodePlaneResponse.model_fields.items()]
    return [
        {name: value for name, value in plane.model_dump().items() if name in valid_prop_names}
        for plane in planes["data"]
    ]


def update_test_data_file(settings: UnicodeApiSettings, planes: dict[str, Any]):
    test_data = construct_test_data_file(planes)
    test_data_file = (
        settings.TESTS_FOLDER.joinpath("test_plane_endpoints")
        .joinpath("test_list_all_unicode_planes")
        .joinpath("data.py")
    )
    test_data_file.write_text(test_data, encoding="utf-8")


def construct_test_data_file(planes: dict[str, Any]) -> str:
    planes_json = json.dumps(planes, indent=4, ensure_ascii=False)
    return f"ALL_PLANES = {pythonize_that_json(planes_json)}\n\n" + STATIC_CONTENT
