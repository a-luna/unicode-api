from http import HTTPStatus

from fastapi import HTTPException

from app.schemas.plane import UnicodePlane


def get_unicode_plane_containing_codepoint(uni_char: str) -> UnicodePlane:
    if len(uni_char) != 1:
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail="This operation is only valid for strings containing a single character",
        )
    codepoint = ord(uni_char)
    if 0 <= codepoint and codepoint <= 65535:
        return UnicodePlane(name="Basic Multilingual Plane", abbreviation="BMP", start=0, finish=65535)
    if 65536 <= codepoint and codepoint <= 131071:
        return UnicodePlane(name="Supplementary Multilingual Plane", abbreviation="SMP", start=65536, finish=131071)
    if 131072 <= codepoint and codepoint <= 196607:
        return UnicodePlane(name="Supplementary Ideographic Plane", abbreviation="SIP", start=131072, finish=196607)
    if 917504 <= codepoint and codepoint <= 917999:
        return UnicodePlane(
            name="Supplement­ary Special-purpose Plane", abbreviation="SSP", start=917504, finish=917999
        )
    return UnicodePlane(name="Invalid Codepoint", abbreviation="N/A", start=0, end=0)
