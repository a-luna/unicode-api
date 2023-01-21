INTRODUCTION = """<p>This API provides access to detailed information for all characters, blocks and planes in <a href="https://www.unicode.org/versions/Unicode15.0.0/" rel="noopener noreferrer" target="_blank">version 15.0 of the Unicode Standard</a> (released September 13, 2022). In an attempt to adhere to the tenants of <a href="http://en.wikipedia.org/wiki/Representational_State_Transfer" rel="noopener noreferrer" target="_blank">REST</a>, the API is organized around the following principles:</p>
<ul>
    <li>URLs are predictable and resource-oriented.</li>
    <li>Uses standard HTTP verbs and response codes.</li>
    <li>Returns JSON-encoded responses.</li>
</ul>
"""

PROJECT_LINKS_SWAGGER_HTML = """    <ul>
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
        <p>The top-level API resources for <strong>Unicode Characters</strong> and <strong>Unicode Blocks</strong> have support for retrieving all character/block objects via "list" API methods. These API methods (<code>/v1/characters</code> and <code>/v1/blocks</code>) share a common structure, taking at least these three parameters: <code>limit</code>, <code>starting_after</code>, and <code>ending_before</code>.</p>
        <p>For your initial request, you should only provide a value for <code>limit</code> (if the default value of <code>limit=10</code> is ok, you do not need to provide values for any parameter in your initial request). The response of a list API method contains a <code>data</code> parameter that represents a single page of results, and a <code>hasMore</code> parameter that indicates whether the list contains more results after this set.</p>
        <p>The <code>starting_after</code> parameter acts as a cursor to navigate between paginated responses, however, the value used for this parameter is different for each endpoint. For <strong>Unicode Characters</strong>, the value of this parameter is the <code>codepoint</code> property, while for <strong>Unicode Blocks</strong> the <code>id</code> property is used.</p>
        <p>For example, if you request 10 items and the response contains <code>hasMore=true</code>, there are more search results beyond the first 10. If the 10th search result has <code>codepoint=U+0346</code>, you can retrieve the next set of results by sending <code>starting_after=U+0346</code> in a subsequent request.</p>
        <p>The <code>ending_before</code> parameter also acts as a cursor to navigate between pages, but instead of requesting the next set of results it allows you to access previous pages in the list.</p>
        <p>For example, if you previously requested 10 items beyond the first page of results, and the first search result of the current page has <code>codepoint=U+0357</code>, you can retrieve the previous set of results by sending <code>ending_before=U+0357</code> in a subsequent request.</p>
        <p>⚠️ <strong><i>IMPORTANT: Only one of <code>starting_after</code> or <code>ending_before</code> may be used in a request, sending a value for both parameters will produce a response with status <code>400 Bad Request</code>.</i></strong></p>
    </div>
"""

SEARCH = """
    <div>
        <p>The top-level API resources for <strong>Unicode Characters</strong> and <strong>Unicode Blocks</strong> also have support for retrieval via "search" API methods. These API methods (<code>/v1/characters/search</code> and <code>/v1/blocks/search</code>) share an identical structure, taking the same four parameters: <code>name</code>, <code>min_score</code>, <code>per_page</code>, and <code>page</code>.</p>
        <p>The <code>name</code> parameter is the search term and is used to retrieve a character/block using the official name defined in the UCD. Since a <a href="https://en.wikipedia.org/wiki/Approximate_string_matching" rel="noopener noreferrer" target="_blank">fuzzy search algorithm</a> is used for this process, the value of <code>name</code> does not need to be an exact match with a character/block name.</p>
        <p>The response will contain a <code>results</code> parameter that represents the characters/blocks that matched your query. Each object in this list has a <code>score</code> property which is a number ranging from <strong>0-100</strong> that describes how similar the character/block name is to the <code>name</code> value provided by the user (A value of 100 means that the <code>name</code> provided by the user is an exact match with a character/block name). The list contains all results where <code>score</code> &gt;= <code>min_score</code>, sorted by <code>score</code> (the first element in the list being the <i><strong>most similar</strong></i>).</p>
        <p>The default value for <code>min_score</code> is <strong>80</strong>, however if your request is returning zero results, you can lower this value to potentially surface lower-quality results. Keep in mind, the lowest value for <code>min_score</code> that is permitted is <strong>70</strong>, since the relevence of results quickly drops off around a score of <strong>72</strong>, often producing hundreds of results with no relevance to the search term.</p>
        <p>The <code>per_page</code> parameter controls how many results are included in a single response. The response will include a <code>hasMore</code> parameter that indicates whether there are more search results beyond the current page, as well as <code>currentPage</code> and <code>totalResults</code> parameters. If <code>hasMore=true</code>, the response will also contain a <code>nextPage</code> parameter. For example, if you make a search request and the response has <code>hasMore=true</code> and <code>nextPage=2</code> in the response, your subsequent call can include <code>page=2</code> to fetch the next page of results.</p>
    </div>
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

PROP_GROUP_MINIMUM = """
            <dl>
                <dt><strong>character</strong></dt>
                <dd>A unit of information used for the organization, control, or representation of textual data.</dd>
                <dt><strong>name</strong></dt>
                <dd>A unique string used to identify each character encoded in the Unicode standard.</dd>
                <dt><strong>codepoint</strong></dt>
                <dd>A number in the range from <code>U+0000</code> to <code>U+10FFFF</code> assigned to a single character</dd>
                <dt><strong>uriEncoded</strong></dt>
                <dd>The character as a URI encoded string. A URI is a string that identifies an abstract or physical resource on the internet (The specification for the URI format is defined in <a href="https://www.rfc-editor.org/rfc/rfc3986" rel="noopener noreferrer" target="_blank">RFC 3986</a>). The string must contain only a defined subset of characters from the standard 128 ASCII character set, any other characters must be replaced by an escape sequence representing the UTF-8 encoding of the character. For example, ∑ (<code>U+2211 <span>N-ARY SUMMATION</span></code>) is equal to <code>0xE2 0x88 0x91</code> in UTF-8 encoding. When used as part of a URI, this character must be escaped using the string <code>%E2%88%91</code>.</dd>
            </dl>
"""

PROP_GROUP_BASIC = """
            <dl>
                <dt><strong>block</strong></dt>
                <dd>A grouping of characters within the Unicode encoding space used for organizing code charts. Each block is a uniquely named, continuous, non-overlapping range of code points, containing a multiple of 16 code points, and starting at a location that is a multiple of 16. A block may contain unassigned code points, which are reserved.</dd>
                <dt><strong>plane</strong></dt>
                <dd>A range of 65,536 (<code>0x10000</code>) contiguous Unicode code points, where the first code point is an integer multiple of 65,536 (<code>0x10000</code>). Planes are numbered from 0 to 16, with the number being the first code point of the plane divided by 65,536. Thus Plane 0 is <code>U+0000...U+FFFF</code>, Plane 1 is <code>U+<strong>1</strong>0000...U+<strong>1</strong>FFFF</code>, ..., and Plane 16 (<code>0x<strong>10</strong></code>) is <code>U+<strong>10</strong>0000...<strong>10</strong>FFFF</code>.<br />The vast majority of commonly used characters are located in Plane 0, which is called the <strong>Basic Multilingual Plane (BMP)</strong>. Planes 1-16 are collectively referred to as <i>supplementary planes</i>.</dd>
                <dt><strong>age</strong></dt>
                <dd>The version of Unicode in which a code point was assigned to an abstract character, or made a surrogate or non-character.</dd>
                <dt><strong>generalCategory</strong></dt>
                <dd>The <a href="https://www.unicode.org/versions/latest/ch04.pdf#G124142" rel="noopener noreferrer" target="_blank">General Category</a> that this character belongs to (e.g., letters, numbers, punctuation, symbols, etc.). The full list of values which are valid for this property is defined in <a href="http://www.unicode.org/reports/tr44/#General_Category_Values">Unicode Standard Annex #44</a></dd>
                <dt><strong>combiningClass</strong></dt>
                <dd>Similar to <strong>bidirectional_class</strong>, this value helps to determine how the canonical ordering of sequences of combining characters takes place. For more info, please see <a href="https://www.unicode.org/versions/Unicode15.0.0/ch04.pdf#page=11" rel="noopener noreferrer" target="_blank">Unicode Standard Section 4.3</a>.</dd>
                <dt><strong>htmlEntities</strong></dt>
                <dd>A string begining with an ampersand (&) character and ending with a semicolon (;). Entities are used to display reserved characters (e.g., '<' in an HTML document) or invisible characters (e.g., non-breaking spaces). For more info, please see the <a href="https://developer.mozilla.org/en-US/docs/Glossary/Entity" rel="noopener noreferrer" target="_blank">MDN entry for HTML Entities</a>.</dd>
            </dl>
"""

PROP_GROUP_UTF8 = """
            <dl>
                <dt><strong>utf8</strong></dt>
                <dd>The UTF-8 encoded value for the character as a hex string. UTF-8 is a method of encoding the Unicode character set where each code unit is equal to 8-bits. UTF-8 is backwards-compatible with ASCII and all codepoints in range 0-127 are represented as a single byte. Codepoints greater than 127 are represented as a sequence of 2-4 bytes.</dd>
                <dt><strong>utf8HexBytes</strong></dt>
                <dd>The byte sequence for the UTF-8 encoded value for the character. This property returns a list of strings, hex values (base-16) in range <code>00-FF</code>.</dd>
                <dt><strong>utf8DecBytes</strong></dt>
                <dd>The byte sequence for the UTF-8 encoded value for the character. This property returns a list of integers, decimal values (base-10) in range 0-127</dd>
            </dl>
"""

PROP_GROUP_UTF16 = """
            <dl>
                <dt><strong>utf16</strong></dt>
                <dd>The UTF-16 encoded value for the character as a hex string. UTF-16 is a method of encoding the Unicode character set where each code unit is equal to 16-bits. All codepoints in the BMP (Plane 0) can be represented as a single 16-bit code unit (2 bytes). Code points in the supplementary planes (Planes 1-16) are represented as pairs of 16-bit code units (4 bytes).</dd>
                <dt><strong>utf16HexBytes</strong></dt>
                <dd>The byte sequence for the UTF-16 encoded value for the character. This property returns a list of strings, hex values (base-16) in range <code>0000-FFFF</code>.</dd>
                <dt><strong>utf16DecBytes</strong></dt>
                <dd>The byte sequence for the UTF-16 encoded value for the character. This property returns a list of integers, decimal values (base-10) in range 0-65,535</dd>
            </dl>
"""

PROP_GROUP_UTF32 = """
            <dl>
                <dt><strong>utf32</strong></dt>
                <dd>The UTF-32 encoded value for the character as a hex string. UTF-32 is a method of encoding the Unicode character set where each code unit is equal to 32-bits. UTF-32 is the simplest Unicode encoding form. Each Unicode code point is represented directly by a single 32-bit code unit. Because of this, UTF-32 has a one-to-one relationship between encoded character and code unit; it is a fixed-width character encoding form.</dd>
                <dt><strong>utf32HexBytes</strong></dt>
                <dd>The byte sequence for the UTF-32 encoded value for the character. This property returns a list of strings, hex values (base-16) in range <code>00000000-0010FFFF</code>.</dd>
                <dt><strong>utf32DecBytes</strong></dt>
                <dd>The byte sequence for the UTF-32 encoded value for the character. This property returns a list of integers, decimal values (base-10) in range 0-1,114,111</dd>
            </dl>
"""

PROP_GROUP_BIDIRECTIONALITY = """
            <dl>
                <dt><strong>bidirectionalClass</strong></dt>
                <dd>A value assigned to each Unicode character based on the appropriate directional formatting style. Each character has an implicit <strong>bidirectional type</strong>. The bidirectional types left-to-right and right-to-left are called <strong>strong types</strong>, and characters of those types are called strong directional characters. The bidirectional types associated with numbers are called <strong>weak types</strong>.</dd>
                <dt><strong>bidirectionalIsMirrored</strong></dt>
                <dd>A normative property of characters such as parentheses, whose images are mirrored horizontally in text that is laid out from right to left. For example, <code>U+0028 <span>LEFT PARENTHESIS</span></code> is interpreted as opening parenthesis; in a left-to-right context it will appear as “(”, while in a right-to-left context it will appear as the mirrored glyph “)”. This requirement is necessary to render the character properly in a bidirectional context.</dd>
                <dt><strong>bidirectionalMirroringGlyph</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>bidirectionalControl</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>pairedBracketType</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>pairedBracketProperty</strong></dt>
                <dd>(description needed)</dd>
            </dl>
"""

PROP_GROUP_DECOMPOSITION = """
            <dl>
                <dt><strong>decompositionType</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>decompositionMapping</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>compositionExclusion</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>fullCompositionExclusion</strong></dt>
                <dd>(description needed)</dd>
            </dl>
"""

PROP_GROUP_NUMERIC = """
            <dl>
                <dt><strong>numericType</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>numericValue</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>numericValueParsed</strong></dt>
                <dd>(description needed)</dd>
            </dl>
"""

PROP_GROUP_JOINING = """
            <dl>
                <dt><strong>joiningClass</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>joiningGroup</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>joiningControl</strong></dt>
                <dd>(description needed)</dd>
            </dl>
"""

PROP_GROUP_LINEBREAK = """
            <dl>
                <dt><strong>lineBreak</strong></dt>
                <dd>(description needed)</dd>
            </dl>
"""

PROP_GROUP_EAW = """
            <dl>
                <dt><strong>eastAsianWidth</strong></dt>
                <dd>(description needed)</dd>
            </dl>
"""

PROP_GROUP_CASE = """
            <dl>
                <dt><strong>uppercase</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>lowercase</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>simpleUppercaseMapping</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>simpleLowercaseMapping</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>simpleTitlecaseMapping</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>simpleCaseFolding</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>otherUppercase</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>otherLowercase</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>otherUppercaseMapping</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>otherLowercaseMapping</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>otherTitlecaseMapping</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>otherCaseFolding</strong></dt>
                <dd>(description needed)</dd>
            </dl>
"""

PROP_GROUP_SCRIPT = """
            <dl>
                <dt><strong>script</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>scriptExtension</strong></dt>
                <dd>(description needed)</dd>
            </dl>
"""

PROP_GROUP_HANGUL = """
            <dl>
                <dt><strong>hangulSyllableType</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>jamoShortName</strong></dt>
                <dd>(description needed)</dd>
            </dl>
"""

PROP_GROUP_INDIC = """
            <dl>
                <dt><strong>indicSyllabicCategory</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>indicMatraCategory</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>indicPositionalCategory</strong></dt>
                <dd>(description needed)</dd>
            </dl>
"""

PROP_GROUP_F_AND_G = """
            <dl>
                <dt><strong>dash</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>hyphen</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>quotationMark</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>terminalPunctuation</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>sentenceTerminal</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>diacritic</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>extender</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>softDotted</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>alphabetic</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>otherAlphabetic</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>math</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>otherMath</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>hexDigit</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>asciiHexDigit</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>defaultIgnorableCodePoint</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>otherDefaultIgnorableCodePoint</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>logicalOrderException</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>prependedConcatenationMark</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>whiteSpace</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>verticalOrientation</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>regionalIndicator</strong></dt>
                <dd>(description needed)</dd>
            </dl>
"""

PROP_GROUP_EMOJI = """
            <dl>
                <dt><strong>emoji</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>emojiPresentation</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>emojiModifier</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>emojiModifierBase</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>emojiComponent</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>extendedPictographic</strong></dt>
                <dd>(description needed)</dd>
            </dl>
"""

UNICODE_CHATACTER_OBJECT_INTRO = '<p>The <code>UnicodeCharacter</code> object represents a single character/codepoint in the <a href="https://unicode.org/reports/tr44/" rel="noopener noreferrer" target="_blank">Unicode Character Database (UCD)</a>. It contains a rich set of properties that document the purpose and intended representation of the character.</p>'

UNICODE_CHARACTER_PROP_GROUPS_INTRO = (
    "<p>If each response contained every character property, it would be massively inneficient. To ensure that the API remains responsive and performant while also allowing clients to access the full set of character properties, each property is assigned to a <strong>property group</strong>.</p>"
    + "<p>Since they are designed to return lists of characters, responses from the <code>/v1/characters</code> or <code>/v1/characters/search</code> endpoints will only include properties from the <strong>Minimum</strong> property group:</p>"
)

UNICODE_CHARACTER_PROP_GROUPS_CONTINUED_1 = "<p>ℹ️ <strong><i>NOTE: Specifying <code>show_props=Minimum</code> in a request is redundent since the <strong>Minimum</strong> property group is included in all responses.</i></strong></p>\n"

UNICODE_CHARACTER_PROP_GROUPS_CONTINUED_2 = "<p>If you wish to explore the properties of a specifc character, the <code>/v1/characters/{string}</code> endpoint accepts one or more <code>show_props</code> parameters that allow you to specify additional property groups to include in the response:</p>\n"

BLOCK_ENDPOINTS = """
        <dl>
            <dt><strong>GET</strong> <code>/v1/blocks/{string}</code></dt>
            <dd>Retrieve one or more Block(s)</dd>
            <dt><strong>GET</strong> <code>/v1/blocks</code></dt>
            <dd>List Blocks</dd>
            <dt><strong>GET</strong> <code>/v1/blocks/search</code></dt>
            <dd>Search Blocks</dd>
        </dl>
"""

PLANE_ENDPOINTS = """
        <dl>
            <dt><strong>GET</strong> <code>/v1/planes/{string}</code></dt>
            <dd>Retrieve one or more Plane(s)</dd>
            <dt><strong>GET</strong> <code>/v1/planes</code></dt>
            <dd>List Planes</dd>
        </dl>
"""
