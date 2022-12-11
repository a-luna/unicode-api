# unicode_chars = list(get_unicode_characters())
# unicode_blocks = list(get_unicode_blocks())
# block_name_map = {id: block.name for (id, block) in unicode_blocks.items()}
# name_lookup_map = {block.name: id for (id, block) in unicode_blocks.items()}


# def fuzzy_block_search(query: str, score_cutoff: int = 80) -> SearchResults[UnicodeBlockInternal]:
#     results = [
#         FuzzySearchResult[UnicodeBlockInternal](
#             value=unicode_blocks.get(result).start_dec, score=score, result=unicode_blocks.get(result)
#         )
#         for (_, score, result) in process.extract(query, block_name_map, limit=len(block_name_map))
#         if score >= score_cutoff
#     ]
#     print(f"query: {query}, score_cutoff: {score_cutoff}, results: {results}")
#     if results:
#         return generate_search_results(query, results)
#     return SearchResults[UnicodeBlockInternal](query=query, total_results=0, results_by_score=[])


# def generate_search_results(
#     query: str, results: list[FuzzySearchResult[UnicodeBlockInternal]]
# ) -> SearchResults[UnicodeBlockInternal]:
#     results_grouped = group_and_sort_list(results, "score", "value", sort_groups_desc=True)
#     results_by_score = [
#         ResultsForScore[UnicodeBlockInternal](
#             score=score,
#             total_results=len(results_with_score),
#             results=[res.result for res in results_with_score],
#         )
#         for (score, results_with_score) in results_grouped.items()
#     ]
#     return SearchResults[UnicodeBlockInternal](
#         query=query,
#         total_results=len(results),
#         results_by_score=results_by_score,
#     )


# def get_unicode_block_containing_character(uni_char: str) -> UnicodeBlockInternal:
#     if len(uni_char) != 1:
#         raise HTTPException(
#             status_code=int(HTTPStatus.BAD_REQUEST),
#             detail="This operation is only valid for strings containing a single character",
#         )
#     codepoint = ord(uni_char)
#     found = [
#         block for block in unicode_blocks.values() if block.start_dec <= codepoint and codepoint <= block.finish_dec
#     ]
#     return found[0] if found else NULL_BLOCK


# def find_all_characters_in_block(block: UnicodeBlockInternal) -> list[UnicodeCharacterInternal]:
#     return [
#         unicode_chars.get(codepoint)
#         for codepoint in range(block.start_dec, block.finish_dec)
#         if char_exists_in_database(codepoint)
#     ]


# def char_exists_in_database(codepoint: int) -> bool:
#     block_name = get_unicode_block_containing_character(chr(codepoint)).name
#     return True if block_name in VIRTUAL_CHAR_BLOCKS else codepoint in unicode_chars
