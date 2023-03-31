import re
from http import HTTPStatus

from fastapi import HTTPException, Path, Query

import app.db.engine as db
from app.core.config import settings
from app.data.cache import cached_data
from app.data.encoding import get_codepoint_string
from app.docs.dependencies import (
    BLOCK_NAME_VALUES_TABLE,
    GENERAL_CATEGORY_VALUES_TABLE,
    PROPERTY_GROUP_VALUES_TABLE,
    SCRIPT_CODE_VALUES_TABLE,
    UNICODE_AGE_VALUES_TABLE,
)
from app.schemas.enums import CharPropertyGroup, GeneralCategory, ScriptCode, UnicodeAge
from app.schemas.enums.block_name import UnicodeBlockName

CODEPOINT_REGEX = re.compile(r"(?:U\+(?P<codepoint_prefix>[A-Fa-f0-9]{4,6}))|(?:(0x)?(?P<codepoint>[A-Fa-f0-9]{2,6}))")
MAX_CODEPOINT = 1114111
MIN_SEARCH_RESULT_SCORE = 70

LIMIT_DESCRIPTION = """
<ul class="param-notes">
    <li>This value is optional (default: <code>limit=10</code>)</li>
</ul>
<p>A limit on the number of objects to be returned.</p>
"""

CODEPOINT_HEX_DESCRIPTION = """
<p>The <code>codepoint</code> property must be expressed as a hexadecimal value within range <code>0000...10FFFF</code>, optionally prefixed by <strong>U+</strong> or <strong>0x</strong>.</p>
"""

BLOCK_ID_DESCRIPTION = "The <code>id</code> property is an integer value within range <strong>1...327</strong>"

CODEPOINT_EXAMPLES = {
    "Default (No Value)": {"summary": "No Value (This value is optional)", "value": ""},
    "Codepoint (Standard Prefix)": {"summary": "With 'U+' Prefix", "value": "U+11FC0"},
    "Codepoint (No Prefix)": {"summary": "Without Prefix", "value": "11FC0"},
    "Codepoint (Hex Prefix)": {"summary": "With '0x' Prefix", "value": "0x11FC0"},
}

CODEPOINT_INVALID_ERROR = (
    "'Code point must be a hexadecimal value within range `0x00 - 0x10FFFF`, optionally prefixed by 'U+' or '0x'. "
    "For example, '72', 'U+0072, '0x72' and '0x0072' are valid ways to express the same code point. It is important "
    "to note that 'U+72' IS NOT valid because codepoints prefixed with 'U+' MUST be left-padded with zeroes to a "
    "minimum length of four digits."
)

UNICODE_CHAR_STRING_DESCRIPTION = f"""
<p>A string containing unicode characters, which can be expressed either directly (unencoded) or as a URI-encoded string. If you are unsure which format to use, please see the <strong>Examples</strong> below.</p>
<details>
    <summary>
        <div>
            <span>Examples with URI-Encoded Characters<sup>1</sup></span>
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                    <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                </svg>
            </div>
        </div>
    </summary>
    <dl class="param-examples">
        <dt><span>Ⱒ</span><sup>2</sup></dt>
        <dd><a href="{settings.API_ROOT}/v1/characters/%E2%B0%A2" rel="noopener noreferrer" target="_blank">%E2%B0%A2</a></dd>
        <dt><span>👨‍🌾 </span><sup>3</sup></dt>
        <dd><a href="{settings.API_ROOT}/v1/characters/%F0%9F%91%A8%E2%80%8D%F0%9F%8C%BE" rel="noopener noreferrer" target="_blank">%F0%9F%91%A8%E2%80%8D%F0%9F%8C%BE</a></dd>
    </dl>
    <div class="footnotes">
        <sup>1</sup>
        <p>These examples are implemented as links because Swagger UI doesn't handle URI-encoded string values correctly when used in the text-box below. Clicking either link will open a new tab, send a request, and display the response. You can also inspect the request/response data by opening the dev tools in the newly opened tab and refreshing the page.</p>
        <sup>2</sup>
        <p>This is an example of a single codepoint (<code>U+2C22</code>) that is URI-encoded.</p>
        <sup>3</sup>
        <p>This is an example of an emoji that is actually a combination of three codepoints (<code>U+1F468</code>, <code>U+200D</code>, <code>U+1F33E</code>) represented as a single URI-encoded string.</p>
    </div>
</details>
"""

UNICODE_CHAR_EXAMPLES = {
    "Character": {"summary": "Unencoded Character", "value": "𛱠"},
    "Emoji": {"summary": "Unencoded Emoji", "value": "🏃🏿‍♀️"},
}

BLOCK_NAME_DESCRIPTION = """
<p>The unique name assigned to each block of Unicode characters. In order to be used as a string enum value, a series of operations are performed on the block name:</p>
<ol>
    <li>Numbers and uppercase characters are left unchanged</li>
    <li>All lowercase characters are replaced with the uppercase version</li>
    <li>All remaining characters (e.g., whitespace, hyphens) are replaced by the underscore ("_") character.</li>
</ol>
"""

CHAR_SEARCH_BLOCK_NAME_DESCRIPTION = f"""
<ul class="param-notes">
    <li>This value is optional</li>
    <li class=\"loose-match\">The <a href="#loose-matching">Loose-matching rule</a> is applied to the value of this parameter</li>
</ul>
<p>if a valid block name is given, the response will only contain characters from that block. If this value  is not provided, the response will contain all characters in all blocks.</p>
<p>A list of the official names for all Unicode blocks is given below, click to expand:</p>
{BLOCK_NAME_VALUES_TABLE}
"""

PLANE_NAME_DESCRIPTION = """
<ul class="param-notes">
    <li>This value is optional</li>
</ul>
<p>The official name of a Unicode character plane (a plane is a continuous group of 65,536 (2<sup>16</sup>) codepoints). Only seven of the possible seventeen planes have an official name in the Unicode standard.</p>
<p>If a valid name is provided, the response will only contain blocks that exist within that plane. If this value is not provided, the response will contain all blocks in all planes.</p>
"""

SEARCH_CHAR_NAME_DESCRIPTION = """
<ul class="param-notes">
    <li class=\"loose-match\">The <a href="#loose-matching">Loose-matching rule</a> is applied to the value of this parameter</li>
</ul>
<p>Search for any unicode character by name. Exact matches are unnecessary since the search algorithm will return character names similar to the search term and provide a <strong>score</strong> value for each result.</p>
<p>For more information on this search behavior, see the <a href="#search">Search section</a> of the docs</p>
"""

SEARCH_BLOCK_NAME_DESCRIPTION = """
<p>Search for any unicode block by name. Exact matches are unnecessary since the search algorithm will return block names similar to the search term and provide a <strong>score</strong> value for each result.</p>
<p>You can restrict or expand your search based on the score value with the <strong>min_score</strong> parameter.</p>
"""

MIN_SCORE_DESCRIPTION = """
<ul class="param-notes">
    <li>This value is optional (default: <code>min_score=80</code>)</li>
</ul>
<p>A score between 0 and 100 (with 100 being a perfect match) that is calculated for each search result.</p>
<p>You can restrict or expand your search with this parameter. If your search isn't returning anything, try lowering the value of <strong>min_score</strong>.</p>
"""

PER_PAGE_DESCRIPTION = """
<ul class="param-notes">
    <li>This value is optional (default: <code>per_page=10</code>)</li>
</ul>
<p>The number of search results to include in each response, must be an integer in the range <strong>1...100</strong>.</p>
"""

PAGE_NUMBER_DESCRIPTION = """
<ul class="param-notes">
    <li>This value is optional (default: <code>page=1</code>)</li>
</ul>
<p>Used to request a specific page of search results. Each response includes a <code>hasMore</code> property. If your query generated more search results than the number specified in the <code>per_page</code> parameter, the <code>hasMore</code> property will be <code>True</code>. When the total number of search results is less than or equal to <code>per_page</code> or the requested page includes the last search result, <code>hasMore</code> will be <code>False</code>.</p>
<p>If <code>hasMore=True</code>, the response will contain a <code>nextPage</code> property. You can access the next set of search results by sending a subsequent request with <code>page</code> equal to <code>nextPage</code>.</p>
"""

CHAR_NAME_FILTER_DESCRIPTION = """
<ul class="param-notes">
    <li>This value is optional</li>
    <li class=\"alert\">This does not behave the same way that <strong><i>searching</i></strong> by <code>name</code> does for requests sent to the <code>/v1/characters/search</code> endpoint (i.e., fuzzy-searching is NOT performed)</li>
</ul>

<p>Filter Unicode characters by name. A character is considered a match if the official name of the character <strong>contains</strong> the value provided.</p>
"""


def get_description_and_values_table_for_property_group() -> str:
    return (
        '<ul class="param-notes">'
        + "<li>This value is optional (default: <code>show_props=Minimum</code>)</li>"
        + '<li class="loose-match">The <a href="#loose-matching">Loose-matching rule</a> is applied to the value of this parameter</li>'
        + "</ul>"
        + "<p>The full set of properties that are defined for each character in the Uhicode Standard is rather large, and sending every property in each response would be wasteful and inefficient. In order to make every property acessible while also prioritizing quick response times, you can request groups of properties to include using the <code>show_props</code> parameter.</p>"
        + '<p>For more information on property groups, including definitions for every property in each group, see the <a href="#unicodecharacter-property-groups"><code>UnicodeCharacter</code> Property Groups</a> section of the docs.</p>'
        + f"{PROPERTY_GROUP_VALUES_TABLE}"
        + "<p>For each group of properties to include in the response, click the button below and enter the value from the <strong>Property Group</strong> <i><u>or</u></i> <strong>Alias</strong> column of the table above.</p>"
    )


def get_description_and_values_table_for_unicode_age() -> str:
    return (
        '<ul class="param-notes">'
        + "<li>This value is optional</li>"
        + "</ul>"
        + "<p>Filter Unicode characters by <code>age</code>. Sending multiple values will return all characters that match any of the selected Unicode versions (e.g., sending <code>age=2.0</code> and <code>age=5.0</code> will return all characters that were assigned to a codepoint in <strong>either</strong> version 2.0 or 5.0.<p>"
        + "<p>You can view all version numbers of the Unicode Standard by expanding the section below:</p>"
        + f"{UNICODE_AGE_VALUES_TABLE}"
        + "<p>To add a filter setting for <code>age</code>, click the button below and enter a value from the list of Unicode version numbers.</p>"
    )


def get_filter_setting_description_general_category() -> str:
    return (
        '<ul class="param-notes">'
        + "<li>This value is optional</li>"
        + '<li class="loose-match">The <a href="#loose-matching">Loose-matching rule</a> is applied to the value of this parameter</li>'
        + "</ul>"
        + "<p>Filter Unicode characters by <code>general_category</code>. Sending multiple values will return all characters that match any of the selected catagories (e.g., sending <code>category=P</code> and <code>category=S</code> will return <strong>both</strong> Punctuation and Symbol characters).<p>"
        + "<p>You can view all possible general category codes by expanding the section below:</p>"
        + f"{GENERAL_CATEGORY_VALUES_TABLE}"
        + "<p>To add a filter setting for <code>general_category</code>, click the button below and enter a value from the <strong>Code</strong> column of the table above.</p>"
    )


def get_filter_setting_description_script_code() -> str:
    return (
        '<ul class="param-notes">'
        + "<li>This value is optional</li>"
        + '<li class="loose-match">The <a href="#loose-matching">Loose-matching rule</a> is applied to the value of this parameter</li>'
        + "</ul>"
        + "<p>Filter Unicode characters by <code>script</code>. Sending multiple values will return all characters that match any of the selected scripts (e.g., sending <code>script=Copt</code> and <code>script=Cyrl</code> will return <strong>both</strong> Greek and Coptic characters.<p>"
        + "<p>You can view all possible script codes by expanding the section below:</p>"
        + f"{SCRIPT_CODE_VALUES_TABLE}"
    )


def customize_ending_before_param_description(
    data_type: str, key_field: str, example_value: str, field_type_description: str
) -> str:
    return f"""
<ul class="param-notes">
    <li>This value is optional</li>
    <li class=\"alert\">Only one of <code>starting_after</code> or <code>ending_before</code> may be used in a request, sending a value for both parameters will produce a response with status <code>400 Bad Request</code>.</i></strong>.</li>
</ul>
<p>The <code>ending_before</code> parameter acts as a cursor to navigate between paginated responses, however, the value used for this parameter is different for each endpoint. <i><u>For Unicode {data_type}, the value of this parameter is the <code>{key_field}</code> property.</i></u></p>
<p>For example, if you previously requested 10 items beyond the first page of results, and the first search result of the current page has <code>{key_field}={example_value}</code>, you can retrieve the previous set of results by sending <code>ending_before={example_value}</code> in a subsequent request.</p>
<p>{field_type_description}</p>
"""


def customize_starting_after_param_description(
    data_type: str, key_field: str, example_value: str, field_type_description: str
) -> str:
    return f"""
<ul class="param-notes">
    <li>This value is optional</li>
    <li class=\"alert\">Only one of <code>starting_after</code> or <code>ending_before</code> may be used in a request, sending a value for both parameters will produce a response with status <code>400 Bad Request</code>.</i></strong>.</li>
</ul>
<p>The <code>starting_after</code> parameter acts as a cursor to navigate between paginated responses, however, the value used for this parameter is different for each endpoint. <i><u>For Unicode {data_type}, the value of this parameter is the <code>{key_field}</code> property.</i></u></p>
<p>For example, if you request 10 items and the response contains <code>hasMore=true</code>, there are more search results beyond the first 10. If the 10th search result has <code>{key_field}={example_value}</code>, you can retrieve the next set of results by sending <code>starting_after={example_value}</code> in a subsequent request.</p>
<p>{field_type_description}</p>
"""


ENDING_BEFORE_CODEPOINT_DESCRIPTION = customize_ending_before_param_description(
    "characters", "codepoint", "U+0431", CODEPOINT_HEX_DESCRIPTION
)
STARTING_AFTER_CODEPOINT_DESCRIPTION = customize_starting_after_param_description(
    "characters", "codepoint", "U+0409", CODEPOINT_HEX_DESCRIPTION
)

ENDING_BEFORE_BLOCK_ID_DESCRIPTION = customize_ending_before_param_description(
    "blocks", "id", "10", BLOCK_ID_DESCRIPTION
)
STARTING_AFTER_BLOCK_ID_DESCRIPTION = customize_starting_after_param_description(
    "blocks", "id", "140", BLOCK_ID_DESCRIPTION
)


def get_decimal_number_from_hex_codepoint(codepoint: str) -> int:
    match = CODEPOINT_REGEX.match(codepoint)
    if not match:
        raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=CODEPOINT_INVALID_ERROR)
    groups = match.groupdict()
    codepoint_dec = int(groups.get("codepoint_prefix", "0") or groups.get("codepoint", "0"), 16)
    if not cached_data.codepoint_is_in_unicode_range(codepoint_dec):
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail=(
                f"Codepoint {get_codepoint_string(codepoint_dec)} is not within the range of unicode "
                "characters (U+0000 to U+10FFFF)."
            ),
        )
    return codepoint_dec


class CharacterSearchParameters:
    def __init__(
        self,
        name: str = Query(description=SEARCH_CHAR_NAME_DESCRIPTION),
        min_score: int
        | None = Query(default=None, ge=MIN_SEARCH_RESULT_SCORE, le=100, description=MIN_SCORE_DESCRIPTION),
        per_page: int | None = Query(default=None, ge=1, le=100, description=PER_PAGE_DESCRIPTION),
        page: int | None = Query(default=None, ge=1, description=PAGE_NUMBER_DESCRIPTION),
    ):
        self.name = name
        self.min_score = min_score or 80
        self.per_page = per_page or 10
        self.page = page or 1


class BlockSearchParameters:
    def __init__(
        self,
        name: str = Query(description=SEARCH_BLOCK_NAME_DESCRIPTION),
        min_score: int | None = Query(default=None, ge=0, le=100, description=MIN_SCORE_DESCRIPTION),
        per_page: int | None = Query(default=None, ge=1, le=100, description=PER_PAGE_DESCRIPTION),
        page: int | None = Query(default=None, ge=1, description=PAGE_NUMBER_DESCRIPTION),
    ):
        self.name = name
        self.min_score = min_score or 80
        self.per_page = per_page or 10
        self.page = page or 1


class ListParameters:
    def __init__(
        self,
        limit: int = Query(default=None, ge=1, le=100, description=LIMIT_DESCRIPTION),
        starting_after: str
        | None = Query(
            default=None,
            description=STARTING_AFTER_CODEPOINT_DESCRIPTION,
            examples=CODEPOINT_EXAMPLES,
        ),
        ending_before: str
        | None = Query(
            default=None,
            description=ENDING_BEFORE_CODEPOINT_DESCRIPTION,
            examples=CODEPOINT_EXAMPLES,
        ),
    ):
        if ending_before and starting_after:
            raise HTTPException(
                status_code=int(HTTPStatus.BAD_REQUEST),
                detail=(
                    "Request contained values for BOTH 'ending_before' and 'starting_after', you must specify ONLY ONE "
                    "of these two values."
                ),
            )
        self.limit: int = limit or 10
        self.ending_before: int | None = get_decimal_number_from_hex_codepoint(ending_before) if ending_before else None
        self.starting_after: int | None = (
            get_decimal_number_from_hex_codepoint(starting_after) if starting_after else None
        )


class ListParametersDecimal:
    def __init__(
        self,
        limit: int = Query(default=None, ge=1, le=100, description=LIMIT_DESCRIPTION),
        starting_after: int
        | None = Query(
            default=None,
            ge=1,
            le=len(cached_data.blocks),
            description=STARTING_AFTER_BLOCK_ID_DESCRIPTION,
        ),
        ending_before: int
        | None = Query(
            default=None,
            ge=1,
            le=len(cached_data.blocks),
            description=ENDING_BEFORE_BLOCK_ID_DESCRIPTION,
        ),
    ):
        if ending_before and starting_after:
            raise HTTPException(
                status_code=int(HTTPStatus.BAD_REQUEST),
                detail=(
                    "Request contained values for BOTH 'ending_before' and 'starting_after', you must specify "
                    "ONLY ONE of these two values."
                ),
            )
        self.limit: int = limit or 10
        self.ending_before: int | None = ending_before
        self.starting_after: int | None = starting_after


class FilterParameters:
    def __init__(
        self,
        name: str | None = Query(default=None, description=CHAR_NAME_FILTER_DESCRIPTION),
        category: list[str] | None = Query(default=None, description=get_filter_setting_description_general_category()),
        age: list[str] | None = Query(default=None, description=get_description_and_values_table_for_unicode_age()),
        script: list[str] | None = Query(default=None, description=get_filter_setting_description_script_code()),
        show_props: list[str]
        | None = Query(default=None, description=get_description_and_values_table_for_property_group()),
        per_page: int | None = Query(default=None, ge=1, le=100, description=PER_PAGE_DESCRIPTION),
        page: int | None = Query(default=None, ge=1, description=PAGE_NUMBER_DESCRIPTION),
    ):
        self.name = name
        self.categories = parse_enum_values_from_parameter(GeneralCategory, "category", category) if category else None
        self.age_list = parse_enum_values_from_parameter(UnicodeAge, "age", age) if age else None
        self.scripts = parse_enum_values_from_parameter(ScriptCode, "script", script) if script else None
        self.show_props = (
            parse_enum_values_from_parameter(CharPropertyGroup, "show_props", show_props) if show_props else None
        )
        self.per_page = per_page or 10
        self.page = page or 1


def parse_enum_values_from_parameter(enum_class, param_name: str, values: list[str]):
    results = {str_val: enum_class.match_loosely(str_val) for str_val in values}
    invalid_results = [str_val for str_val, did_parse in results.items() if not did_parse]
    if invalid_results:
        needs_plural = len(invalid_results) > 1
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail=(
                f'{len(invalid_results)} value{"s" if needs_plural else ""} provided for the {param_name!r} '
                f'parameter {"are" if needs_plural else "is"} invalid: {invalid_results}'
            ),
        )
    return list(results.values())


class UnicodeBlockQueryParamResolver:
    def __init__(
        self,
        block: str | None = Query(default=None, description=CHAR_SEARCH_BLOCK_NAME_DESCRIPTION),
    ):
        self.block = loose_match_string_with_unicode_block_name(block) if block else cached_data.all_characters_block
        self.name = self.block.name
        self.start = self.block.start_dec
        self.finish = self.block.finish_dec


class UnicodeBlockPathParamResolver:
    def __init__(
        self,
        name: str = Path(default=..., description=BLOCK_NAME_DESCRIPTION),
    ):
        self.block = loose_match_string_with_unicode_block_name(name)
        self.name = self.block.name
        self.start = self.block.start_dec
        self.finish = self.block.finish_dec


def loose_match_string_with_unicode_block_name(name: str) -> db.UnicodeBlock:
    block_name = UnicodeBlockName.match_loosely(name)
    if not block_name:
        detail = f"{name!r} does not match any valid Unicode block name."
        fuzzy_matches = [
            cached_data.get_unicode_block_by_id(block_id).as_search_result(score)
            for (block_id, score) in cached_data.search_blocks_by_name(name, score_cutoff=72)
        ]
        if fuzzy_matches:
            detail += (
                " The following block names are similar to the name you provided: "
                f'{", ".join([str(b) for b in fuzzy_matches])}'
            )
        raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=detail)
    return cached_data.get_unicode_block_by_id(block_name.block_id)


class UnicodePlaneResolver:
    def __init__(
        self,
        plane: str | None = Query(default=None, description=PLANE_NAME_DESCRIPTION),
    ):
        self.plane = cached_data.get_unicode_plane_by_abbreviation(plane) if plane else cached_data.all_characters_plane
        if self.plane.name == "None":
            raise HTTPException(
                status_code=int(HTTPStatus.BAD_REQUEST),
                detail=(
                    f"{plane} does not match any valid Unicode plane abbreviation: BMP, SMP, SIP, TIP, SSP, SPUA-A, SPUA-B. "
                ),
            )
        self.start_block_id = self.plane.start_block_id
        self.finish_block_id = self.plane.finish_block_id
