import re
from http import HTTPStatus

from fastapi import HTTPException

from app.core.result import Result
from app.data.constants import ASCII_HEX, MAX_CODEPOINT
from app.data.encoding import get_codepoint_string

CP_PREFIX_1_REGEX = re.compile(r"^U\+([A-Fa-f0-9]{4,6})$")
CP_PREFIX_2_REGEX = re.compile(r"^0x([A-Fa-f0-9]{2,6})$")
CP_NO_PREFIX_REGEX = re.compile(r"^([A-Fa-f0-9]{2,6})$")
CP_NEED_LEADING_ZEROS_REGEX = re.compile(r"^U\+([A-Fa-f0-9]{1,3})$")
CP_OUT_OF_RANGE_REGEX = re.compile(r"^(?:U\+)([A-Fa-f0-9]+)|(?:0x)?([A-Fa-f0-9]{7,})$")


def get_decimal_number_from_hex_codepoint(codepoint: str, starting_after: bool = True) -> int:
    result = get_codepoint_hex_from_string(codepoint)
    if result.failure:
        raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=result.error)
    cp_hex = result.value or "0"
    codepoint_dec = int(cp_hex, 16)
    result = check_codepoint_is_in_unicode_range(codepoint_dec, starting_after)
    if result.success:
        return codepoint_dec
    raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=result.error)


def get_codepoint_hex_from_string(s: str) -> Result[str]:
    match = CP_PREFIX_1_REGEX.match(s)
    if match:
        return Result.Ok(match[1])
    match = CP_PREFIX_2_REGEX.match(s)
    if match:
        return Result.Ok(match[1])
    match = CP_NO_PREFIX_REGEX.match(s)
    if match:
        return Result.Ok(match[1])
    return Result.Fail(get_error_message_for_invalid_codepoint_value(s))


def get_error_message_for_invalid_codepoint_value(s: str) -> str:
    sanitized_codepoint = sanitize_codepoint_value(s)
    if match := CP_NEED_LEADING_ZEROS_REGEX.search(s):
        return (
            f"The value provided (U+{sanitized_codepoint.upper()}) is invalid because Unicode codepoint values "
            "prefixed with 'U+' must contain at least 4 hexadecimal digits. The correct way to request "
            f"the character assigned to codepoint 0x{match[1].upper()} is with the value "
            f"'{get_codepoint_string(int(match[1], 16))}', which adds the necessary leading zeros."
        )
    invalid_chars = get_invalid_hex_characters(sanitized_codepoint)
    if invalid_chars:
        return (
            f"The value provided ({s}) contains {len(invalid_chars)} invalid hexadecimal "
            f"character{'s' if len(invalid_chars) > 1 else ''}: [{', '.join(invalid_chars)}]. "
            "The codepoint value must be expressed as a hexadecimal value within range 0000...10FFFF, "
            "optionally prefixed by 'U+'' or '0x'."
        )
    return (
        (
            f"U+{match[1] or match[2]} is not within the range of valid codepoints for Unicode characters "
            "(U+0000 to U+10FFFF)."
        )
        if (match := CP_OUT_OF_RANGE_REGEX.match(s))
        else "Error! Value provided is not a valid hexadecimal number."
    )


def sanitize_codepoint_value(codepoint: str) -> str:
    return codepoint[2:] if codepoint.startswith(("U+", "0x")) else codepoint


def get_invalid_hex_characters(s: str) -> list[str]:
    return sorted(list({char for char in s if char not in ASCII_HEX}))


def check_codepoint_is_in_unicode_range(codepoint: int, starting_after: bool) -> Result[int]:
    lower_limit = 0 if starting_after else 1
    upper_limit = MAX_CODEPOINT if starting_after else MAX_CODEPOINT + 1
    if codepoint in range(lower_limit, upper_limit + 1):
        return Result.Ok(codepoint)
    cp_hex = get_codepoint_string(codepoint)
    error = f"{cp_hex} is not within the range of valid codepoints for Unicode characters (U+0000 to U+10FFFF)."
    return Result.Fail(error)
