import json
from typing import Any

from fastapi import HTTPException

from app.api.api_v1.dependencies import ListParametersDecimal, UnicodePlaneResolver
from app.api.api_v1.endpoints.blocks import get_block_list_endpoints
from app.config.api_settings import UnicodeApiSettings
from app.core.result import Result
from app.data.scripts.update_test_data.util import pythonize_that_json

STATIC_CONTENT_1 = """
PLANE_BMP_START_AFTER_57_LIMIT_20 = {
    "url": "/v1/blocks",
    "hasMore": True,
    "data": [
        {
            "id": 58,
            "name": "Combining Diacritical Marks Extended",
            "plane": "BMP",
            "start": "U+1AB0",
            "finish": "U+1AFF",
            "totalAllocated": 80,
            "totalDefined": 31,
        },
        {
            "id": 59,
            "name": "Balinese",
            "plane": "BMP",
            "start": "U+1B00",
            "finish": "U+1B7F",
            "totalAllocated": 128,
            "totalDefined": 124,
        },
        {
            "id": 60,
            "name": "Sundanese",
            "plane": "BMP",
            "start": "U+1B80",
            "finish": "U+1BBF",
            "totalAllocated": 64,
            "totalDefined": 64,
        },
        {
            "id": 61,
            "name": "Batak",
            "plane": "BMP",
            "start": "U+1BC0",
            "finish": "U+1BFF",
            "totalAllocated": 64,
            "totalDefined": 56,
        },
        {
            "id": 62,
            "name": "Lepcha",
            "plane": "BMP",
            "start": "U+1C00",
            "finish": "U+1C4F",
            "totalAllocated": 80,
            "totalDefined": 74,
        },
        {
            "id": 63,
            "name": "Ol Chiki",
            "plane": "BMP",
            "start": "U+1C50",
            "finish": "U+1C7F",
            "totalAllocated": 48,
            "totalDefined": 48,
        },
        {
            "id": 64,
            "name": "Cyrillic Extended-C",
            "plane": "BMP",
            "start": "U+1C80",
            "finish": "U+1C8F",
            "totalAllocated": 16,
            "totalDefined": 9,
        },
        {
            "id": 65,
            "name": "Georgian Extended",
            "plane": "BMP",
            "start": "U+1C90",
            "finish": "U+1CBF",
            "totalAllocated": 48,
            "totalDefined": 46,
        },
        {
            "id": 66,
            "name": "Sundanese Supplement",
            "plane": "BMP",
            "start": "U+1CC0",
            "finish": "U+1CCF",
            "totalAllocated": 16,
            "totalDefined": 8,
        },
        {
            "id": 67,
            "name": "Vedic Extensions",
            "plane": "BMP",
            "start": "U+1CD0",
            "finish": "U+1CFF",
            "totalAllocated": 48,
            "totalDefined": 43,
        },
        {
            "id": 68,
            "name": "Phonetic Extensions",
            "plane": "BMP",
            "start": "U+1D00",
            "finish": "U+1D7F",
            "totalAllocated": 128,
            "totalDefined": 128,
        },
        {
            "id": 69,
            "name": "Phonetic Extensions Supplement",
            "plane": "BMP",
            "start": "U+1D80",
            "finish": "U+1DBF",
            "totalAllocated": 64,
            "totalDefined": 64,
        },
        {
            "id": 70,
            "name": "Combining Diacritical Marks Supplement",
            "plane": "BMP",
            "start": "U+1DC0",
            "finish": "U+1DFF",
            "totalAllocated": 64,
            "totalDefined": 64,
        },
        {
            "id": 71,
            "name": "Latin Extended Additional",
            "plane": "BMP",
            "start": "U+1E00",
            "finish": "U+1EFF",
            "totalAllocated": 256,
            "totalDefined": 256,
        },
        {
            "id": 72,
            "name": "Greek Extended",
            "plane": "BMP",
            "start": "U+1F00",
            "finish": "U+1FFF",
            "totalAllocated": 256,
            "totalDefined": 233,
        },
        {
            "id": 73,
            "name": "General Punctuation",
            "plane": "BMP",
            "start": "U+2000",
            "finish": "U+206F",
            "totalAllocated": 112,
            "totalDefined": 111,
        },
        {
            "id": 74,
            "name": "Superscripts and Subscripts",
            "plane": "BMP",
            "start": "U+2070",
            "finish": "U+209F",
            "totalAllocated": 48,
            "totalDefined": 42,
        },
        {
            "id": 75,
            "name": "Currency Symbols",
            "plane": "BMP",
            "start": "U+20A0",
            "finish": "U+20CF",
            "totalAllocated": 48,
            "totalDefined": 33,
        },
        {
            "id": 76,
            "name": "Combining Diacritical Marks for Symbols",
            "plane": "BMP",
            "start": "U+20D0",
            "finish": "U+20FF",
            "totalAllocated": 48,
            "totalDefined": 33,
        },
        {
            "id": 77,
            "name": "Letterlike Symbols",
            "plane": "BMP",
            "start": "U+2100",
            "finish": "U+214F",
            "totalAllocated": 80,
            "totalDefined": 80,
        },
    ],
}

ALL_BLOCKS_ENDING_BEFORE_171_LIMIT_15 = {
    "url": "/v1/blocks",
    "hasMore": True,
    "data": [
        {
            "id": 156,
            "name": "Arabic Presentation Forms-A",
            "plane": "BMP",
            "start": "U+FB50",
            "finish": "U+FDFF",
            "totalAllocated": 688,
            "totalDefined": 631,
        },
        {
            "id": 157,
            "name": "Variation Selectors",
            "plane": "BMP",
            "start": "U+FE00",
            "finish": "U+FE0F",
            "totalAllocated": 16,
            "totalDefined": 16,
        },
        {
            "id": 158,
            "name": "Vertical Forms",
            "plane": "BMP",
            "start": "U+FE10",
            "finish": "U+FE1F",
            "totalAllocated": 16,
            "totalDefined": 10,
        },
        {
            "id": 159,
            "name": "Combining Half Marks",
            "plane": "BMP",
            "start": "U+FE20",
            "finish": "U+FE2F",
            "totalAllocated": 16,
            "totalDefined": 16,
        },
        {
            "id": 160,
            "name": "CJK Compatibility Forms",
            "plane": "BMP",
            "start": "U+FE30",
            "finish": "U+FE4F",
            "totalAllocated": 32,
            "totalDefined": 32,
        },
        {
            "id": 161,
            "name": "Small Form Variants",
            "plane": "BMP",
            "start": "U+FE50",
            "finish": "U+FE6F",
            "totalAllocated": 32,
            "totalDefined": 26,
        },
        {
            "id": 162,
            "name": "Arabic Presentation Forms-B",
            "plane": "BMP",
            "start": "U+FE70",
            "finish": "U+FEFF",
            "totalAllocated": 144,
            "totalDefined": 141,
        },
        {
            "id": 163,
            "name": "Halfwidth and Fullwidth Forms",
            "plane": "BMP",
            "start": "U+FF00",
            "finish": "U+FFEF",
            "totalAllocated": 240,
            "totalDefined": 225,
        },
        {
            "id": 164,
            "name": "Specials",
            "plane": "BMP",
            "start": "U+FFF0",
            "finish": "U+FFFF",
            "totalAllocated": 16,
            "totalDefined": 5,
        },
        {
            "id": 165,
            "name": "Linear B Syllabary",
            "plane": "SMP",
            "start": "U+10000",
            "finish": "U+1007F",
            "totalAllocated": 128,
            "totalDefined": 88,
        },
        {
            "id": 166,
            "name": "Linear B Ideograms",
            "plane": "SMP",
            "start": "U+10080",
            "finish": "U+100FF",
            "totalAllocated": 128,
            "totalDefined": 123,
        },
        {
            "id": 167,
            "name": "Aegean Numbers",
            "plane": "SMP",
            "start": "U+10100",
            "finish": "U+1013F",
            "totalAllocated": 64,
            "totalDefined": 57,
        },
        {
            "id": 168,
            "name": "Ancient Greek Numbers",
            "plane": "SMP",
            "start": "U+10140",
            "finish": "U+1018F",
            "totalAllocated": 80,
            "totalDefined": 79,
        },
        {
            "id": 169,
            "name": "Ancient Symbols",
            "plane": "SMP",
            "start": "U+10190",
            "finish": "U+101CF",
            "totalAllocated": 64,
            "totalDefined": 14,
        },
        {
            "id": 170,
            "name": "Phaistos Disc",
            "plane": "SMP",
            "start": "U+101D0",
            "finish": "U+101FF",
            "totalAllocated": 48,
            "totalDefined": 46,
        },
    ],
}
"""

STATIC_CONTENT_2 = """
BOTH_START_AFTER_END_BEFORE_INVALID = {
    "detail": "Request contained values for BOTH 'ending_before' and 'starting_after', you must specify ONLY ONE of these two values."
}

INALID_PLANE_ABBREVIATION = {
    "detail": "BDP does not match any Unicode plane abbreviation: BMP, SMP, SIP, TIP, SSP, SPUA-A, SPUA-B."
}
"""


def update_test_list_all_unicode_blocks(settings: UnicodeApiSettings):
    result = get_error_detail()
    if result.failure:
        return result
    response = {"detail": result.value}
    update_test_data_file(settings, response)
    return Result.Ok()


def get_error_detail() -> Result[str]:
    plane = UnicodePlaneResolver(plane="TIP")
    list_params = ListParametersDecimal(limit=15, starting_after=20)
    try:
        _ = get_block_list_endpoints(list_params, plane)
        return Result.Fail("Expected an HTTPException to be raised")
    except HTTPException as ex:
        return Result.Ok(ex.detail)


def update_test_data_file(settings: UnicodeApiSettings, response: dict[str, Any]):
    test_data = construct_test_data_file(response)
    test_data_file = (
        settings.TESTS_FOLDER.joinpath("test_block_endpoints")
        .joinpath("test_list_all_unicode_blocks")
        .joinpath("data.py")
    )
    test_data_file.write_text(test_data, encoding="utf-8")


def construct_test_data_file(response: dict[str, Any]):
    response_json = json.dumps(response, indent=4, ensure_ascii=False)
    return (
        f"{STATIC_CONTENT_1}\n\n"
        + f"PLANE_TIP_START_AFTER_20_LIMIT_15 = {pythonize_that_json(response_json)}\n\n"
        + STATIC_CONTENT_2
    )
