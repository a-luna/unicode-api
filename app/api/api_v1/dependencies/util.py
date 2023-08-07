from http import HTTPStatus

from fastapi import HTTPException

from app.core.result import Result
from app.data.constants import ASCII_HEX, MAX_CODEPOINT
from app.data.encoding import get_codepoint_string
from app.docs.dependencies.custom_parameters import (
    CODEPOINT_REGEX,
    CODEPOINT_WITHOUT_ZERO_PADDING_REGEX,
)


def get_decimal_number_from_hex_codepoint(codepoint: str, starting_after: bool = True) -> int:
    match = CODEPOINT_REGEX.match(codepoint)
    if not match:
        error = get_error_message_for_invalid_codepoint_value(codepoint)
        raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=error)
    groups = match.groupdict()
    codepoint_dec = int(groups.get("codepoint_prefix", "0") or groups.get("codepoint", "0"), 16)
    result = check_codepoint_is_in_unicode_range(codepoint_dec, starting_after)
    if result.success:
        return codepoint_dec
    raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=result.error)


def get_error_message_for_invalid_codepoint_value(codepoint: str) -> str:
    sanitized_codepoint = sanitize_codepoint_value(codepoint)
    if match := CODEPOINT_WITHOUT_ZERO_PADDING_REGEX.search(codepoint):
        return (
            f"The value provided (U+{sanitized_codepoint.upper()}) is invalid because Unicode codepoint values "
            "prefixed with 'U+' must contain at least 4 hexadecimal digits. The correct way to request "
            f"the character assigned to codepoint 0x{match[1].upper()} is with the value "
            f"'{get_codepoint_string(int(match[1], 16))}', which adds the necessary leading zeros."
        )

    invalid_chars = get_invalid_hex_characters(sanitized_codepoint)
    return (
        f"The value provided ({codepoint}) contains {len(invalid_chars)} invalid hexadecimal "
        f"character{'s' if len(invalid_chars) > 1 else ''}: [{', '.join(invalid_chars)}]."
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
    error = f"Codepoint {cp_hex} is not within the range of Unicode characters (U+0000 to U+10FFFF)."
    return Result.Fail(error)
