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
        <p>⛔️ <strong><i>IMPORTANT: Only one of <code>starting_after</code> or <code>ending_before</code> may be used in a request, sending a value for both parameters will produce a response with status <code>400 Bad Request</code>.</i></strong></p>
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
                <dd>Name of the block to which the character belongs. Each block is a uniquely named, continuous, non-overlapping range of code points, containing a multiple of 16 code points, and starting at a location that is a multiple of 16. A block may contain unassigned code points, which are reserved.</dd>
                <dt><strong>plane</strong></dt>
                <dd>A range of 65,536 (<code>0x10000</code>) contiguous Unicode code points, where the first code point is an integer multiple of 65,536 (<code>0x10000</code>). Planes are numbered from 0 to 16, with the number being the first code point of the plane divided by 65,536. Thus Plane 0 is <code>U+0000...U+FFFF</code>, Plane 1 is <code>U+<strong>1</strong>0000...U+<strong>1</strong>FFFF</code>, ..., and Plane 16 (<code>0x<strong>10</strong></code>) is <code>U+<strong>10</strong>0000...<strong>10</strong>FFFF</code>.<br />The vast majority of commonly used characters are located in Plane 0, which is called the <strong>Basic Multilingual Plane (BMP)</strong>. Planes 1-16 are collectively referred to as <i>supplementary planes</i>.</dd>
                <dt><strong>age</strong></dt>
                <dd>The version of Unicode in which the character was assigned to a codepoint, such as "1.1" or "4.0.".</dd>
                <dt><strong>generalCategory</strong></dt>
                <dd>The <a href="https://www.unicode.org/versions/latest/ch04.pdf#G124142" rel="noopener noreferrer" target="_blank">General Category</a> that this character belongs to (e.g., letters, numbers, punctuation, symbols, etc.). The full list of values which are valid for this property is defined in <a href="http://www.unicode.org/reports/tr44/#General_Category_Values">Unicode Standard Annex #44</a></dd>
                <dt><strong>combiningClass</strong></dt>
                <dd>Specifies, with a numeric code, how a diacritic mark is positioned with respect to the base character. This is used in the Canonical Ordering Algorithm and in normalization. For more info, please see <a href="https://www.unicode.org/versions/Unicode15.0.0/ch04.pdf#page=11" rel="noopener noreferrer" target="_blank">Unicode Standard Section 4.3</a>.</dd>
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
            <div>Reference: <a href="https://www.unicode.org/reports/tr9/" rel="noopener noreferrer" target="_blank">Unicode Standard Annex #9, "Unicode Bidirectional Algorithm"</a></div>
            <dl>
                <dt><strong>bidirectionalClass</strong></dt>
                <dd>A value assigned to each Unicode character based on the appropriate directional formatting style. For the property values, see <a href="https://www.unicode.org/reports/tr44/#Bidi_Class_Values" rel="noopener noreferrer" target="_blank">Bidirectional Class Values</a>.</dd>
                <dt><strong>bidirectionalIsMirrored</strong></dt>
                <dd>A normative property of characters such as parentheses, whose images are mirrored horizontally in text that is laid out from right to left. For example, <code>U+0028 <span>LEFT PARENTHESIS</span></code> is interpreted as opening parenthesis; in a left-to-right context it will appear as “(”, while in a right-to-left context it will appear as the mirrored glyph “)”. This requirement is necessary to render the character properly in a bidirectional context.</dd>
                <dt><strong>bidirectionalMirroringGlyph</strong></dt>
                <dd>A character that can be used to supply a mirrored glyph for the requested character. For example, "(" (<code>U+0028 LEFT PARENTHESIS</code>) mirrors ")" (<code>U+0098 RIGHT PARENTHESIS</code>) and vice versa.</dd>
                <dt><strong>bidirectionalControl</strong></dt>
                <dd>
                    <p>Boolean value that indicates whether the character is one of 12 format control characters which have specific functions in the Unicode Bidirectional Algorithm:</p>
                    <ul>
                        <li><code>U+200E\tLEFT-TO-RIGHT MARK</code></li>
                        <li><code>U+200F\tRIGHT-TO-LEFT MARK</code></li>
                        <li><code>U+202A\tLEFT-TO-RIGHT EMBEDDING</code></li>
                        <li><code>U+202B\tRIGHT-TO-LEFT EMBEDDING</code></li>
                        <li><code>U+202C\tPOP DIRECTIONAL FORMATTING</code></li>
                        <li><code>U+202D\tLEFT-TO-RIGHT OVERRIDE</code></li>
                        <li><code>U+202E\tRIGHT-TO-LEFT OVERRIDE</code></li>
                        <li><code>U+2066\tLEFT-TO-RIGHT ISOLATE</code></li>
                        <li><code>U+2067\tRIGHT-TO-LEFT ISOLATE</code></li>
                        <li><code>U+2068\tFIRST STRONG ISOLATE</code></li>
                        <li><code>U+2069\tPOP DIRECTIONAL ISOLATE</code></li>
                        <li><code>U+061C\tARABIC LETTER MARK</code></li>
                    </ul>
                </dd>
                <dt><strong>pairedBracketType</strong></dt>
                <dd>Type of a paired bracket, either opening, closing or none (the default value). This property is used in the implementation of parenthesis matching.</dd>
                <dt><strong>pairedBracketProperty</strong></dt>
                <dd>For an opening bracket, the code point of the matching closing bracket. For a closing bracket, the code point of the matching opening bracket.</dd>
            </dl>
"""

PROP_GROUP_DECOMPOSITION = """
            <div>Reference: <a href="https://www.unicode.org/versions/Unicode15.0.0/ch03.pdf#page=46" rel="noopener noreferrer" target="_blank">Unicode Standard, Section 3.7, <i>Decomposition</i></a></div>
            <dl>
                <dt><strong>decompositionType</strong></dt>
                <dd>
                    <p>The type of the decomposition (canonical or compatibility). The possible values are listed below:</p>
                    <ul>
                        <li><code>none&nbsp;</code>None</li>
                        <li><code>can&nbsp;&nbsp;</code>Canonical</li>
                        <li><code>com&nbsp;&nbsp;</code>Otherwise Unspecified Compatibility Character</li>
                        <li><code>enc&nbsp;&nbsp;</code>Encircled Form</li>
                        <li><code>fin&nbsp;&nbsp;</code>Final Presentation Form (Arabic)</li>
                        <li><code>font&nbsp;</code>Font Variant</li>
                        <li><code>fra&nbsp;&nbsp;</code>Vulgar Fraction Form</li>
                        <li><code>init&nbsp;</code>Initial Presentation Form (Arabic)</li>
                        <li><code>iso&nbsp;&nbsp;</code>Isolated Presentation Form (Arabic)</li>
                        <li><code>med&nbsp;&nbsp;</code>Medial Presentation Form (Arabic)</li>
                        <li><code>nar&nbsp;&nbsp;</code>Narrow (or Hankaku) Compatibility Character</li>
                        <li><code>nb&nbsp;&nbsp;&nbsp;</code>No No-break Version Of A Space Or Hyphen</li>
                        <li><code>sml&nbsp;&nbsp;</code>Small Variant Form (CNS Compatibility)</li>
                        <li><code>sqr&nbsp;&nbsp;</code>CJK Squared Font Variant</li>
                        <li><code>sub&nbsp;&nbsp;</code>Subscript Form</li>
                        <li><code>sup&nbsp;&nbsp;</code>Superscript Form</li>
                        <li><code>vert&nbsp;</code>Vertical Layout Presentation Form</li>
                        <li><code>wide&nbsp;</code>Wide (or Zenkaku) Compatibility Character</li>
                    </ul>
                </dd>
            </dl>
"""

PROP_GROUP_QUICK_CHECK = """
            <div>
                <p>Reference: <a href="https://www.unicode.org/reports/tr15/" rel="noopener noreferrer" target="_blank">Unicode Standard Annex #15, "Unicode Normalization Forms"</a></p>
                <p>Unicode, being a unifying character set, contains characters that allow similar results to be expressed in different ways. Given that similar text can be written in different ways, we have a problem. How can we determine if two strings are equal ? How can we find a substring in a string?</p>
                <p>The answer is to convert the string to a well-known form, a process known as <strong>normalization</strong>. Unicode normalization is a set of rules based on tables and algorithms. It defines two kinds of normalization equivalence: <strong>canonical</strong> and <strong>compatible</strong>.</p>
                <p>Code point sequences that are defined as <strong>canonically equivalent</strong> are assumed to have the same appearance and meaning when printed or displayed. For example, "Å" (<code>U+212B ANGSTROM SIGN</code>) is canonically equivalent to <strong>BOTH</strong> "Å" (<code>U+00C5 LATIN CAPITAL LETTER A WITH RING ABOVE</code>) and "A" (<code>U+00C5 LATIN CAPITAL LETTER A</code>) + "◌̊" (<code>U+030A COMBINING RING ABOVE</code>).</p>
                <p>Code point sequences that are defined as <strong>compatible</strong> are assumed to have possibly distinct appearances, but the same meaning in some contexts. An example of this could be representations of the decimal digit 6: "Ⅵ" (<code>U+2165 ROMAN NUMERAL SIX</code>) and "⑥" (<code>U+2465 CIRCLED DIGIT SIX</code>). In one particular sense they are the same, but there are many other qualities that are different between then.</p>
                <p>Compatible equivalence is a superset of canonical equivalence. In other words each canonical mapping is also a compatible one, but not the other way around.</p>
                <p><strong>Composition</strong> is the process of combining marks with base letters (multiple code points are replaced by single points whenever possible). <strong>Decomposition</strong> is the process of taking already composed characters apart (single code points are split into multiple ones). Both processes are recursive.</p>
                <p>An additional difficulty is that the normalized ordering of multiple consecutive combining marks must be defined. This is done using a concept called the Canonical Combining Class or CCC, a Unicode character property (available as the <strong>combiningClass</strong> property in the <strong>Basic</strong> property group).</p>
                <p>When you take all of these concepts into consideration, four normalization forms are defined:</p>
                <ul>
                    <li><code>NFD&nbsp;&nbsp;</code>Canonical decomposition and ordering</li>
                    <li><code>NFC&nbsp;&nbsp;</code>Composition after canonical decomposition and ordering</li>
                    <li><code>NFKD&nbsp;</code>Compatible decomposition and ordering</li>
                    <li><code>NFKC&nbsp;</code>Composition after compatible decomposition and ordering</li>
                </ul>
            </div>
            <dl>
                <dt><strong>NFD_QC</strong></dt>
                <dd>Canonical decomposition and ordering</dd>
                <dt><strong>NFC_QC</strong></dt>
                <dd>Composition after canonical decomposition and ordering</dd>
                <dt><strong>NFKD_QC</strong></dt>
                <dd>Compatible decomposition and ordering</dd>
                <dt><strong>NFKC_QC</strong></dt>
                <dd>Composition after compatible decomposition and ordering</dd>
            </dl>
"""

PROP_GROUP_NUMERIC = """
            <div>Reference: <a href="https://www.unicode.org/versions/Unicode15.0.0/ch04.pdf#page=18" rel="noopener noreferrer" target="_blank">Unicode Standard, Section 4.6, <i>Numeric Value</i></a></div>
            <dl>
                <dt><strong>numericType</strong></dt>
                <dd>
                    <p>If a character is normally used as a number, it will be assigned a value other than <code>None</code>, which is the default value used for all non-number characters:</p>
                    <ul>
                        <li><code>None&nbsp;</code>None</li>
                        <li><code>De&nbsp;&nbsp;&nbsp;</code>Decimal</li>
                        <li><code>Di&nbsp;&nbsp;&nbsp;</code>Digit</li>
                        <li><code>Nu&nbsp;&nbsp;&nbsp;</code>Numeric</li>
                    </ul>
                </dd>
                <dt><strong>numericValue</strong></dt>
                <dd>
                    <p>If the character has the property value <code><strong>numericValue=Decimal</code></strong>, then the <code>numericValue</code> of that digit is represented with an integer value (limited to the range 0..9) in fields 6, 7, and 8. Characters with the property value <code><strong>numericValue=Decimal</code></strong> are restricted to digits which can be used in a decimal radix positional numeral system and which are encoded in the standard in a contiguous ascending range 0..9.</p>
                    <p>If the character has the property value <code><strong>numericValue=Digit</code></strong>, then the <code>numericValue</code> of that digit is represented with an integer value (limited to the range 0..9) in fields 7 and 8, and field 6 is null. This covers digits that need special handling, such as the compatibility superscript digits. Starting with Unicode 6.3.0, no newly encoded numeric characters will be given <code><strong>numericValue=Digit</code></strong>, nor will existing characters with <code><strong>numericValue=Decimal</code></strong> be changed to <code><strong>numericValue=Digit</code></strong>. The distinction between those two types is not considered useful.</p>
                    <p>If the character has the property value <code><strong>numericValue=Numeric</code></strong>, then the <code>numericValue</code> of that character is represented with a positive or negative integer or rational number in this field, and fields 6 and 7 are null. This includes fractions such as, for example, "1/5" for ⅕ (<code>U+2155 <span>VULGAR FRACTION ONE FIFTH</span></code>).</p>
                </dd>
                <dt><strong>numericValueParsed</strong></dt>
                <dd>(description needed)</dd>
            </dl>
"""

PROP_GROUP_JOINING = """
            <div>Reference: <a href="https://www.unicode.org/versions/Unicode15.0.0/ch09.pdf#page=19" rel="noopener noreferrer" target="_blank">Unicode Standard, Section 9.2, <i>Arabic</i></a></div>
            <dl>
                <dt><strong>joiningType</strong></dt>
                <dd>
                    <p>Each Arabic letter must be depicted by one of a number of possible contextual glyph forms. The appropriate form is determined on the basis of the cursive joining behavior of that character as it interacts with the cursive joining behavior of adjacent characters. In the Unicode Standard, such cursive joining behavior is formally described in terms of values of a character property called <strong>joiningType</strong>. Each Arabic character falls into one of the types listed below:</p>
                    <ul>
                        <li><code>R&nbsp;</code>Right Joining</li>
                        <li><code>L&nbsp;</code>Left Joining</li>
                        <li><code>D&nbsp;</code>Dual Joining</li>
                        <li><code>C&nbsp;</code>Join Causing</li>
                        <li><code>U&nbsp;</code>Non Joining</li>
                        <li><code>T&nbsp;</code>Transparent</li>
                    </ul>
                    <p>Note that for cursive joining scripts which are typically rendered top-to-bottom, rather than right-to-left, <code><strong>joiningType=L</code></strong> conventionally refers to bottom joining, and <code><strong>joiningType=R</code></strong> conventionally refers to top joining.</p>
                </dd>
                <dt><strong>joiningGroup</strong></dt>
                <dd>The group of characters that the character belongs to in cursive joining behavior. For Arabic and Syriac characters.</dd>
                <dt><strong>joiningControl</strong></dt>
                <dd>Boolean value that indicates whether the character has specific functions for control of cursive joining and ligation.</dd>
            </dl>
"""

PROP_GROUP_LINEBREAK = """
            <div>Reference: <a href="https://www.unicode.org/reports/tr41/tr41-30.html#UAX14" rel="noopener noreferrer" target="_blank">Unicode Standard Annex #14, "Unicode Line Breaking Algorithm"</a></div>
            <dl>
                <dt><strong>lineBreak</strong></dt>
                <dd>
                    <p>Line-breaking class of the character. Affects whether a line break must, may, or must not appear before or after the character. The possible values are listed below:</p>
                    <ul>
                        <li><code>AL</code>&nbsp;&nbsp;Ordinary Alphabetic And Symbol</li>
                        <li><code>AI</code>&nbsp;&nbsp;Ambiguous (Alphabetic Or Ideographic)</li>
                        <li><code>BA</code>&nbsp;&nbsp;Break Opportunity After</li>
                        <li><code>B2</code>&nbsp;&nbsp;Break Opportunity Before And After</li>
                        <li><code>BK</code>&nbsp;&nbsp;Mandatory Break</li>
                        <li><code>BB</code>&nbsp;&nbsp;Break Opportunity Before</li>
                        <li><code>CL</code>&nbsp;&nbsp;Closing Punctuation</li>
                        <li><code>CB</code>&nbsp;&nbsp;Contingent Break Opportunity</li>
                        <li><code>CR</code>&nbsp;&nbsp;Carriage Return</li>
                        <li><code>CM</code>&nbsp;&nbsp;Attached Characters And Combining Marks</li>
                        <li><code>GL</code>&nbsp;&nbsp;Non-breaking ("Glue")</li>
                        <li><code>EX</code>&nbsp;&nbsp;Exclamation/Interrogation</li>
                        <li><code>H3</code>&nbsp;&nbsp;Hangul LVT Syllable</li>
                        <li><code>H2</code>&nbsp;&nbsp;Hangul LV Syllable</li>
                        <li><code>ID</code>&nbsp;&nbsp;Ideographic</li>
                        <li><code>HY</code>&nbsp;&nbsp;Hyphen</li>
                        <li><code>IS</code>&nbsp;&nbsp;Infix Separator</li>
                        <li><code>IN</code>&nbsp;&nbsp;Inseparable</li>
                        <li><code>JT</code>&nbsp;&nbsp;Hangul T Jamo</li>
                        <li><code>JL</code>&nbsp;&nbsp;Hangul L Jamo</li>
                        <li><code>LF</code>&nbsp;&nbsp;Line Feed</li>
                        <li><code>JV</code>&nbsp;&nbsp;Hangul V Jamo</li>
                        <li><code>NS</code>&nbsp;&nbsp;Non Starter</li>
                        <li><code>NL</code>&nbsp;&nbsp;Next Line</li>
                        <li><code>OP</code>&nbsp;&nbsp;Opening Punctuation</li>
                        <li><code>NU</code>&nbsp;&nbsp;Numeric</li>
                        <li><code>PR</code>&nbsp;&nbsp;Prefix (Numeric)</li>
                        <li><code>PO</code>&nbsp;&nbsp;Postfix (Numeric)</li>
                        <li><code>SA</code>&nbsp;&nbsp;Complex Context (South East Asian)</li>
                        <li><code>QU</code>&nbsp;&nbsp;Ambiguous Quotation</li>
                        <li><code>SP</code>&nbsp;&nbsp;Space</li>
                        <li><code>SG</code>&nbsp;&nbsp;Surrogates</li>
                        <li><code>WJ</code>&nbsp;&nbsp;Word Joiner</li>
                        <li><code>SY</code>&nbsp;&nbsp;Symbols Allowing Breaks</li>
                        <li><code>ZW</code>&nbsp;&nbsp;Zero Width Spac</li>
                        <li><code>XX</code>&nbsp;&nbsp;Unknown</li>
                    </ul>
                </dd>
            </dl>
"""

PROP_GROUP_EAW = """
            <dl>
                <dt><strong>eastAsianWidth</strong></dt>
                <dd>
                    <p>The width of the character, in terms of East Asian writing systems that distinguish between full width, half width, and narrow. The possible values are listed in <a href="https://www.unicode.org/reports/tr11/" rel="noopener noreferrer" target="_blank">Unicode Standard Annex #11</a>:</p>
                    <ul>
                        <li><code>A&nbsp;&nbsp;</code>East Asian Ambiguous</li>
                        <li><code>F&nbsp;&nbsp;</code>East Asian Fullwidth</li>
                        <li><code>H&nbsp;&nbsp;</code>East Asian Halfwidth</li>
                        <li><code>N&nbsp;&nbsp;</code>Neutral Not East Asian</li>
                        <li><code>Na&nbsp;</code>East Asian Narrow</li>
                        <li><code>W&nbsp;&nbsp;</code>East Asian Wide</li>
                    </ul>
                </dd>
            </dl>
"""

PROP_GROUP_CASE = """
            <dl>
                <dt><strong>uppercase</strong></dt>
                <dd>The uppercase form of the character.</dd>
                <dt><strong>lowercase</strong></dt>
                <dd>The lowercase form of the character.</dd>
                <dt><strong>simpleUppercaseMapping</strong></dt>
                <dd>The uppercase form of the character, if expressible as a single character.</dd>
                <dt><strong>simpleLowercaseMapping</strong></dt>
                <dd>The lowercase form of the character, if expressible as a single character.</dd>
                <dt><strong>simpleTitlecaseMapping</strong></dt>
                <dd>The titlecase form of the character, if expressible as a single character.</dd>
                <dt><strong>simpleCaseFolding</strong></dt>
                <dd>The case-folded (lowercase) form of the character when applying simple folding, which does not change the length of a string (and may thus fail to fold some characters correctly).</dd>
            </dl>
"""

PROP_GROUP_SCRIPT = """
            <dl>
                <dt><strong>script</strong></dt>
                <dd>The script (writing system) to which the character primarily belongs to, such as "Latin," "Greek," or "Common," which indicates a character that is used in different scripts.</dd>
                <dt><strong>scriptExtension</strong></dt>
                <dd>(description needed)</dd>
            </dl>
"""

PROP_GROUP_HANGUL = """
            <dl>
                <dt><strong>hangulSyllableType</strong></dt>
                <dd>
                    <p>Type of syllable, for characters that are Hangul (Korean) syllabic characters. Possible values </p>
                    <ul>
                        <li><code>NA&nbsp;&nbsp;</code>Not Applicable
                        <li><code>L&nbsp;&nbsp;&nbsp;</code>Leading Jamo
                        <li><code>V&nbsp;&nbsp;&nbsp;</code>Vowel Jamo
                        <li><code>T&nbsp;&nbsp;&nbsp;</code>Trailing Jamo
                        <li><code>LV&nbsp;&nbsp;</code>Lv Syllable
                        <li><code>LVT&nbsp;</code>Lvt Syllable
                    </ul>
                </dd>
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
                <dd>Boolean value that indicates whether the character is classified as a dash. This includes characters explicitly designated as dashes and their compatibility equivalents.</dd>
                <dt><strong>hyphen</strong></dt>
                <dd>Boolean value that indicates whether the character is regarded as a hyphen. This refers to those dashes that are used to mark connections between parts of a word and to the Katakana middle dot.</dd>
                <dt><strong>quotationMark</strong></dt>
                <dd>Boolean value that indicates whether the character is used as a quotation mark in some language(s).</dd>
                <dt><strong>terminalPunctuation</strong></dt>
                <dd>Boolean value that indicates whether the character is a punctuation mark that generally marks the end of a textual unit.</dd>
                <dt><strong>sentenceTerminal</strong></dt>
                <dd>Boolean value that indicates whether the character is used to terminate a sentence.</dd>
                <dt><strong>diacritic</strong></dt>
                <dd>Boolean value that indicates whether the character is diacritic. i.e., linguistically modifies another character to which it applies. A diacritic is usually, but not necessarily, a combining character.</dd>
                <dt><strong>extender</strong></dt>
                <dd>Boolean value that indicates whether the principal function of the character is to extend the value or shape of a preceding alphabetic character.</dd>
                <dt><strong>softDotted</strong></dt>
                <dd>Boolean value that indicates whether the character contains a dot that disappears when a diacritic is placed above the character (e.g., "i" and "j" are soft dotted).</dd>
                <dt><strong>alphabetic</strong></dt>
                <dd>Boolean value that indicates whether the character is alphabetic. i.e., a letter or comparable to a letter in usage. True for characters with <strong>generalCategory</strong> value of <strong>Lu</strong>, <strong>Ll</strong>, <strong>Lt</strong>, <strong>Lm</strong>, <strong>Lo</strong>, or <strong>Nl</strong> and additionally for characters with the <strong>otherAlphabetic</strong> property.</dd>
                <dt><strong>math</strong></dt>
                <dd>Boolean value that indicates whether the character is mathematical. This includes characters with Sm (Symbol, math) as the General Category value, and some other characters.</dd>
                <dt><strong>hexDigit</strong></dt>
                <dd>Boolean value that indicates whether the character is used in hexadecimal numbers. This is true for ASCII hexadecimal digits and their fullwidth versions.</dd>
                <dt><strong>asciiHexDigit</strong></dt>
                <dd>Boolean value that indicates whether the character is an ASCII character used to represent hexadecimal numbers (i.e., letters A-F, a-f and digits 0-9).</dd>
                <dt><strong>defaultIgnorableCodePoint</strong></dt>
                <dd>Boolean value that indicates whether the code point should be ignored in automatic processing by default.</dd>
                <dt><strong>logicalOrderException</strong></dt>
                <dd>Boolean value that indicates whether the character belongs to the small set of characters that do not use logical order and hence require special handling in most processing</dd>
                <dt><strong>prependedConcatenationMark</strong></dt>
                <dd>(description needed)</dd>
                <dt><strong>whiteSpace</strong></dt>
                <dd>Boolean value that indicates whether the character should be treated by programming languages as a whitespace character when parsing elements. This concept does not match the more restricted whitespace concept in many programming languages, but it is a generalization of that concept to the "Unicode world."</dd>
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

UNICODE_CHARACTER_PROP_GROUPS_CONTINUED_1 = "<p>⚠️ <strong><i>NOTE: Specifying <code>show_props=Minimum</code> in any request is redundent since the <strong>Minimum</strong> property group is included in all responses.</i></strong></p>\n"

UNICODE_CHARACTER_PROP_GROUPS_CONTINUED_2 = "<p>If you wish to explore the properties of one or more specifc characters, the <code>/v1/characters/{string}</code> endpoint accepts one or more <code>show_props</code> parameters that allow you to specify additional property groups to include in the response:</p>\n"

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