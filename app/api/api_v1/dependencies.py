from http import HTTPStatus

from fastapi import Depends, HTTPException, Path, Query

from app.core.constants import CODE_POINT_REGEX, MAX_CODE_POINT
from app.core.util import get_code_point_string

CODE_POINT_DESCRIPTION = (
    "Hexadecimal value within range `0x0000 - 0x10FFFF`, optionally prefixed by **U+** or **0x**."
)
CODE_POINT_EXAMPLES = {
    "Codepoint (Standard Prefix)": {"summary": "With 'U+' Prefix", "value": "U+11FC0"},
    "Codepoint (No Prefix)": {"summary": "Without Prefix", "value": "11FC0"},
    "Codepoint (Hex Prefix)": {"summary": "With '0x' Prefix", "value": "0x11FC0"},
}

UNICODE_CHAR_DESCRIPTION = (
    "A string containing unicode characters, which can be expressed either directly (unencoded) or as a "
    "UTF-8 encoded string. If you are unsure which format to use, please see the **Examples** below."
)

UNICODE_CHAR_EXAMPLES = {
    "Character": {"summary": "Unencoded Character", "value": "𛱠"},
    "UTF-8 Encoded Character": {
        "summary": "UTF-8 Encoded Character (works in address bar, not on this form)",
        "value": "%E2%B0%A2",
    },
    "Emoji": {"summary": "Emoji", "value": "🏃🏿‍♀️"},
    "UTF-8 Encoded Emoji": {
        "summary": "UTF-8 Encoded Emoji (works in address bar, not on this form)",
        "value": "%F0%9F%8F%83%F0%9F%8F%BF%E2%80%8D%E2%99%80%EF%B8%8F",
    },
}

CODEPOINT_DESCRIPTION = "Decimal (Base-10) value within range `0-1114111`"

UNICODE_STRING_DESCRPITION = (
    "Arbirary string value. Response will include a list of characters from the provided string along with "
    "their assigned unicode block."
)


def get_char_from_hex_code_point(code_point: str | None):  # noqa:B008
    if code_point:
        match = CODE_POINT_REGEX.match(code_point)
        if not match:
            raise HTTPException(
                status_code=int(HTTPStatus.BAD_REQUEST),
                detail=(
                    "'Code point must be a hexadecimal value within range `0x0000 - 0x10FFFF`, optionally prefixed by 'U+' or '0x'. "
                    "For example, '72', 'U+0072' and '0x72' are valid and equivalent values for the same code point."
                ),
            )
        groups = match.groupdict()
        code_point_int = int(groups.get("code_point_prefix") or groups.get("code_point"), 16)
        if code_point_int > MAX_CODE_POINT:
            raise HTTPException(
                status_code=int(HTTPStatus.BAD_REQUEST),
                detail=(
                    f"Codepoint {get_code_point_string(code_point_int)} is not within the range of unicode characters "
                    "(U+0000 to U+10FFFF)."
                ),
            )
        return chr(code_point_int)


def get_char_from_hex_code_point_path_param(
    code_point: str = Path(description=CODE_POINT_DESCRIPTION, examples=CODE_POINT_EXAMPLES)  # noqa:B008)
):
    return get_char_from_hex_code_point(code_point)


def get_char_from_hex_code_point_query_param(
    code_point_hex: str | None = Query(default=None, description=CODE_POINT_DESCRIPTION, examples=CODE_POINT_EXAMPLES)
):
    if code_point_hex:
        return get_char_from_hex_code_point(code_point_hex)


def get_single_char(char: str = Path(description=UNICODE_CHAR_DESCRIPTION, examples=UNICODE_CHAR_EXAMPLES)):  # noqa:B0
    if not char:
        raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail="Invalid value, string must not be empty.")
    return char


def get_query_params(
    code_point_int: int
    | None = Query(default=None, ge=0, le=MAX_CODE_POINT, description=CODEPOINT_DESCRIPTION),  # noqa: B008
    code_point_hex: str | None = Depends(get_char_from_hex_code_point_query_param),  # noqa:B008)
    s: str | None = Query(default=None, description=UNICODE_STRING_DESCRPITION),  # noqa: B008
):
    char_list: str = ""
    if code_point_int:
        char_list += chr(code_point_int)
    if code_point_hex:
        char_list += code_point_hex
    if s:
        char_list += s
    if not char_list:
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail="Request did not include any character data",
        )
    return char_list
