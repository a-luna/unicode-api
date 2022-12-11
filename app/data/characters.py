# import json
# import unicodedata
# from html.entities import html5

# from rapidfuzz import process

# from app.core.config import CHARACTERS_JSON, settings
# from app.core.util import get_codepoint_string, group_and_sort_list
# from app.data.blocks import (
#     CJK_COMPATIBILITY_BLOCKS,
#     CJK_UNIFIED_BLOCKS,
#     get_unicode_block_containing_character,
#     TANGUT_BLOCKS,
#     VAR_SELECTOR_BLOCKS,
# )
# from app.data.categories import (
#     get_bidirectional_category,
#     get_general_category,
#     get_class_category,
# )
# from app.data.constants import HTML_ENTITY_MAP, NULL_CHARACTER, NULL_CHARACTER_RESULT
# from app.data.planes import get_unicode_plane_containing_character
# from app.schemas import (
#     FuzzySearchResult,
#     ResultsForScore,
#     SearchResults,
#     UnicodeCharacterInternal,
#     UnicodeCharacterResult,
# )


# def build_char_name_map() -> dict[int, UnicodeCharacterInternal]:
#     return {int(d["codepoint"]): d["name"] for d in char_data}


# def build_html_entity_map():
#     codepoint_entity_map = [(ord(uni_char), entity) for (entity, uni_char) in html5.items() if len(uni_char) == 1]
#     return {cp: entity for (cp, entity) in sorted(codepoint_entity_map, key=lambda x: x[0])}


# char_data = json.loads(CHARACTERS_JSON.read_text())
# char_names = build_char_name_map()
# html_entity_map = build_html_entity_map()


# def fuzzy_character_search(
#     query: str, score_cutoff: int = 80
# ) -> SearchResults[ResultsForScore[UnicodeCharacterResult]]:
#     results = [
#         FuzzySearchResult[UnicodeCharacterResult](
#             value=result, score=score, result=get_character_details(chr(result), min_details=True)
#         )
#         for (_, score, result) in process.extract(query, char_names, limit=len(char_names))
#         if score >= score_cutoff
#     ]
#     if results:
#         return generate_search_results(query, results)
#     return SearchResults[UnicodeCharacterResult](query=query, total_results=0, results_by_score=[])


# def generate_search_results(
#     query: str, results: list[FuzzySearchResult[UnicodeCharacterResult]]
# ) -> SearchResults[UnicodeCharacterResult]:
#     results_grouped = group_and_sort_list(results, "score", "value", sort_groups_desc=True)
#     results_by_score = [
#         ResultsForScore[UnicodeCharacterResult](
#             score=score,
#             total_results=len(results_with_score),
#             results=([result.result for result in results_with_score]),
#         )
#         for (score, results_with_score) in results_grouped.items()
#     ]
#     return SearchResults[UnicodeCharacterResult](
#         query=query,
#         total_results=len(results),
#         results_by_score=results_by_score,
#     )


# def get_unicode_char_name(codepoint: int, block_name: str) -> str:
#     if block_name == "Invalid Codepoint":
#         return f"Invalid Codepoint ({get_codepoint_string(codepoint)})"
#     if block_name in CJK_UNIFIED_BLOCKS:
#         return f"CJK UNIFIED IDEOGRAPH-{codepoint:04X}"
#     if block_name in CJK_COMPATIBILITY_BLOCKS:
#         return f"CJK COMPATIBILITY IDEOGRAPH-{codepoint:04X}"
#     if block_name in TANGUT_BLOCKS:
#         return f"TANGUT IDEOGRAPH-{codepoint:04X}"
#     if block_name in VAR_SELECTOR_BLOCKS:
#         return f"VARIATION SELECTOR-{codepoint - 917743}"
#     char_name = char_names.get(codepoint)
#     return char_name if char_name else f"Undefined Codepoint ({get_codepoint_string(codepoint)}) (Reserved for {block_name})"


# def get_character_details(
#     char_data: dict[str, int | str], min_details: bool = False
# ) -> UnicodeCharacterResult | UnicodeCharacterInternal:
#     codepoint = int(char_data["codepoint"])
#     uni_char = chr(codepoint)
#     plane = get_unicode_plane_containing_character(uni_char)
#     block = //////////(uni_char)
#     if block.name == "Invalid Codepoint":
#         return NULL_CHARACTER_RESULT if min_details else NULL_CHARACTER
#     if min_details:
#         return UnicodeCharacterResult(
#             character=uni_char,
#             name=get_unicode_char_name(codepoint, block.name),
#             codepoint=get_codepoint_string(codepoint),
#             link=f"{settings.API_VERSION}/characters/{get_uri_encoded_value(uni_char)}",
#         )
#     new_char_data = {}
#     new_char_data["character"] = uni_char
#     new_char_data["name"] = get_unicode_char_name(codepoint, block.name)
#     new_char_data["codepoint_dec"] = codepoint
#     new_char_data["codepoint"] = get_codepoint_string(codepoint)
#     new_char_data["block"] = block.name
#     new_char_data["block_id"] = block.id
#     new_char_data["plane"] = plane.abbreviation
#     new_char_data["plane_number"] = plane.number
#     new_char_data["general_category"] = get_general_category(char_data["general_category"])
#     new_char_data["general_category_value"] = char_data["general_category"]

#     return UnicodeCharacterInternal(
#         character=uni_char,
#         name=get_unicode_char_name(codepoint, block.name),
#         codepoint_dec=codepoint,
#         codepoint=get_codepoint_string(codepoint),
#         block=block.name,
#         plane=get_unicode_plane_containing_character(uni_char).abbreviation,
#         category_value=unicodedata.category(uni_char),
#         category=get_general_category(unicodedata.category(uni_char)),
#         bidirectional_class_value=unicodedata.bidirectional(uni_char),
#         bidirectional_class=get_bidirectional_category(unicodedata.bidirectional(uni_char)),
#         combining_class_value=unicodedata.combining(uni_char),
#         combining_class=get_class_category(unicodedata.combining(uni_char)),
#         bidirectional_is_mirrored=unicodedata.mirrored(uni_char),
#         html_entities=get_html_entities(codepoint),
#         uri_encoded=get_uri_encoded_value(uni_char),
#         utf8_dec_bytes=get_utf8_dec_bytes(uni_char),
#         utf8_hex_bytes=get_utf8_hex_bytes(uni_char),
#         utf8=get_utf8_value(uni_char),
#         utf16=get_utf16_value(uni_char),
#         utf32=get_utf32_value(uni_char),
#     )


# def get_html_entities(codepoint: int) -> list[str]:
#     html_entities = [f"&#{codepoint};", f"&#x{codepoint:02X};"]
#     named_entity = HTML_ENTITY_MAP.get(codepoint)
#     if named_entity:
#         html_entities.append(f"&{named_entity}")
#     return html_entities


# def get_utf8_dec_bytes(uni_char: str) -> list[int]:
#     return list(uni_char.encode())


# def get_utf8_hex_bytes(uni_char: str) -> list[str]:
#     return [f"{x:02X}" for x in uni_char.encode()]


# def get_uri_encoded_value(uni_char: str) -> str:
#     return "".join(f"%{hex_byte}" for hex_byte in get_utf8_hex_bytes(uni_char))


# def get_utf8_value(uni_char: str) -> str:
#     return " ".join(f"0x{hex_byte}" for hex_byte in get_utf8_hex_bytes(uni_char))


# def get_utf16_value(uni_char: str) -> str:
#     hex_bytes = [f"{x:02X}" for x in uni_char.encode("utf_16_be")]
#     if len(hex_bytes) == 2:
#         return f"0x{hex_bytes[0]}{hex_bytes[1]}"
#     if len(hex_bytes) == 4:
#         return f"0x{hex_bytes[0]}{hex_bytes[1]} 0x{hex_bytes[2]}{hex_bytes[3]}"


# def get_utf32_value(uni_char: str) -> str:
#     return f"0x{ord(uni_char):08X}"


# def build_unicode_char_map() -> dict[int, UnicodeCharacterInternal]:
#     return {int(d["codepoint"]): get_character_details(d) for d in char_data}


# unicode_chars = build_unicode_char_map()
