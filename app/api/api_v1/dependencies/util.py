from fastapi import HTTPException, status

from app.constants import (
    ASCII_HEX,
    CP_NEED_LEADING_ZEROS_REGEX,
    CP_NO_PREFIX_REGEX_STRICT,
    CP_OUT_OF_RANGE_REGEX,
    CP_PREFIX_1_REGEX_STRICT,
    CP_PREFIX_2_REGEX_STRICT,
    MAX_CODEPOINT,
)
from app.core.encoding import get_codepoint_string
from app.core.result import Result
from app.core.util import s


def get_decimal_number_from_hex_codepoint(codepoint: str, starting_after: bool = True) -> int:
    result = get_codepoint_hex_from_string(codepoint)
    if result.failure:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.error)
    cp_hex = result.value or "0"
    cp_dec = int(cp_hex, 16)
    result = check_codepoint_is_in_unicode_range(cp_dec, starting_after)
    if result.success:
        return cp_dec
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.error)


def get_codepoint_hex_from_string(cp: str) -> Result[str]:
    if match := CP_PREFIX_1_REGEX_STRICT.match(cp):
        return Result.Ok(match[1])
    if match := CP_PREFIX_2_REGEX_STRICT.match(cp):
        return Result.Ok(match[1])
    if match := CP_NO_PREFIX_REGEX_STRICT.match(cp):
        return Result.Ok(match[1])
    return Result.Fail(get_error_message_for_invalid_codepoint_value(cp))


def check_codepoint_is_in_unicode_range(codepoint: int, starting_after: bool) -> Result[int]:
    lower_limit = 0 if starting_after else 1
    upper_limit = MAX_CODEPOINT if starting_after else MAX_CODEPOINT + 1
    if codepoint in range(lower_limit, upper_limit + 1):
        return Result.Ok(codepoint)
    error = f"{get_codepoint_string(codepoint)} is not within the Unicode codespace (U+0000 to U+10FFFF)."
    return Result.Fail(error)


def get_error_message_for_invalid_codepoint_value(cp: str) -> str:
    sanitized_codepoint = sanitize_codepoint_value(cp)
    if match := CP_NEED_LEADING_ZEROS_REGEX.search(cp):
        return (
            f"The value provided (U+{sanitized_codepoint.upper()}) is invalid because Unicode codepoint values "
            "prefixed with 'U+' must contain at least 4 hexadecimal digits. The correct way to request "
            f"the character assigned to codepoint 0x{match[1].upper()} is with the value "
            f"'{get_codepoint_string(int(match[1], 16))}', which adds the necessary leading zeros."
        )
    if invalid_chars := get_invalid_hex_characters(sanitized_codepoint):
        return (
            f"The value provided ({cp}) contains {len(invalid_chars)} invalid hexadecimal "
            f"character{s(invalid_chars)}: [{', '.join(invalid_chars)}]. The codepoint value must be expressed "
            "as a hexadecimal value within range 0000...10FFFF, optionally prefixed by 'U+'' or '0x'."
        )
    if match := CP_OUT_OF_RANGE_REGEX.match(cp):
        return (
            f"U+{match[1] or match[2]} is not within the range of valid codepoints for Unicode characters "
            "(U+0000 to U+10FFFF)."
        )
    return "Error! Value provided is not a valid hexadecimal number."


def sanitize_codepoint_value(codepoint: str) -> str:
    return codepoint[2:] if codepoint.startswith(("U+", "0x")) else codepoint


def get_invalid_hex_characters(s: str) -> list[str]:
    return sorted({char for char in s if char not in ASCII_HEX})
