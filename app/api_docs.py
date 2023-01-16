import re

HtmlHeading = dict[str, int | str]
HeadingMap = dict[int, list[HtmlHeading]]

HEADING_ELEMENT_REGEX = re.compile(
    r'h(?P<level>2|3|4|5|6) id="(?P<slug>[0-9a-z-_]+)">(?P<text>.+)<\/(?:h2|h3|h4|h5|h6)>'
)


def create_details_element_swagger_docs(title: str, content: str, open: bool | None = False) -> str:
    open_tag = "<details open>" if open else "<details>"
    return f"""{open_tag}
    <summary>
        <div>
            <span><strong>{title}</strong></span>
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                    <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                </svg>
            </div>
        </div>
    </summary>{content}</details>
"""


def create_details_element_readme(title: str, content: str, open: bool | None = False) -> str:
    open_tag = "<details open>" if open else "<details>"
    return f"""{open_tag}
  <summary>
    <strong>{title}</strong>
  </summary>{content}</details>
"""


def create_readme_section(heading_level: int, title: str, content: str):
    return f"""<h{heading_level} id="{slugify(title)}">{title}</h{heading_level}>{content}"""


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.compile(r"\s+").sub("-", text)
    text = re.compile(r"([^A-Za-z0-9-])+").sub("-", text)
    text = re.compile(r"--+").sub("-", text)
    text = re.compile(r"(^-|-$)").sub("", text)
    return text


INTRODUCTION = """<p>This API provides access to detailed information for all characters, blocks and planes in <a href="https://www.unicode.org/versions/Unicode15.0.0/" rel="noopener noreferrer" target="_blank">version 15.0 of the Unicode Standard</a> (released September 13, 2022). In an attempt to adhere to the tenants of <a href="http://en.wikipedia.org/wiki/Representational_State_Transfer" rel="noopener noreferrer" target="_blank">REST</a>, the API is organized around the following principles:</p>
<ul>
    <li>URLs are predictable and resource-oriented.</li>
    <li>Uses standard HTTP verbs and response codes.</li>
    <li>Returns JSON-encoded responses.</li>
</ul>
"""

PROJECT_LINKS_SWAGGER_HTML = """
    <ul>
        <li><a href="https://github.com/a-luna/unicode-api" rel="noopener noreferrer" target="_blank">Source Code (github.com)</a></li>
        <li><a href="https://github.com/a-luna/unicode-api/blob/master/LICENSE" rel="noopener noreferrer" target="_blank">MIT License</a></li>
        <li>Created by Aaron Luna</li>
        <ul>
            <li><a href="https://github.com/a-luna" rel="noopener noreferrer" target="_blank">Github Profile</a></li>
            <li><a href="https://aaronluna.dev" rel="noopener noreferrer" target="_blank">Personal Website</a></li>
            <li><a href="mailto:contact@aaronluna.dev" rel="noopener noreferrer" class="link">Send Email</a></li>
        </ul>
    </ul>
"""

PROJECT_LINKS_README = """
    <ul>
        <li><a href="https://unicode-api.aaronluna.dev/" rel="noopener noreferrer" target="_blank">Interactive API Documents (Swagger UI)</a></li>
        <li>Created by Aaron Luna</li>
        <ul>
            <li><a href="https://aaronluna.dev" rel="noopener noreferrer" target="_blank">Personal Website</a></li>
            <li><a href="mailto:contact@aaronluna.dev" rel="noopener noreferrer" class="link">Send Email</a></li>
        </ul>
    </ul>
"""

PAGINATION = f"""
    <div>
        <p>The top-level API resources for <strong>Unicode Characters</strong> and <strong>Unicode Blocks</strong> have support for bulk fetches via "list" API methods. These API methods share a common structure, taking at least these three parameters: <code>limit</code>, <code>starting_after</code>, and <code>ending_before</code>.</p>
        <p>For your initial request, you should only provide a value for <code>limit</code> (if the default value of <code>limit=10</code> is ok, you do not need to provide values for any parameter in your initial request). The response of a list API method contains a <code>data</code> parameter that represents a single page of results, and a <code>hasMore</code> parameter that indicates whether the list contains more results after this set.</p>
        <p>The <code>starting_after</code> parameter acts as a cursor to navigate between paginated responses, however, the value used for this parameter is different for each endpoint. For <strong>Unicode Characters</strong> (<code>/v1/characters</code>), the value of this parameter is the <code>codepoint</code> property, while for <strong>Unicode Blocks</strong>  (<code>/v1/blocks</code>) the <code>id</code> property is used.</p>
        <p>For example, if you request 10 items and the response contains <code>hasMore=true</code>, there are more search results beyond the first 10. If the 10th search result has <code>codepoint=U+0346</code>, you can retrieve the next set of results by sending <code>starting_after=U+0346</code> in a subsequent request.</p>
        <p>The <code>ending_before</code> parameter also acts as a cursor to navigate between pages, but instead of requesting the next set of results it allows you to access previous pages in the list.</p>
        <p>For example, if you previously requested 10 items beyond the first page of results, and the first search result of the current page has <code>codepoint=U+0357</code>, you can retrieve the previous set of results by sending <code>ending_before=U+0357</code> in a subsequent request.</p>
        <p>⚠️ <strong><i>IMPORTANT: Only one of <code>starting_after</code> or <code>ending_before</code> may be used in a request, sending a value for both parameters will produce a response with status <code>400 Bad Request</code>.</i></strong> ⚠️</p>
    </div>
"""

SEARCH = """
    <div>
        <p>The top-level API resources for <strong>Unicode Characters</strong> and <strong>Unicode Blocks</strong> also have support for retrieval via "search" API methods. These API methods expect the same four parameters: <code>name</code>, <code>min_score</code>, <code>per_page</code>, and <code>page</code>.</p>
        <p>In both endpoints (<code>/v1/characters/search</code> and <code>/v1/blocks/search</code>), the <code>name</code> parameter is the search term and is compared to the official name for all characters/blocks. Since a <a href="https://en.wikipedia.org/wiki/Approximate_string_matching" rel="noopener noreferrer" target="_blank">fuzzy search algorithm</a> is used for this process, the value of <code>name</code> does not need to be an exact match with a character/block name.</p>
        <p>The response to a search request will contain a <code>results</code> parameter that represents the characters/blocks that matched your query. Each object in this list has a <code>score</code> property which is a number ranging from <strong>0-100</strong> that describes how similar the character/block name is to the <code>name</code> value provided by the user (a value of 100 means the <code>name</code> provided by the user is an exact match with a character/block name).</p>
        <p>The response will include all search results where <code>score</code> &gt;= <code>min_score</code>. The default value for <code>min_score</code> is <strong>80</strong>, however if your request is returning zero results, you can lower this value to potentially surface lower-quality results. Keep in mind, the lowest value for <code>min_score</code> that is permitted is <strong>70</strong>, since the relevence of results quickly drops off around a score of <strong>72</strong>, often producing hundreds of results.</p>
        <p>The <code>per_page</code> parameter controls how many results are included in a single response. The response will include a <code>hasMore</code> parameter that indicates whether there are more search results beyond the current page, as well as <code>currentPage</code> and <code>totalResults</code> parameters. If <code>hasMore=true</code>, the response will contain a <code>nextPage</code> parameter. For example, if you make a search request and receive <code>nextPage=2</code> in the response, your subsequent call can include <code>page=2</code> to fetch the next page of results.</p>
    </div>
"""


CHARACTER_PROPERTIES = f"""
    <dl>
        <dt><strong>character</strong></dt>
        <dd>A unit of information used for the organization, control, or representation of textual data.</dd>
        <dt><strong>name</strong></dt>
        <dd>A unique string used to identify each character encoded in the Unicode standard.</dd>
        <dt><strong>codepoint</strong></dt>
        <dd>A number in the range from <code>U+0000</code> to <code>U+10FFFF</code> assigned to a single character</dd>
        <dt><strong>block</strong></dt>
        <dd>A grouping of characters within the Unicode encoding space used for organizing code charts. Each block is a uniquely named, continuous, non-overlapping range of code points, containing a multiple of 16 code points, and starting at a location that is a multiple of 16. A block may contain unassigned code points, which are reserved.</dd>
        <dt><strong>plane</strong></dt>
        <dd>A range of 65,536 (<code>0x10000</code>) contiguous Unicode code points, where the first code point is an integer multiple of 65,536 (<code>0x10000</code>). Planes are numbered from 0 to 16, with the number being the first code point of the plane divided by 65,536. Thus Plane 0 is <code>U+0000...U+FFFF</code>, Plane 1 is <code>U+<strong>1</strong>0000...U+<strong>1</strong>FFFF</code>, ..., and Plane 16 (<code>0x<strong>10</strong></code>) is <code>U+<strong>10</strong>0000...<strong>10</strong>FFFF</code>.<br />The vast majority of commonly used characters are located in Plane 0, which is called the <strong>Basic Multilingual Plane (BMP)</strong>. Planes 1-16 are collectively referred to as <i>supplementary planes</i>.</dd>
        <dt><strong>category</strong></dt>
        <dd>The <a href="https://www.unicode.org/versions/latest/ch04.pdf#G124142" rel="noopener noreferrer" target="_blank">General Category</a> that this character belongs to (e.g., letters, numbers, punctuation, symbols, etc.). The full list of values which are valid for this property is defined in <a href="http://www.unicode.org/reports/tr44/#General_Category_Values">Unicode Standard Annex #44</a></dd>
        <dt><strong>bidirectional_class</strong></dt>
        <dd>A value assigned to each Unicode character based on the appropriate directional formatting style. Each character has an implicit <i>bidirectional type</i>. The bidirectional types left-to-right and right-to-left are called <i>strong types</i>, and characters of those types are called strong directional characters. The bidirectional types associated with numbers are called <i>weak types</i>.</dd>
        <dt><strong>combining_class</strong></dt>
        <dd>Similar to <strong>bidirectional_class</strong>, this value helps to determine how the canonical ordering of sequences of combining characters takes place. For more info, please see <a href="https://www.unicode.org/versions/Unicode15.0.0/ch04.pdf#page=11" rel="noopener noreferrer" target="_blank">Unicode Standard Section 4.3</a>.</dd>
        <dt><strong>bidirectional_is_mirrored</strong></dt>
        <dd>A normative property of characters such as parentheses, whose images are mirrored horizontally in text that is laid out from right to left. For example, <code>U+0028 <span>LEFT PARENTHESIS</span></code> is interpreted as opening parenthesis; in a left-to-right context it will appear as “(”, while in a right-to-left context it will appear as the mirrored glyph “)”. This requirement is necessary to render the character properly in a bidirectional context.</dd>
        <dt><strong>html_entities</strong></dt>
        <dd>A string begining with an ampersand (&) character and ending with a semicolon (;). Entities are used to display reserved characters (e.g., '<' in an HTML document) or invisible characters (e.g., non-breaking spaces). For more info, please see the <a href="https://developer.mozilla.org/en-US/docs/Glossary/Entity" rel="noopener noreferrer" target="_blank">MDN entry for HTML Entities</a>.</dd>
        <dt><strong>uri_encoded</strong></dt>
        <dd>The character as a URI encoded string. A URI is a string that identifies an abstract or physical resource on the internet (The specification for the URI format is defined in <a href="https://www.rfc-editor.org/rfc/rfc3986" rel="noopener noreferrer" target="_blank">RFC 3986</a>). The string must contain only a defined subset of characters from the standard 128 ASCII character set, any other characters must be replaced by an escape sequence representing the UTF-8 encoding of the character. For example, ∑ (<code>U+2211 <span>N-ARY SUMMATION</span></code>) is equal to <code>0xE2 0x88 0x91</code> in UTF-8 encoding. When used as part of a URI, this character must be escaped using the string <code>%E2%88%91</code>.</dd>
        <dt><strong>utf8</strong></dt>
        <dd>The UTF-8 encoded value for the character as a hex string. UTF-8 is a method of encoding the Unicode character set where each code unit is equal to 8-bits. UTF-8 is backwards-compatible with ASCII and all codepoints in range 0-127 are represented as a single byte. Codepoints greater than 127 are represented as a sequence of 2-4 bytes.</dd>
        <dt><strong>utf16</strong></dt>
        <dd>The UTF-16 encoded value for the character as a hex string. UTF-16 is a method of encoding the Unicode character set where each code unit is equal to 16-bits. All codepoints in the BMP (Plane 0) can be represented as a single 16-bit code unit (2 bytes). Code points in the supplementary planes (Planes 1-16) are represented as pairs of 16-bit code units (4 bytes).</dd>
        <dt><strong>utf32</strong></dt>
        <dd>The UTF-32 encoded value for the character as a hex string. UTF-32 is a method of encoding the Unicode character set where each code unit is equal to 32-bits. UTF-32 is the simplest Unicode encoding form. Each Unicode code point is represented directly by a single 32-bit code unit. Because of this, UTF-32 has a one-to-one relationship between encoded character and code unit; it is a fixed-width character encoding form.</dd>
        <dt><strong>utf8_hex_bytes</strong></dt>
        <dd>The byte sequence for the UTF-8 encoded value for the character. This property returns a list of strings, hex values (base-16) in range <code>00-FF</code>.</dd>
        <dt><strong>utf8_dec_bytes</strong></dt>
        <dd>The byte sequence for the UTF-8 encoded value for the character. This property returns a list of integers, decimal values (base-10) in range 0-127</dd>
    </dl>
"""

CHARACTER_ENDPOINTS = """
    <dl>
        <dt><strong>GET</strong> <code>/v1/characters/{string}</code></dt>
        <dd>Retrieve one or more Character(s)</dd>
        <dt><strong>GET</strong> <code>/v1/characters</code></dt>
        <dd>List Characters</dd>
        <dt><strong>GET</strong> <code>/v1/characters/search</code></dt>
        <dd>Search Characters</dd>
    </dl>
"""

UNICODE_CHARACTERS_DOCS_SWAGGER_HTML = f"""
    <div>
        <p>The <code>UnicodeCharacter</code> object represents a single character/codepoint in the <a href="https://unicode.org/reports/tr44/" rel="noopener noreferrer" target="_blank">Unicode Character Database (UCD)</a>. It contains a rich set of properties that document the purpose and intended representation of the character.</p>
        {create_details_element_swagger_docs("Endpoints", CHARACTER_ENDPOINTS, True)}<h4>The Unicode Character Object</h4>
<p>Each property is assigned to a <strong>property group</strong>. Responses from any <code>character</code> endpoint will only include properties from the <strong>MINIMUM</strong> property group by default. The <code>/v1/characters</code> endpoint accepts one or more <code>show_props</code> parameters that allow you to specify additional property groups to include in the response.</p>
{create_details_element_swagger_docs("Properties of the <code>UnicodeCharacter</code> object", CHARACTER_PROPERTIES)}</div>
"""

UNICODE_CHARACTERS_DOCS_README = f"""
    <div>
        <p>The <code>UnicodeCharacter</code> object represents a single character/codepoint in the <a href="https://unicode.org/reports/tr44/" rel="noopener noreferrer" target="_blank">Unicode Character Database (UCD)</a>. It contains a rich set of properties that document the purpose and intended representation of the character.</p>
        {create_readme_section(4, "Endpoints", CHARACTER_ENDPOINTS)}<h4>The Unicode Character Object</h4>
<p>Each property is assigned to a <strong>property group</strong>. Responses from any <code>character</code> endpoint will only include properties from the <strong>MINIMUM</strong> property group by default. The <code>/v1/characters</code> endpoint accepts one or more <code>show_props</code> parameters that allow you to specify additional property groups to include in the response.</p>
{create_readme_section(4, "Properties of the <code>UnicodeCharacter</code> object", CHARACTER_PROPERTIES)}</div>
"""

UNICODE_BLOCKS = """
<div>
    <p></p>
</div>
"""

UNICODE_PLANES = """
<div>
    <p></p>
</div>
"""


def get_api_docs_for_swagger_html():
    return (
        INTRODUCTION
        + create_details_element_swagger_docs("Project Resources/Contact Info", PROJECT_LINKS_SWAGGER_HTML)
        + create_details_element_swagger_docs("Pagination", PAGINATION)
        + create_details_element_swagger_docs("Search", SEARCH)
        + "<h3>Core Resources</h3>\n"
        + create_details_element_swagger_docs("Unicode Characters", UNICODE_CHARACTERS_DOCS_SWAGGER_HTML)
        + create_details_element_swagger_docs("Unicode Blocks", UNICODE_BLOCKS)
        + create_details_element_swagger_docs("Unicode Planes", UNICODE_PLANES)
    )


def get_api_docs_with_toc_for_readme():
    return "<h1>Unicode API</h1>\n" + INTRODUCTION + create_toc_for_readme() + get_api_docs_for_readme()


def create_toc_for_readme():
    html = get_api_docs_for_readme()
    toc = create_toc_section(2, 0, len(html), create_html_heading_map())
    html = f"<ul>"
    for section in toc:
        html += create_toc_section_html(section)
    html += "</ul>\n"
    return html


def get_api_docs_for_readme():
    return (
        create_readme_section(2, "Project Resources/Contact Info", PROJECT_LINKS_README)
        + create_readme_section(2, "Pagination", PAGINATION)
        + create_readme_section(2, "Search", SEARCH)
        + '<h2 id="core_resources">Core Resources</h2>\n'
        + create_readme_section(3, "Unicode Characters", UNICODE_CHARACTERS_DOCS_README)
        + create_readme_section(3, "Unicode Blocks", UNICODE_BLOCKS)
        + create_readme_section(3, "Unicode Planes", UNICODE_PLANES)
    )


def create_html_heading_map() -> HeadingMap:
    heading_elements = []
    readme_html = get_api_docs_for_readme()
    for match in HEADING_ELEMENT_REGEX.finditer(readme_html):
        match_dict = match.groupdict()
        heading_elements.append(
            {
                "level": int(match_dict["level"]),
                "slug": match_dict["slug"],
                "text": match_dict["text"],
                "index": match.start(),
            }
        )
    return {
        heading_level: [h for h in heading_elements if h["level"] == heading_level] for heading_level in range(2, 7)
    }


def create_toc_section(level: int, section_start: int, section_end: int, heading_map: HeadingMap):
    level_map = [h for h in heading_map[level] if (int(h["index"]) >= section_start and section_end > int(h["index"]))]
    if not level_map or not len(level_map):
        return []
    toc = []
    for i, heading in enumerate(level_map):
        if i < len(level_map) - 1:
            end = (int(level_map[i + 1]["index"]) or 0) - 1
        else:
            end = section_end
        toc.append(
            {"heading": heading, "children": create_toc_section(level + 1, int(heading["index"]), end, heading_map)}
        )
    return toc


def create_toc_section_html(section):
    html = "<li>"
    html += f'<a href="#{section["heading"]["slug"]}">{section["heading"]["text"]}</a>'
    if section["children"]:
        html += "<ul>"
        for sub_toc in section["children"]:
            html += create_toc_section_html(sub_toc)
        html += "</ul>"
    html += f"</li>"
    return html


# This API provides access to every character in the Unicode database. It can be used in various ways:
# - You can list all characters ordered by codepoint using the **`/api/v1/characters`** endpoint.
#   - Rather than listing every character, you can list only characters from a Unicode Block using the **block** query parameter.
#   - By default, the response contains only the rendered character, name and codepoint for each character. A **link** is provided with each character that can be used to request the full set of character properties.
# - You can search the Unicode database by name using the **`/api/v1/characters/search`** endpoint.
# - If you would like to see detailed information about a Unicode character, use the **`/api/v1/characters/{string}`** endpoint.
