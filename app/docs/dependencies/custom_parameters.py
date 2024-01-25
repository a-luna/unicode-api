from app.config.api_settings import get_settings
from app.data.cache import cached_data
from app.data.encoding import get_uri_encoded_value
from app.docs.dependencies import (
    BIDI_CLASS_VALUES_TABLE,
    BLOCK_NAME_NO_LEGEND_TABLE,
    BLOCK_NAME_VALUES_TABLE,
    CCC_VALUES_TABLE,
    CHAR_FLAGS_TABLE,
    DECOMP_TYPE_VALUES_TABLE,
    GENERAL_CATEGORY_VALUES_TABLE,
    JOINING_TYPES_TABLE,
    LINE_BREAK_TYPE_VALUES_TABLE,
    NUMERIC_TYPES_TABLE,
    PROPERTY_GROUP_VALUES_TABLE,
    SCRIPT_CODE_VALUES_TABLE,
    UNICODE_AGE_VALUES_TABLE,
)

MIN_SEARCH_RESULT_SCORE = 70

LIMIT_DESCRIPTION = """
<ul class="param-notes">
    <li>This value is optional (default: <code>limit=10</code>)</li>
</ul>
<p>A limit on the number of objects to be returned.</p>
"""

CODEPOINT_HEX_DESCRIPTION = """
<p>The <code>codepoint</code> property must be expressed as a hexadecimal value within range <code>0000...10FFFF</code>, optionally prefixed by <code>U+</code> or <code>0x</code>.</p>
"""

BLOCK_ID_DESCRIPTION = (
    f"The <code>id</code> property is an integer value within range <strong>1...{len(cached_data.blocks)}</strong>"
)

CODEPOINT_EXAMPLES = """
<details>
    <summary>
        <div>
            <span>Examples: Character Codepoint Values</span>
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                    <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                </svg>
            </div>
        </div>
    </summary>
    <dl class="param-examples">
        <dt>Codepoint without prefix</dt>
        <dd>✅<code>72</code>, ✅<code>11FC0</code></dd>
        <dt>Codepoint with 'U+' prefix</dt>
        <dd>✅<code>U+0072</code>, ✅<code>U+11FC0</code>, ❌<code>U+72</code></dd>
        <dt>Codepoint with '0x' prefix</dt>
        <dd>✅<code>0x72</code>, ✅<code>0x0072</code>, ✅<code>0x11FC0</code></dd>
    </dl>
</details>
"""

CODEPOINT_INVALID_ERROR = (
    "'Code point must be a hexadecimal value within range `0x00 - 0x10FFFF`, optionally prefixed by 'U+' or '0x'. "
    "For example, '72', 'U+0072, '0x72' and '0x0072' are valid ways to express the same code point. It is important "
    "to note that 'U+72' IS NOT valid because codepoints prefixed with 'U+' MUST be left-padded with zeroes to a "
    "minimum length of four digits."
)

UNICODE_CHAR_NORMAL_EXAMPLES = """
<details id="normal-char-examples">
    <summary>
        <div>
            <span>Examples: Using Characters Directly</span>
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                    <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                </svg>
            </div>
        </div>
    </summary>
    <dl class="param-examples">
        <dt><span>𛱠</span></dt>
        <dd>Copy and paste the character into the text box below.</dd>
        <dt><span>🏃🏿‍♀️</span></dt>
        <dd>Copy and paste the character into the text box below.</dd>
    </dl>
</details>
"""

UNICODE_CHAR_URI_EXAMPLES = f"""
<details id="uri-char-examples">
    <summary>
        <div>
            <span>Examples: Using URI-Encoded Value of Character</span>
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                    <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                </svg>
            </div>
        </div>
    </summary>
    <dl class="param-examples">
        <dt><span>Ⱒ</span><sup>2</sup></dt>
        <dd><a href="{get_settings().API_ROOT}/v1/characters/{get_uri_encoded_value('Ⱒ')}" rel="noopener noreferrer" target="_blank">{get_uri_encoded_value('Ⱒ')}</a><sup>1</sup></dd>
        <dt><span>👨‍🌾 </span><sup>3</sup></dt>
        <dd><a href="{get_settings().API_ROOT}/v1/characters/{get_uri_encoded_value('👨‍🌾')}" rel="noopener noreferrer" target="_blank">{get_uri_encoded_value('👨‍🌾')}</a><sup>1</sup></dd>
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

UNICODE_CHAR_STRING_DESCRIPTION = f"""
<p>A string containing Unicode characters, which can be expressed either directly (unencoded) or as a URI-encoded string. If you are unsure which format to use, please see the <strong>Examples</strong> below.</p>
{UNICODE_CHAR_NORMAL_EXAMPLES}
{UNICODE_CHAR_URI_EXAMPLES}
"""

CODEPOINT_PATH_PARAM_DESSCRIPTION = f"""
<p>The codepoint of a Unicode character. This value must be expressed as a hexadecimal value within range <code>0000...10FFFF</code>, optionally prefixed by <code>U+</code> or <code>0x</code>.</p>
<p>For example, <code>72</code>, <code>U+0072</code>, <code>0x72</code> and <code>0x0072</code> are valid ways to express the same code point. It is important to note that <code>U+72</code> IS NOT valid because codepoints prefixed with <code>U+</code> MUST be left-padded with zeroes to a minimum length of four digits. For more information, see the examples below:</p>
{CODEPOINT_EXAMPLES}
"""

BLOCK_NAME_DESCRIPTION = f"""
<ul class="param-notes">
    <li class=\"loose-match\">The <a href="#loose-matching">Loose-matching rule</a> is applied to the value of this parameter</li>
</ul>
<p>The name of a Unicode block. If the value provided matches the name of a Unicode block according to the loose-matching rule, the response will contain a <a href="#the-unicodeblock-object"><code>UnicodeBlock</code> object</a> for the specified block.</p>
<p>A list of the official names for all Unicode blocks is given below:</p>
{BLOCK_NAME_VALUES_TABLE}
<p>Enter the name of any block into the field below:</p>
"""

CHAR_SEARCH_BLOCK_NAME_DESCRIPTION = f"""
<ul class="param-notes">
    <li>This value is optional</li>
    <li class=\"loose-match\">The <a href="#loose-matching">Loose-matching rule</a> is applied to the value of this parameter</li>
</ul>
<p>if a valid block name is given, the response will only contain characters from that block. If this value is not provided, the response will contain all characters in all blocks.</p>
<p>A list of the official names for all Unicode blocks is given below:</p>
{BLOCK_NAME_VALUES_TABLE}
<p>To only list characters from a single block, enter the name of the block into the field below:</p>
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
<p>Search for any Unicode character by name. Exact matches are unnecessary since the search algorithm will return character names similar to the search term and provide a <strong>score</strong> value for each result.</p>
<p>You can restrict or expand your search based on the score value with the <strong>min_score</strong> parameter. For more information on this search behavior, see the <a href="#search">Search section</a> of the docs</p>
"""

SEARCH_BLOCK_NAME_DESCRIPTION = """
<ul class="param-notes">
    <li class=\"loose-match\">The <a href="#loose-matching">Loose-matching rule</a> is applied to the value of this parameter</li>
</ul>
<p>Search for any Unicode block by name. Exact matches are unnecessary since the search algorithm will return block names similar to the search term and provide a <strong>score</strong> value for each result that indicates how similar your search term is to each block name.</p>
<p>You can restrict or expand your search based on the score value with the <strong>min_score</strong> parameter. For more information on this search behavior, see the <a href="#search">Search section</a> of the docs.</p>
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

CJK_DEFINITION_FILTER_DESCRIPTION = """
<ul class="param-notes">
    <li>This value is optional</li>
    <li class=\"alert\">This parameter only applies to CJK characters. Including this parameter in any request guarantees that the response will be limited to CJK characters.</li>
</ul>
<p>Filter CJK characters by the English-language definition, if available. A character is considered a match if the CJK definition of the character <strong>contains</strong> the value provided.</p>
"""

VERBOSE_DESCRIPTION = """
<ul class="param-notes">
    <li>This value is optional (default: <code>verbose=false</code>)</li>
</ul>
<p>Sending <code>verbose=true</code> makes the response include every property value specified by the values sent for the <code>show_props</code> parameter. By default, properties are removed from the response if the value is irrelevent. For more info, see the <a href="#verbosity">Verbosity section</a> of the docs.</p>
"""


def get_description_and_values_table_for_block_name() -> str:
    return (
        '<ul class="param-notes">'
        + "<li>This value is optional</li>"
        + '<li class="loose-match">The <a href="#loose-matching">Loose-matching rule</a> is applied to the value of this parameter</li>'
        + "</ul>"
        + "<p>Filter characters by Unicode block. Sending multiple values will return all characters that match any of the specified blocks (e.g., sending <code>block=Cyrillic</code> and <code>block=Cyrillic_Supplement</code> will return characters that are assigned to <strong>either</strong> of the two blocks.</p>"
        + "<p>A list of the official names for all Unicode blocks is given below:</p>"
        + f"{BLOCK_NAME_NO_LEGEND_TABLE}"
        + "<p>To add a filter setting for <code>block</code>, click the button below and enter a value from the <strong>Block Name</strong> column in the table above.</p>"
    )


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
        + "<p>Filter Unicode characters by <strong>Age</strong> (i.e., the version of the Unicode Standard in which the character was originally assigned to a codepoint). Sending multiple values will return all characters that match any of the selected Unicode versions (e.g., sending <code>age=2.0</code> and <code>age=5.0</code> will return all characters that were assigned to a codepoint in <strong>either</strong> version 2.0 or 5.0).<p>"
        + "<p>Version numbers for all releases of the Unicode Standard are shown in the table below:</p>"
        + f"{UNICODE_AGE_VALUES_TABLE}"
        + "<p>To add a filter setting for <code>age</code>, click the button below and enter a value from the list of Unicode version numbers.</p>"
    )


def get_description_and_values_table_for_general_category() -> str:
    return (
        '<ul class="param-notes">'
        + "<li>This value is optional</li>"
        + '<li class="loose-match">The <a href="#loose-matching">Loose-matching rule</a> is applied to the value of this parameter</li>'
        + "</ul>"
        + "<p>Filter Unicode characters by <strong>General Category</strong>. Sending multiple values will return all characters that match any of the selected catagories (e.g., sending <code>category=P</code> and <code>category=S</code> will return <strong>both</strong> Punctuation and Symbol characters).<p>"
        + "<p>All valid general category codes are shown in the table below:</p>"
        + f"{GENERAL_CATEGORY_VALUES_TABLE}"
        + "<p>To add a filter setting for <code>general_category</code>, click the button below and enter a value from the <strong>Code</strong> column of the table above.</p>"
    )


def get_description_and_values_table_for_script_code() -> str:
    return (
        '<ul class="param-notes">'
        + "<li>This value is optional</li>"
        + '<li class="loose-match">The <a href="#loose-matching">Loose-matching rule</a> is applied to the value of this parameter</li>'
        + "</ul>"
        + "<p>Filter Unicode characters by <strong>Script</strong>. Sending multiple values will return all characters that match any of the selected scripts (e.g., sending <code>script=Copt</code> and <code>script=Cyrl</code> will return <strong>both</strong> Greek and Coptic characters.<p>"
        + "<p>All valid script codes are shown in the table below:</p>"
        + f"{SCRIPT_CODE_VALUES_TABLE}"
        + "<p>To add a filter setting for <code>script</code>, click the button below and enter a value from the <strong>Code</strong> column of the table above.</p>"
    )


def get_description_and_values_table_for_bidi_class() -> str:
    return (
        '<ul class="param-notes">'
        + "<li>This value is optional</li>"
        + '<li class="loose-match">The <a href="#loose-matching">Loose-matching rule</a> is applied to the value of this parameter</li>'
        + "</ul>"
        + "<p>Filter Unicode characters by <strong>Bidirectional Class</strong>. Sending multiple values will return all characters that match any of the selected classes (e.g., sending <code>bidi_class=AL</code> and <code>bidi_class=AN</code> will return characters that are treated as Arabic Letters <strong>and</strong> characters that are treated as Arabic Numbers when formatting bidiretional text.<p>"
        + "<p>All valid bidirectional class values are shown in the table below:</p>"
        + f"{BIDI_CLASS_VALUES_TABLE}"
        + "<p>To add a filter setting for <code>bidirectional_class</code>, click the button below and enter a value from the <strong>Code</strong> column of the table above.</p>"
    )


def get_description_and_values_table_for_decomp_type() -> str:
    return (
        '<ul class="param-notes">'
        + "<li>This value is optional</li>"
        + '<li class="loose-match">The <a href="#loose-matching">Loose-matching rule</a> is applied to the value of this parameter</li>'
        + "</ul>"
        + "<p>Filter Unicode characters by <strong>Decomposition Type</strong>. Sending multiple values will return all characters that match any of the selected types (e.g., sending <code>decomp_type=sub</code> and <code>decomp_type=sup</code> will return characters that decompose as subscript <strong>and</strong> superscript characters when normalization algorithms are applied.<p>"
        + "<p>All valid decomposition types are shown in the table below:</p>"
        + f"{DECOMP_TYPE_VALUES_TABLE}"
        + "<p>To add a filter setting for <code>decomposition_type</code>, click the button below and enter a value from the <strong>Code</strong> column of the table above.</p>"
    )


def get_description_and_values_table_for_line_break_type() -> str:
    return (
        '<ul class="param-notes">'
        + "<li>This value is optional</li>"
        + '<li class="loose-match">The <a href="#loose-matching">Loose-matching rule</a> is applied to the value of this parameter</li>'
        + "</ul>"
        + "<p>Filter Unicode characters by <strong>Line Break Type</strong>. Sending multiple values will return all characters that match any of the selected types (e.g., sending <code>line_break=WJ</code> and <code>line_break=ZW</code> will return characters that prohibit line breaks before and after their location in a string.<p>"
        + "<p>All valid line break types are shown in the table below:</p>"
        + f"{LINE_BREAK_TYPE_VALUES_TABLE}"
        + "<p>To add a filter setting for <code>line_break_type</code>, click the button below and enter a value from the <strong>Code</strong> column of the table above.</p>"
    )


def get_description_and_values_table_for_combining_class_category() -> str:
    return (
        '<ul class="param-notes">'
        + "<li>This value is optional</li>"
        + "</ul>"
        + "<p>Filter Unicode characters by <strong>Combining Class Category</strong>. Sending multiple values will return all characters that match any of the selected classes (e.g., sending <code>ccc=6</code> and <code>ccc=9</code> will return characters that act as diactritic reading marks for CJK unified ideographs <strong>AND</strong> Virama characters.<p>"
        + "<p>All valid combining class category values are shown in the table below:</p>"
        + f"{CCC_VALUES_TABLE}"
        + "<p>To add a filter setting for <code>Combining Class Category</code>, click the button below and enter a value from the <strong>Code</strong> column of the table above.</p>"
    )


def get_description_and_values_table_for_numeric_type() -> str:
    return (
        '<ul class="param-notes">'
        + "<li>This value is optional</li>"
        + '<li class="loose-match">The <a href="#loose-matching">Loose-matching rule</a> is applied to the value of this parameter</li>'
        + "</ul>"
        + "<p>Filter Unicode characters by <strong>Numeric Type</strong>. Sending multiple values will return all characters that match any of the selected types (e.g., sending <code>num_type=De</code> and <code>num_type=Nu</code> will return characters where the <code>numericValue</code> of the digit is represented with an integer digit <strong>OR</strong> a rational number.<p>"
        + "<p>All valid values for numeric type are shown in the table below:</p>"
        + f"{NUMERIC_TYPES_TABLE}"
        + "<p>To add a filter setting for <code>Numeric Type</code>, click the button below and enter a value from the <strong>Code</strong> column of the table above.</p>"
    )


def get_description_and_values_table_for_joining_type() -> str:
    return (
        '<ul class="param-notes">'
        + "<li>This value is optional</li>"
        + '<li class="loose-match">The <a href="#loose-matching">Loose-matching rule</a> is applied to the value of this parameter</li>'
        + "</ul>"
        + "<p>Filter Unicode characters by <strong>Joining Type</strong>. Sending multiple values will return all characters that match any of the selected types (e.g., sending <code>join_type=R</code> and <code>join_type=D</code> will return characters that cursively join to a character displayed to their right in visual order <strong>AND</strong> characters that cursively join to characters displayed both to their left and their right in visual order.<p>"
        + "<p>All valid values for joining type are shown in the table below:</p>"
        + f"{JOINING_TYPES_TABLE}"
        + "<p>To add a filter setting for <code>Joining Type</code>, click the button below and enter a value from the <strong>Code</strong> column of the table above.</p>"
    )


def get_description_and_values_table_for_flags() -> str:
    return (
        '<ul class="param-notes">'
        + "<li>This value is optional</li>"
        + '<li class="loose-match">The <a href="#loose-matching">Loose-matching rule</a> is applied to the value of this parameter</li>'
        + "</ul>"
        + "<p>Filter Unicode characters by various boolean values. Sending multiple values will return all characters that match any of the selected types (e.g., sending <code>flag=emoji</code> and <code>flag=ascii_hex</code> will return <strong>both</strong> Emoji and ASCII Hex Digit characters).<p>"
        + "<p>All possible flag values are shown in the table below:</p>"
        + f"{CHAR_FLAGS_TABLE}"
        + "<p>To add a filter setting for any <strong>flag</strong> value, click the button below and enter the value from the <strong>Flags (Boolean Properties)</strong> <i><u>or</u></i> <strong>Alias</strong> column of the table above.</p>"
    )


def customize_ending_before_param_description(
    data_type: str, key_field: str, example_value: str, field_type_description: str
) -> str:
    return f"""
<ul class="param-notes">
    <li>This value is optional</li>
    <li class=\"alert\">Only one of <code>starting_after</code> or <code>ending_before</code> may be used in a request, sending a value for both parameters will produce a response with status <code>400 Bad Request</code></i></strong>.</li>
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
    <li class=\"alert\">Only one of <code>starting_after</code> or <code>ending_before</code> may be used in a request, sending a value for both parameters will produce a response with status <code>400 Bad Request</code></i></strong>.</li>
</ul>
<p>The <code>starting_after</code> parameter acts as a cursor to navigate between paginated responses, however, the value used for this parameter is different for each endpoint. <i><u>For Unicode {data_type}, the value of this parameter is the <code>{key_field}</code> property.</i></u></p>
<p>For example, if you request 10 items and the response contains <code>hasMore=true</code>, there are more search results beyond the first 10. If the 10th search result has <code>{key_field}={example_value}</code>, you can retrieve the next set of results by sending <code>starting_after={example_value}</code> in a subsequent request.</p>
<p>{field_type_description}</p>
"""


ENDING_BEFORE_CODEPOINT_DESCRIPTION_1 = customize_ending_before_param_description(
    "characters", "codepoint", "U+0431", CODEPOINT_HEX_DESCRIPTION
)
STARTING_AFTER_CODEPOINT_DESCRIPTION_1 = customize_starting_after_param_description(
    "characters", "codepoint", "U+0409", CODEPOINT_HEX_DESCRIPTION
)

ENDING_BEFORE_CODEPOINT_DESCRIPTION = f"""
{ENDING_BEFORE_CODEPOINT_DESCRIPTION_1}
{CODEPOINT_EXAMPLES}
"""

STARTING_AFTER_CODEPOINT_DESCRIPTION = f"""
{STARTING_AFTER_CODEPOINT_DESCRIPTION_1}
{CODEPOINT_EXAMPLES}
"""

ENDING_BEFORE_BLOCK_ID_DESCRIPTION = customize_ending_before_param_description(
    "blocks", "id", "10", BLOCK_ID_DESCRIPTION
)
STARTING_AFTER_BLOCK_ID_DESCRIPTION = customize_starting_after_param_description(
    "blocks", "id", "140", BLOCK_ID_DESCRIPTION
)


def get_filter_param_description(param_name: str) -> str:
    param_map = {
        "bidi_class": get_description_and_values_table_for_bidi_class(),
        "block": get_description_and_values_table_for_block_name(),
        "ccc": get_description_and_values_table_for_combining_class_category(),
        "decomp_type": get_description_and_values_table_for_decomp_type(),
        "flag": get_description_and_values_table_for_flags(),
        "category": get_description_and_values_table_for_general_category(),
        "join_type": get_description_and_values_table_for_joining_type(),
        "line_break": get_description_and_values_table_for_line_break_type(),
        "num_type": get_description_and_values_table_for_numeric_type(),
        "show_props": get_description_and_values_table_for_property_group(),
        "script": get_description_and_values_table_for_script_code(),
        "age": get_description_and_values_table_for_unicode_age(),
    }
    return param_map.get(param_name, "")
