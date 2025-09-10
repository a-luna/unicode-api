import json
from typing import Any

from unicode_api.api.api_v1.endpoints.planes import list_all_unicode_planes
from unicode_api.config.api_settings import UnicodeApiSettings
from unicode_api.core.result import Result
from unicode_api.core.util import convert_keys_to_camel_case
from unicode_api.data.scripts.update_test_data.util import convert_json_to_python_literals

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


def update_test_list_all_unicode_planes(settings: UnicodeApiSettings) -> Result[None]:
    result = get_all_planes_response()
    if result.failure:
        return Result[None].Fail(result.error)
    data_all_planes = result.value or ""

    update_test_data_file(settings, data_all_planes)
    return Result[None].Ok()


def get_all_planes_response() -> Result[str]:
    response = list_all_unicode_planes()
    plane_data = response.get("data", [])
    if not plane_data or not isinstance(plane_data, list):
        return Result[str].Fail("Expected 'data' to be a list")
    formatted_data: dict[str, Any] = {
        **response,
        "data": [plane.model_dump() for plane in plane_data],
    }
    formatted_data = convert_keys_to_camel_case(formatted_data)
    converted_data = convert_json_to_python_literals(json.dumps(formatted_data, indent=4, ensure_ascii=False))
    return Result[str].Ok(converted_data)


def update_test_data_file(settings: UnicodeApiSettings, data_all_planes: str):
    test_data = f"ALL_PLANES = {data_all_planes}\n\n" + STATIC_CONTENT
    test_data_file = (
        settings.tests_folder.joinpath("test_plane_endpoints")
        .joinpath("test_list_all_unicode_planes")
        .joinpath("data.py")
    )
    test_data_file.write_text(test_data, encoding="utf-8")
