import re
from http import HTTPStatus

from fastapi import Depends, HTTPException, Path, Query
from sqlalchemy.engine import Engine
from sqlmodel import Session

import app.core.db as db
from app.core.enums import UnicodeBlockName, UnicodePlaneName
from app.core.util import get_codepoint_string
from app.schemas.enums import CharPropertyGroup

CODEPOINT_REGEX = re.compile(r"(?:U\+(?P<codepoint_prefix>[A-Fa-f0-9]{4,6}))|(?:(0x)?(?P<codepoint>[A-Fa-f0-9]{2,6}))")
MAX_CODEPOINT = 1114111

LIMIT_DESCRIPTION = """
<p><i><strong><span>this value is optional (default: <strong>limit=10</strong>)</span></strong></i></p>
<p>A limit on the number of objects to be returned. <strong>limit</strong> is an integer value within range <strong>1...100</strong>.</p>
"""

MIN_DETAILS_DESCRIPTION = """
<p><i><strong><span>this value is optional (default: <strong>min_details=true</strong>)</span></strong></i></p>
<p>Flag that controls the level of detail for each character included in the response.</p>
<p>The default behavior (<strong>minDetails=<i>true</i></strong>), will return <strong>only the name and codepoint value</strong> for each character. Specifying <strong>minDetails=<i>false</i></strong> will return the full set of properties specified in the <a href="#swagger-ui"><i>Properties of the UnicodeCharacter Object</i></a> section at the top of this page.</p>
"""

CODEPOINT_HEX_DESCRIPTION = """
<p>The <strong>codepoint</strong> value must be expressed as a hexadecimal value within range <code>0000...10FFFF</code>, optionally prefixed by <strong>U+</strong> or <strong>0x</strong>.</p>
"""

BLOCK_ID_DESCRIPTION = "The <strong>id</strong> value is an integer value within range <strong>1...327</strong>"

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

UNICODE_CHAR_STRING_DESCRIPTION = """
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
    <dl>
        <dt><span>Ⱒ</span><sup>2</sup></dt>
        <dd><a href="/v1/characters/%E2%B0%A2" target="_blank">%E2%B0%A2</a></dd>
        <dt><span>👨‍🌾 </span><sup>3</sup></dt>
        <dd><a href="/v1/characters/%F0%9F%91%A8%E2%80%8D%F0%9F%8C%BE" target="_blank">%F0%9F%91%A8%E2%80%8D%F0%9F%8C%BE</a></dd>
    </dl>
    <div>
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

CHAR_SEARCH_BLOCK_NAME_DESCRIPTION = """
<p><i><strong><span>this value is optional</span></strong></i></p>
<p>if a valid block name is given, the response will only contain characters from that block. If this value  is not provided, the response will contain all characters in all blocks.</p>
"""

PLANE_NAME_DESCRIPTION = """
<p><i><strong><span>this value is optional</span></strong></i></p>
<p>The official name of a Unicode character plane (a plane is a continuous group of 65,536 (2<sup>16</sup>) codepoints). Only seven of the possible seventeen planes have an official name in the Unicode standard.</p>
<p><strong>This value is optional</strong>, if a valid name is provided, the response will only contain blocks that exist within that plane. If this value is not provided, the response will contain all blocks in all planes.</p>
"""

SEARCH_CHAR_NAME_DESCRIPTION = """
<p>Search for any unicode character by name. Exact matches are unnecessary since the search algorithm will return character names similar to the search term and provide a <strong>score</strong> value for each result. </p>
<p>You can restrict or expand your search based on the score value with the <strong>min_score</strong> parameter.</p>
"""

SEARCH_BLOCK_NAME_DESCRIPTION = """
<p>Search for any unicode block by name. Exact matches are unnecessary since the search algorithm will return block names similar to the search term and provide a <strong>score</strong> value for each result.</p>
<p>You can restrict or expand your search based on the score value with the <strong>min_score</strong> parameter.</p>
"""

MIN_SCORE_DESCRIPTION = """
<p><i><strong><span>this value is optional (default: <strong>min_score=80</strong>)</span></strong></i></p>
<p>A score between 0 and 100 (with 100 being a perfect match) is calculated for each search result. If your search isn't returning anything, try lowering the value of <strong>min_score</strong>.</p>
"""

PER_PAGE_DESCRIPTION = """
<p><i><strong><span>this value is optional (default: <strong>per_page=10</strong>)</span></strong></i></p>
<p>The number of search results to include in each response, must be an integer in the range <strong>1...100</strong>.</p>
"""

PAGE_NUMBER_DESCRIPTION = """
<p><i><strong><span>this value is optional (default: <strong>page=1</strong>)</span></strong></i></p>
<p>Used to request a specific page of search results. <i><strong>Do not include this parameter with your first search request.</strong></i></p>
<p>Each response includes a <strong>hasMore</strong> property. If your query generated more search results than the number specified in the <strong>per_page</strong> parameter, the <strong>hasMore</strong> property will be <code>True</code>. When the total number of search results is less than or equal to <strong>per_page</strong> <strong><i>OR</i></strong> the requested page includes the last search result, <strong>hasMore</strong> will be <code>False</code>.</p>
<p>If <strong>hasMore</strong>=<code>True</code>, the response will contain a <strong>nextPage</strong> property. You can access the next set of search results by sending a subsequent request with <strong>page</strong> equal to <strong>nextPage</strong>.</p>
"""


def customize_ending_before_param_description(
    id_field: str, example_value: str, field_type_description: str | None, hide_examples: bool
) -> str:
    description = f"""
<p><i><strong><span>this value is optional</span></strong></i></p>
<p>The <strong>ending_before</strong> parameter acts as a cursor to navigate between paginated responses.</p>
<p>The value of this parameter is an object ID. <strong>{id_field}</strong> is the property that acts as an object ID for this endpoint.</p>
<p>For example, if you previosly requested 10 items beyond the first page of results, and the first search result of the current page has <strong>{id_field}=<i>{example_value}</i></strong>, you can retrieve the previous set of results by sending <strong>ending_before=<i>{example_value}</i></strong> in a subsequent request.</p>
"""
    if field_type_description:
        description += f"<p>{field_type_description}</p>"
    if not hide_examples:
        description += "<p>Each of these different formats are shown below (these are also valid for the <strong>ending_before</strong> parameter):</p>"
    return description


def customize_starting_after_param_description(
    id_field: str, example_value: str, field_type_description: str | None, hide_examples: bool
) -> str:
    description = f"""
<p><i><strong><span>this value is optional</span></strong></i></p>
<p>The <strong>starting_after</strong> parameter acts as a cursor to navigate between paginated responses.</p>
<p>The value of this parameter is an object ID. <strong>{id_field}</strong> is the property that acts as an object ID for this endpoint.</p>
<p>For example, if you request 10 items and the response contains <strong>hasMore=<i>true</i></strong>, there are more search results beyond the first 10. If the 10th search result has <strong>{id_field}=<i>{example_value}</i></strong>, you can retrieve the next set of results by sending <strong>starting_after=<i>{example_value}</i></strong> in a subsequent request.</p>
"""
    if field_type_description:
        description += f"<p>{field_type_description}</p>"
    if not hide_examples:
        description += "<p>Each of these different formats are shown below (these are also valid for the <strong>ending_before</strong> parameter):</p>"
    return description


ENDING_BEFORE_CODEPOINT_DESCRIPTION = customize_ending_before_param_description(
    "codepoint", "U+0431", CODEPOINT_HEX_DESCRIPTION, True
)
STARTING_AFTER_CODEPOINT_DESCRIPTION = customize_starting_after_param_description(
    "codepoint", "U+0409", CODEPOINT_HEX_DESCRIPTION, False
)

ENDING_BEFORE_BLOCK_ID_DESCRIPTION = customize_ending_before_param_description("id", "10", BLOCK_ID_DESCRIPTION, True)
STARTING_AFTER_BLOCK_ID_DESCRIPTION = customize_starting_after_param_description(
    "id", "140", BLOCK_ID_DESCRIPTION, True
)


def get_decimal_number_from_hex_codepoint(codepoint: str) -> int:
    match = CODEPOINT_REGEX.match(codepoint)
    if not match:
        raise HTTPException(status_code=int(HTTPStatus.BAD_REQUEST), detail=CODEPOINT_INVALID_ERROR)
    groups = match.groupdict()
    codepoint_dec = int(groups.get("codepoint_prefix", "0") or groups.get("codepoint", "0"), 16)
    if codepoint_dec > MAX_CODEPOINT:
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail=(
                f"Codepoint {get_codepoint_string(codepoint_dec)} is not within the range of unicode "
                "characters (U+0000 to U+10FFFF)."
            ),
        )
    return codepoint_dec


def get_string_path_param(
    string: str = Path(description=UNICODE_CHAR_STRING_DESCRIPTION, examples=UNICODE_CHAR_EXAMPLES)
):
    if not string:
        raise HTTPException(
            status_code=int(HTTPStatus.BAD_REQUEST),
            detail="Invalid value, string must not be empty.",
        )
    return string


def get_min_details_query_param(min_details: bool = Query(default=None, description=MIN_DETAILS_DESCRIPTION)):
    return min_details if min_details is not None else True


def get_char_property_groups_query_param(show_props: list[CharPropertyGroup] | None = Query(default=None)):
    return show_props if show_props else [CharPropertyGroup.BASIC]


class CharacterSearchParameters:
    def __init__(
        self,
        name: str = Query(description=SEARCH_CHAR_NAME_DESCRIPTION),
        min_score: int | None = Query(default=None, ge=0, le=100, description=MIN_SCORE_DESCRIPTION),
        per_page: int | None = Query(default=None, ge=1, le=100, description=PER_PAGE_DESCRIPTION),
        page: int | None = Query(default=None, ge=1, description=PAGE_NUMBER_DESCRIPTION),
    ):
        self.name = name
        self.min_score = min_score or 80
        self.per_page = per_page or 10
        self.page = page or 1

    def __str__(self):
        return (
            "CharacterSearchParameters<"
            f'name="{self.name}", '
            f'min_score="{self.min_score}", '
            f'per_page="{self.per_page}", '
            f'page="{self.page}"'
            ">"
        )

    def __repr__(self):
        return str(self)


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

    def __str__(self):
        return (
            "BlockSearchParameters<"
            f'name="{self.name}", '
            f'min_score="{self.min_score}", '
            f'per_page="{self.per_page}", '
            f'page="{self.page}"'
            ">"
        )

    def __repr__(self):
        return str(self)


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
        ending_before: str | None = Query(default=None, description=ENDING_BEFORE_CODEPOINT_DESCRIPTION),
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

    def __str__(self):
        return (
            "ListParameters<"
            f'limit="{self.limit}", '
            f'starting_after="{self.starting_after}", '
            f'ending_before="{self.ending_before}"'
            ">"
        )

    def __repr__(self):
        return str(self)


class ListParametersDecimal:
    def __init__(
        self,
        limit: int = Query(default=None, ge=1, le=100, description=LIMIT_DESCRIPTION),
        starting_after: int | None = Query(default=None, description=STARTING_AFTER_BLOCK_ID_DESCRIPTION),
        ending_before: int | None = Query(default=None, description=ENDING_BEFORE_BLOCK_ID_DESCRIPTION),
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

    def __str__(self):
        return (
            "ListParametersDecimal<"
            f'limit="{self.limit}", '
            f'starting_after="{self.starting_after}", '
            f'ending_before="{self.ending_before}"'
            ">"
        )

    def __repr__(self):
        return str(self)


class UnicodeBlockQueryParamResolver:
    def __init__(
        self,
        block: UnicodeBlockName | None = Query(default=None, description=CHAR_SEARCH_BLOCK_NAME_DESCRIPTION),
        db_ctx: tuple[Session, Engine] = Depends(db.get_session),
    ):
        session, _ = db_ctx
        if not block:
            self.block: db.UnicodeBlock = get_all_characters_block(session)
        else:
            self.block: db.UnicodeBlock = (
                session.query(db.UnicodeBlock).filter(db.UnicodeBlock.id == block.block_id).one()
            )
        self.name = self.block.name
        self.start = self.block.start
        self.start_dec = self.block.start_dec
        self.finish = self.block.finish
        self.finish_dec = self.block.finish_dec

    def __str__(self):
        return (
            "UnicodeBlockQueryParamResolver<"
            f'block="{self.block.name}", '
            f'start="{self.start}", '
            f'finish="{self.finish}"'
            ">"
        )

    def __repr__(self):
        return str(self)


class UnicodeBlockPathParamResolver:
    def __init__(
        self,
        block: UnicodeBlockName | None = Path(default=None, description=BLOCK_NAME_DESCRIPTION),
        db_ctx: tuple[Session, Engine] = Depends(db.get_session),
    ):
        session, _ = db_ctx
        if not block:
            self.block: db.UnicodeBlock = get_all_characters_block(session)
            self.plane_abbrev = self.block.plane.abbreviation
        else:
            self.block: db.UnicodeBlock = (
                session.query(db.UnicodeBlock).filter(db.UnicodeBlock.id == block.block_id).one()
            )
            self.plane_abbrev = "ALL"
        self.name = self.block.name
        self.start = self.block.start
        self.start_dec = self.block.start_dec
        self.finish = self.block.finish
        self.finish_dec = self.block.finish_dec

    def __str__(self):
        return (
            "UnicodeBlockQueryParamResolver<"
            f'block="{self.block.name}", '
            f'start="{self.start}", '
            f'finish="{self.finish}"'
            ">"
        )

    def __repr__(self):
        return str(self)


class UnicodePlaneResolver:
    def __init__(
        self,
        plane: UnicodePlaneName | None = Query(default=None, description=PLANE_NAME_DESCRIPTION),
        db_ctx: tuple[Session, Engine] = Depends(db.get_session),
    ):
        session, _ = db_ctx
        if not plane:
            self.plane: db.UnicodePlane = get_all_characters_plane(session)
        else:
            self.plane: db.UnicodePlane = (
                session.query(db.UnicodePlane).filter(db.UnicodePlane.number == plane.number).one()
            )
        self.start_block_id = self.plane.start_block_id
        self.finish_block_id = self.plane.finish_block_id

    def __str__(self):
        return (
            "UnicodePlaneResolver<"
            f'plane="{self.plane.name}", '
            f'start="{self.start_block_id}", '
            f'finish="{self.finish_block_id}"'
            ">"
        )

    def __repr__(self):
        return str(self)


def get_all_characters_block(session: Session) -> db.UnicodeBlock:
    return db.UnicodeBlock(
        id=0,
        name="All Unicode Characters",
        plane_id=0,
        start_dec=0,
        start="U+0000",
        finish_dec=1114111,
        finish="U+10FFFF",
        total_allocated=1114112,
        total_defined=sum(len(block.characters) for block in session.query(db.UnicodeBlock).all()),
    )


def get_all_characters_plane(session: Session) -> db.UnicodePlane:
    return db.UnicodePlane(
        number=-1,
        name="All Unicode Characters",
        abbreviation="ALL",
        start="U+0000",
        start_dec=0,
        finish="U+10FFFF",
        finish_dec=1114111,
        start_block_id=1,
        finish_block_id=327,
        total_allocated=1114112,
        total_defined=sum(len(plane.characters) for plane in session.query(db.UnicodePlane).all()),
    )
