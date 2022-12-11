# import json
# from http import HTTPStatus

# from fastapi import HTTPException

# from app.core.config import PLANES_JSON
# from app.data.constants import NULL_PLANE
# from app.data.unicode import get_unicode_planes
# from app.schemas import UnicodePlaneInternal

# ALL_CHARACTERS_PLANE = {
#     "number": -1,
#     "name": "All Unicode Characters",
#     "abbreviation": "ALL",
#     "start": "U+0000",
#     "start_dec": 0,
#     "finish": "U+10FFFF",
#     "finish_dec": 1114111,
#     "start_block_id": 1,
#     "finish_block_id": 327,
#     "total_allocated": 1114112,
#     "total_defined": 0,
# }

# unicode_planes = list(get_unicode_planes())


# def get_unicode_plane_containing_character(uni_char: str) -> UnicodePlaneInternal:
#     if len(uni_char) != 1:
#         raise HTTPException(
#             status_code=int(HTTPStatus.BAD_REQUEST),
#             detail="This operation is only valid for strings containing a single character",
#         )
#     codepoint = ord(uni_char)
#     found = [
#         plane for plane in unicode_planes.values() if plane.start_dec <= codepoint and codepoint <= plane.finish_dec
#     ]
#     return found[0] if found else NULL_PLANE


# def get_unicode_plane_containing_block_id(block_id: int) -> UnicodePlaneInternal:
#     found = [
#         plane
#         for plane in unicode_planes.values()
#         if plane.start_block_id <= block_id and block_id <= plane.finish_block_id
#     ]
#     return found[0] if found else NULL_PLANE


# def save_unicode_planes_to_json(planes: dict[str, str | int]):
#     PLANES_JSON.write_text(json.dumps(planes, indent=4))
