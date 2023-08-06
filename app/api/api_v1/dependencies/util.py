from http import HTTPStatus

from fastapi import HTTPException

from app.data.constants import MAX_CODEPOINT
from app.data.encoding import get_codepoint_string
from app.docs.dependencies.custom_parameters import (
    CODEPOINT_INVALID_ERROR,
    CODEPOINT_REGEX,
    CODEPOINT_WITHOUT_ZERO_PADDING_REGEX,
)


def get_decimal_number_from_hex_codepoint(codepoint: str, starting_after: bool = True) -> int:
    match = CODEPOINT_REGEX.match(codepoint)
    if not match:
        match = CODEPOINT_WITHOUT_ZERO_PADDING_REGEX.search(codepoint)
        if match:
            error = (
                f"The value provided ({codepoint.upper()}) is invalid because Unicode codepoint values "
                "prefixed with 'U+' must contain at least 4 hexadecimal digits. The correct way to request "
                f"the character assigned to codepoint 0x{match[1].upper()} is with the value "
                f"'{get_codepoint_string(int(match[1], 16))}', which adds the necessary leading zeros."
            )
            raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=error)
        else:
            raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=CODEPOINT_INVALID_ERROR)
    groups = match.groupdict()
    codepoint_dec = int(groups.get("codepoint_prefix", "0") or groups.get("codepoint", "0"), 16)
    lower_limit = 0 if starting_after else 1
    upper_limit = MAX_CODEPOINT if starting_after else MAX_CODEPOINT + 1
    if codepoint_dec in range(lower_limit, upper_limit + 1):
        return codepoint_dec
    raise HTTPException(
        status_code=int(HTTPStatus.BAD_REQUEST),
        detail=(
            f"Codepoint {get_codepoint_string(codepoint_dec)} is not within the range of Unicode "
            "characters (U+0000 to U+10FFFF)."
        ),
    )
