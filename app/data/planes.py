from app.schemas.plane import UnicodePlane


def get_unicode_plane_containing_code_point(code_point: int) -> UnicodePlane:
    if 0 <= code_point and code_point <= 65535:
        return UnicodePlane(name="Basic Multilingual Plane", abbreviation="BMP", start=0, finish=65535)
    if 65536 <= code_point and code_point <= 131071:
        return UnicodePlane(name="Supplementary Multilingual Plane", abbreviation="SMP", start=65536, finish=131071)
    if 131072 <= code_point and code_point <= 196607:
        return UnicodePlane(name="Supplementary Ideographic Plane", abbreviation="SIP", start=131072, finish=196607)
    if 196608 <= code_point and code_point <= 917503:
        return UnicodePlane(name="Unassigned Codepoint", abbreviation="N/A", start=0, finish=0)
    if 917504 <= code_point and code_point <= 917999:
        return UnicodePlane(
            name="Supplement­ary Special-purpose Plane", abbreviation="SSP", start=917504, finish=917999
        )
    if 983040 <= code_point and code_point <= 1114111:
        return UnicodePlane(
            name="Supplement­ary Private Use Area planes", abbreviation="PUA", start=983040, finish=1114111
        )
    return UnicodePlane(name="Invalid Codepoint", abbreviation="N/A", start=0, finish=0)
