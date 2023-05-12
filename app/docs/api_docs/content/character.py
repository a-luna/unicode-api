# flake8: noqa
from app.core.config import settings

CHARACTER_ENDPOINTS = """
            <dl>
                <dt><strong>GET</strong> <code>/v1/characters/{string}</code></dt>
                <dd>Retrieve one or more character(s)<sup class="fn fn1">*</sup></dd>
                <dt><strong>GET</strong> <code>/v1/characters</code></dt>
                <dd>List all characters<sup class="fn fn1">*</sup></dd>
                <dt><strong>GET</strong> <code>/v1/characters/filter</code></dt>
                <dd>List characters that match filter settings<sup class="fn fn2">†</sup></dd>
                <dt><strong>GET</strong> <code>/v1/characters/search</code></dt>
                <dd>Search characters<sup class="fn fn2">†</sup></dd>
            </dl>
            <div class="footnotes">
                <div class="footnote">
                    <sup class="symbol">*</sup><span class="note">Supports requests for all codepoints in the Unicode space (i.e., assigned, reserved, noncharacter, surrogate, and private-use codepoints).</span>
                </div>
                <div class="footnote">
                    <sup class="symbol">†</sup><span class="note">Supports <strong>ONLY</strong> assigned codepoints.</span>
                </div>
            </div>
"""

UNICODE_CHATACTER_OBJECT_INTRO = '<p>The <code>UnicodeCharacter</code> object represents a single character/codepoint in the <a href="https://unicode.org/reports/tr44/" rel="noopener noreferrer" target="_blank">Unicode Character Database (UCD)</a>. It contains a rich set of properties that document the purpose and intended representation of the character.</p>'

UNICODE_CHARACTER_PROP_GROUPS_INTRO = (
    "<p>If each response contained every character property, it would be massively inneficient. To ensure that the API remains responsive and performant while also allowing clients to access the full set of character properties, each property is assigned to a <strong>property group</strong>.</p>"
    + "<p>Since they are designed to return lists of characters, responses from the <code>/v1/characters</code> or <code>/v1/characters/search</code> endpoints will only include properties from the <strong>Minimum</strong> property group:</p>"
)

PROP_GROUP_MINIMUM = """
            <dl>
                <dt><strong>character</strong></dt>
                <dd>A unit of information used for the organization, control, or representation of textual data.</dd>
                <dt><strong>name</strong></dt>
                <dd>A unique string used to identify each character encoded in the Unicode standard.</dd>
                <dt><strong>codepoint</strong></dt>
                <dd>A number in the range from <code>U+0000</code> to <code>U+10FFFF</code> assigned to a single character</dd>
                <dt><strong>uriEncoded</strong></dt>
                <dd>The character as a URI encoded string. A URI is a string that identifies an abstract or physical resource on the internet (The specification for the URI format is defined in <a href="https://www.rfc-editor.org/rfc/rfc3986" rel="noopener noreferrer" target="_blank">RFC 3986</a>). The string must contain only a defined subset of characters from the standard 128 ASCII character set, any other characters must be replaced by an escape sequence representing the UTF-8 encoding of the character. For example, ∑ (<code>U+2211 <span>N-ARY SUMMATION</span></code>) is equal to <code>0xE2 0x88 0x91</code> in UTF-8 encoding. When used as part of a URI, this character must be escaped using the URI-escaped string <code>%E2%88%91</code>.</dd>
            </dl>
"""

UNICODE_CHARACTER_PROP_GROUPS_CONTINUED_1 = "<p>⚠️ <strong><i>NOTE: Specifying <code>show_props=Minimum</code> in any request is redundent since the <strong>Minimum</strong> property group is included in all responses.</i></strong></p>\n"

UNICODE_CHARACTER_PROP_GROUPS_CONTINUED_2 = (
    "<p>If you wish to explore the properties of one or more specifc characters, the <code>/v1/characters/{string}</code> endpoint accepts one or more <code>show_props</code> parameters that allow you to specify additional property groups to include in the response.</p>"
    + f'<p>For example, you could view the properties from groups <strong>UTF-8</strong>, <strong>Numeric</strong>, and <strong>Script</strong> for the character Ⱒ (<code>U+2C22 <span>GLAGOLITIC CAPITAL LETTER SPIDERY HA</span></code>) by submitting the following request: <a href="{settings.API_ROOT}/v1/characters/%E2%B0%A2?show_props=UTF8&show_props=Numeric&show_props=Script" rel="noopener noreferrer" target="_blank">/v1/characters/%E2%B0%A2?show_props=UTF8&show_props=Numeric&show_props=Script</a>.</p>\n'
)

PROP_GROUP_BASIC = """
            <dl>
                <dt><strong>block</strong></dt>
                <dd>Name of the block to which the character belongs. Each block is a uniquely named, continuous, non-overlapping range of code points, containing a multiple of 16 code points, and starting at a location that is a multiple of 16. A block may contain unassigned code points, which are reserved.</dd>
                <dt><strong>plane</strong></dt>
                <dd>A range of 65,536 (<code>0x10000</code>) contiguous Unicode code points, where the first code point is an integer multiple of 65,536 (<code>0x10000</code>). Planes are numbered from 0 to 16, with the number being the first code point of the plane divided by 65,536. Thus Plane 0 is <code>U+0000...U+FFFF</code>, Plane 1 is <code>U+<strong>1</strong>0000...U+<strong>1</strong>FFFF</code>, ..., and Plane 16 (<code>0x<strong>10</strong></code>) is <code>U+<strong>10</strong>0000...<strong>10</strong>FFFF</code>.<br />The vast majority of commonly used characters are located in Plane 0, which is called the <strong>Basic Multilingual Plane (BMP)</strong>. Planes 1-16 are collectively referred to as <i>supplementary planes</i>.</dd>
                <dt><strong>age</strong></dt>
                <dd>The version of Unicode in which the character was assigned to a codepoint, such as "1.1" or "4.0.".</dd>
                <dt><strong>generalCategory</strong></dt>
                <dd>The <a href="https://www.unicode.org/versions/latest/ch04.pdf#G124142" rel="noopener noreferrer" target="_blank">General Category</a> that this character belongs to (e.g., letters, numbers, punctuation, symbols, etc.). The full list of values which are valid for this property is defined in <a href="http://www.unicode.org/reports/tr44/#General_Category_Values" rel="noopener noreferrer" target="_blank">Unicode Standard Annex #44</a></dd>
                <dt><strong>combiningClass</strong></dt>
                <dd>Specifies, with a numeric code, which sequences of combining marks are to be considered canonically equivalent and which are not. This is used in the Canonical Ordering Algorithm and in normalization. For more info, please see <a href="https://www.unicode.org/versions/Unicode15.0.0/ch04.pdf#page=11" rel="noopener noreferrer" target="_blank">Unicode Standard Section 4.3</a>.</dd>
                <dt><strong>htmlEntities</strong></dt>
                <dd>A string begining with an ampersand (&) character and ending with a semicolon (;). Entities are used to display reserved characters (e.g., '<' in an HTML document) or invisible characters (e.g., non-breaking spaces). For more info, please see the <a href="https://developer.mozilla.org/en-US/docs/Glossary/Entity" rel="noopener noreferrer" target="_blank">MDN entry for HTML Entities</a>.</dd>
            </dl>
"""

PROP_GROUP_UTF8 = """
            <div>UTF-8 is a method of encoding the Unicode character set where each code unit is equal to 8-bits. UTF-8 is backwards-compatible with ASCII and all codepoints in range 0-127 are represented as a single byte. Codepoints greater than 127 are represented as a sequence of 2-4 bytes.</div>
            <dl>
                <dt><strong>utf8</strong></dt>
                <dd>The UTF-8 encoded value for the character as a hex string.</dd>
                <dt><strong>utf8HexBytes</strong></dt>
                <dd>The byte sequence for the UTF-8 encoded value for the character. This property returns a list of strings, hex values (base-16) in range <code>00-FF</code>.</dd>
                <dt><strong>utf8DecBytes</strong></dt>
                <dd>The byte sequence for the UTF-8 encoded value for the character. This property returns a list of integers, decimal values (base-10) in range 0-127</dd>
            </dl>
"""

PROP_GROUP_UTF16 = """
            <div>UTF-16 is a method of encoding the Unicode character set where each code unit is equal to 16-bits. All codepoints in the BMP (Plane 0) can be represented as a single 16-bit code unit (2 bytes). Code points in the supplementary planes (Planes 1-16) are represented as pairs of 16-bit code units (4 bytes).</div>
            <dl>
                <dt><strong>utf16</strong></dt>
                <dd>The UTF-16 encoded value for the character as a hex string.</dd>
                <dt><strong>utf16HexBytes</strong></dt>
                <dd>The byte sequence for the UTF-16 encoded value for the character. This property returns a list of strings, hex values (base-16) in range <code>0000-FFFF</code>.</dd>
                <dt><strong>utf16DecBytes</strong></dt>
                <dd>The byte sequence for the UTF-16 encoded value for the character. This property returns a list of integers, decimal values (base-10) in range 0-65,535</dd>
            </dl>
"""

PROP_GROUP_UTF32 = """
            <div>UTF-32 is a method of encoding the Unicode character set where each code unit is equal to 32-bits. UTF-32 is the simplest Unicode encoding form. Each Unicode code point is represented directly by a single 32-bit code unit. Because of this, UTF-32 has a one-to-one relationship between encoded character and code unit; it is a fixed-width character encoding form.</div>
            <dl>
                <dt><strong>utf32</strong></dt>
                <dd>The UTF-32 encoded value for the character as a hex string.</dd>
                <dt><strong>utf32HexBytes</strong></dt>
                <dd>The byte sequence for the UTF-32 encoded value for the character. This property returns a list of strings, hex values (base-16) in range <code>00000000-0010FFFF</code>.</dd>
                <dt><strong>utf32DecBytes</strong></dt>
                <dd>The byte sequence for the UTF-32 encoded value for the character. This property returns a list of integers, decimal values (base-10) in range 0-1,114,111</dd>
            </dl>
"""

PROP_GROUP_BIDIRECTIONALITY = """
            <div class="prop-group-ref">Reference: <a href="https://www.unicode.org/reports/tr9/" rel="noopener noreferrer" target="_blank">Unicode Standard Annex #9, "Unicode Bidirectional Algorithm"</a></div>
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
            <div class="prop-group-ref">Reference: <a href="https://www.unicode.org/versions/Unicode15.0.0/ch03.pdf#page=46" rel="noopener noreferrer" target="_blank">Unicode Standard, Section 3.7, <i>Decomposition</i></a></div>
            <dl>
                <dt><strong>decompositionType</strong></dt>
                <dd>
                    <p>The type of the decomposition (canonical or compatibility). The possible values are listed below:</p>
                    <ul>
                        <li><code>none</code>&nbsp;None</li>
                        <li><code>can</code>&nbsp;&nbsp;Canonical</li>
                        <li><code>com</code>&nbsp;&nbsp;Otherwise Unspecified Compatibility Character</li>
                        <li><code>enc</code>&nbsp;&nbsp;Encircled Form</li>
                        <li><code>fin</code>&nbsp;&nbsp;Final Presentation Form (Arabic)</li>
                        <li><code>font</code>&nbsp;Font Variant</li>
                        <li><code>fra</code>&nbsp;&nbsp;Vulgar Fraction Form</li>
                        <li><code>init</code>&nbsp;Initial Presentation Form (Arabic)</li>
                        <li><code>iso</code>&nbsp;&nbsp;Isolated Presentation Form (Arabic)</li>
                        <li><code>med</code>&nbsp;&nbsp;Medial Presentation Form (Arabic)</li>
                        <li><code>nar</code>&nbsp;&nbsp;Narrow (or Hankaku) Compatibility Character</li>
                        <li><code>nb</code>&nbsp;&nbsp;&nbsp;No No-break Version Of A Space Or Hyphen</li>
                        <li><code>sml</code>&nbsp;&nbsp;Small Variant Form (CNS Compatibility)</li>
                        <li><code>sqr</code>&nbsp;&nbsp;CJK Squared Font Variant</li>
                        <li><code>sub</code>&nbsp;&nbsp;Subscript Form</li>
                        <li><code>sup</code>&nbsp;&nbsp;Superscript Form</li>
                        <li><code>vert</code>&nbsp;Vertical Layout Presentation Form</li>
                        <li><code>wide</code>&nbsp;Wide (or Zenkaku) Compatibility Character</li>
                    </ul>
                </dd>
            </dl>
"""

PROP_GROUP_QUICK_CHECK = """
            <div class="prop-group-ref">Reference: <a href="https://www.unicode.org/reports/tr15/" rel="noopener noreferrer" target="_blank">Unicode Standard Annex #15, "Unicode Normalization Forms"</a></div>
            <div>
                <p>Unicode, being a unifying character set, contains characters that allow similar results to be expressed in different ways. Given that similar text can be written in different ways, we have a problem. How can we determine if two strings are equal ? How can we find a substring in a string?</p>
                <p>The answer is to convert the string to a well-known form, a process known as <strong>normalization</strong>. Unicode normalization is a set of rules based on tables and algorithms. It defines two kinds of normalization equivalence: <strong>canonical</strong> and <strong>compatible</strong>.</p>
                <p>Code point sequences that are defined as <strong>canonically equivalent</strong> are assumed to have the same appearance and meaning when printed or displayed. For example, "Å" (<code>U+212B ANGSTROM SIGN</code>) is canonically equivalent to <strong>BOTH</strong> "Å" (<code>U+00C5 LATIN CAPITAL LETTER A WITH RING ABOVE</code>) and "A" (<code>U+00C5 LATIN CAPITAL LETTER A</code>) + "◌̊" (<code>U+030A COMBINING RING ABOVE</code>).</p>
                <p>Code point sequences that are defined as <strong>compatible</strong> are assumed to have possibly distinct appearances, but the same meaning in some contexts. An example of this could be representations of the decimal digit 6: "Ⅵ" (<code>U+2165 ROMAN NUMERAL SIX</code>) and "⑥" (<code>U+2465 CIRCLED DIGIT SIX</code>). In one particular sense they are the same, but there are many other qualities that are different between then.</p>
                <p>Compatible equivalence is a superset of canonical equivalence. In other words each canonical mapping is also a compatible one, but not the other way around.</p>
                <p><strong>Composition</strong> is the process of combining marks with base letters (multiple code points are replaced by single points whenever possible). <strong>Decomposition</strong> is the process of taking already composed characters apart (single code points are split into multiple ones). Both processes are recursive.</p>
                <p>An additional difficulty is that the normalized ordering of multiple consecutive combining marks must be defined. This is done using a concept called the Canonical Combining Class or CCC, a Unicode character property (available as the <strong>combiningClass</strong> property in the <strong>Basic</strong> property group).</p>
                <p>When you take all of these concepts into consideration, four normalization forms are defined:</p>
                <ul>
                    <li><code>NFD</code>&nbsp;&nbsp;Canonical decomposition and ordering</li>
                    <li><code>NFC</code>&nbsp;&nbsp;Composition after canonical decomposition and ordering</li>
                    <li><code>NFKD</code>&nbsp;Compatible decomposition and ordering</li>
                    <li><code>NFKC</code>&nbsp;Composition after compatible decomposition and ordering</li>
                </ul>
                <p>In an effort to make the process of normalizing/determining if a string is already normalized less tedious and complex, four “quick check” properties exist for each character (<strong>NFD_QC</strong>, <strong>NFC_QC</strong>, <strong>NFKD_QC</strong>, and <strong>NFKC_QC</strong>, one for each normalization form).</p>
                <p>These properties allow implementations to quickly determine whether a string is in a particular Normalization Form. This is, in general, many times faster than normalizing and then comparing.</p>
            </div>
            <dl>
                <dt><strong>NFD_QC</strong></dt>
                <dd><strong>NFD_QC</strong> stands for <strong>Normalization Form D Quick Check</strong>. This property is used to quickly check if a character is already in NFD form, and thus does not need to be further normalized.</dd>
                <dt><strong>NFC_QC</strong></dt>
                <dd><strong>NFC_QC</strong> stands for <strong>Normalization Form C Quick Check</strong>. This property is used to quickly check if a character is already in NFC form, and thus does not need to be further normalized.</dd>
                <dt><strong>NFKD_QC</strong></dt>
                <dd><strong>NFKD_QC</strong> stands for <strong>Normalization Form KD Quick Check</strong>. This property is used to quickly check if a character is already in NFKD form, and thus does not need to be further normalized.</dd>
                <dt><strong>NFKC_QC</strong></dt>
                <dd><strong>NFKC_QC</strong> stands for <strong>Normalization Form KC Quick Check</strong>. This property is used to quickly check if a character is already in NFKC form, and thus does not need to be further normalized.</dd>
            </dl>
"""

PROP_GROUP_NUMERIC = """
            <div class="prop-group-ref">Reference: <a href="https://www.unicode.org/versions/Unicode15.0.0/ch04.pdf#page=18" rel="noopener noreferrer" target="_blank">Unicode Standard, Section 4.6, <i>Numeric Value</i></a></div>
            <dl>
                <dt><strong>numericType</strong></dt>
                <dd>
                    <p>If a character is normally used as a number, it will be assigned a value other than <code>None</code>, which is the default value used for all non-number characters:</p>
                    <ul>
                        <li><code>None</code>&nbsp;None</li>
                        <li><code>De</code>&nbsp;&nbsp;&nbsp;Decimal</li>
                        <li><code>Di</code>&nbsp;&nbsp;&nbsp;Digit</li>
                        <li><code>Nu</code>&nbsp;&nbsp;&nbsp;Numeric</li>
                    </ul>
                </dd>
                <dt><strong>numericValue</strong></dt>
                <dd>
                    <p>If the character has the property value <code><strong>numericValue=Decimal</code></strong>, then the <code>numericValue</code> of that digit is represented with an integer value (limited to the range 0..9).</p>
                    <p>If the character has the property value <code><strong>numericValue=Digit</code></strong>, then the <code>numericValue</code> of that digit is represented with an integer value (limited to the range 0..9). This covers digits that need special handling, such as the compatibility superscript digits. Starting with Unicode 6.3.0, no newly encoded numeric characters will be given <code><strong>numericValue=Digit</code></strong>, nor will existing characters with <code><strong>numericValue=Decimal</code></strong> be changed to <code><strong>numericValue=Digit</code></strong>. The distinction between those two types is not considered useful.</p>
                    <p>If the character has the property value <code><strong>numericValue=Numeric</code></strong>, then the <code>numericValue</code> of that character is represented with a positive or negative integer or rational number. This includes fractions such as, for example, "1/5" for ⅕ (<code>U+2155 <span>VULGAR FRACTION ONE FIFTH</span></code>).</p>
                </dd>
                <dt><strong>numericValueParsed</strong></dt>
                <dd><strong><i>This is NOT a property from the Unicode Standard.</i></strong> This is a floating point version of the <strong>numericValue</strong> property (which is a string value). For example, <code>0.2</code> for ⅕ (<code>U+2155 <span>VULGAR FRACTION ONE FIFTH</span></code>)
                </dd>
            </dl>
"""

PROP_GROUP_JOINING = """
            <div class="prop-group-ref">Reference: <a href="https://www.unicode.org/versions/Unicode15.0.0/ch09.pdf#page=19" rel="noopener noreferrer" target="_blank">Unicode Standard, Section 9.2, <i>Arabic</i></a></div>
            <dl>
                <dt><strong>joiningType</strong></dt>
                <dd>
                    <p>Each Arabic letter must be depicted by one of a number of possible contextual glyph forms. The appropriate form is determined on the basis of the cursive joining behavior of that character as it interacts with the cursive joining behavior of adjacent characters. In the Unicode Standard, such cursive joining behavior is formally described in terms of values of a character property called <strong>joiningType</strong>. Each Arabic character falls into one of the types listed below:</p>
                    <ul>
                        <li><code>R</code>&nbsp;Right Joining</li>
                        <li><code>L</code>&nbsp;Left Joining</li>
                        <li><code>D</code>&nbsp;Dual Joining</li>
                        <li><code>C</code>&nbsp;Join Causing</li>
                        <li><code>U</code>&nbsp;Non Joining</li>
                        <li><code>T</code>&nbsp;Transparent</li>
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
            <div class="prop-group-ref">Reference: <a href="https://www.unicode.org/reports/tr14/" rel="noopener noreferrer" target="_blank">Unicode Standard Annex #14, "Unicode Line Breaking Algorithm"</a></div>
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
            <div class="prop-group-ref">Reference: <a href="https://www.unicode.org/reports/tr11/" rel="noopener noreferrer" target="_blank">Unicode Standard Annex #11, "East Asian Width"</a></div>
            <dl>
                <dt><strong>eastAsianWidth</strong></dt>
                <dd>
                    <p>The width of the character, in terms of East Asian writing systems that distinguish between full width, half width, and narrow. The possible values are listed in <a href="https://www.unicode.org/reports/tr11/" rel="noopener noreferrer" target="_blank">Unicode Standard Annex #11</a>:</p>
                    <ul>
                        <li><code>A</code>&nbsp;&nbsp;East Asian Ambiguous</li>
                        <li><code>F</code>&nbsp;&nbsp;East Asian Fullwidth</li>
                        <li><code>H</code>&nbsp;&nbsp;East Asian Halfwidth</li>
                        <li><code>N</code>&nbsp;&nbsp;Neutral Not East Asian</li>
                        <li><code>Na</code>&nbsp;East Asian Narrow</li>
                        <li><code>W</code>&nbsp;&nbsp;East Asian Wide</li>
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
            <div class="prop-group-ref">Reference: <a href="https://www.unicode.org/reports/tr24/" rel="noopener noreferrer" target="_blank">Unicode Standard Annex #24, "Unicode Script Property"</a></div>
            <dl>
                <dt><strong>script</strong></dt>
                <dd>The script (writing system) to which the character primarily belongs to, such as "Latin," "Greek," or "Common," which indicates a character that is used in different scripts.</dd>
                <dt><strong>scriptExtensions</strong></dt>
                <dd>
                    <p>Further refines the script category of a character by providing additional information about the character's usage and context. This property allows for more specific categorization of characters that may have multiple uses or are used in multiple scripts.</p>
                    <p>The script extensions property can also be used to indicate characters that are used in multiple scripts, such as characters that are used in both Latin and Cyrillic scripts.</p>
                </dd>
            </dl>
"""

PROP_GROUP_HANGUL = """
            <dl>
                <dt><strong>hangulSyllableType</strong></dt>
                <dd>
                    <p>Type of syllable, for characters that are Hangul (Korean) syllabic characters. Possible values </p>
                    <ul>
                        <li><code>NA</code>&nbsp;&nbsp;Not Applicable
                        <li><code>L</code>&nbsp;&nbsp;&nbsp;Leading Jamo
                        <li><code>V</code>&nbsp;&nbsp;&nbsp;Vowel Jamo
                        <li><code>T</code>&nbsp;&nbsp;&nbsp;Trailing Jamo
                        <li><code>LV</code>&nbsp;&nbsp;Lv Syllable
                        <li><code>LVT</code>&nbsp;Lvt Syllable
                    </ul>
                </dd>
            </dl>
"""

PROP_GROUP_INDIC = """
            <dl>
                <dt><strong>indicSyllabicCategory</strong></dt>
                <dd>Used to identify the type of syllable that a character belongs to, such as a vowel, consonant, or a combination of both.</dd>
                <dt><strong>indicMatraCategory</strong></dt>
                <dd>Used to identify the type of matra (vowel sign) associated with a character, such as a short or long vowel sign.</dd>
                <dt><strong>indicPositionalCategory</strong></dt>
                <dd>Used to identify the position of a character in a syllable, such as the initial, medial, or final position.</dd>
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
                <dd>Boolean value that indicates whether the character belongs to a small class of visible format controls, which precede and then span a sequence of other characters, usually digits. These have also been known as "subtending marks", because most of them take a form which visually extends underneath the sequence of following digits.</dd>
                <dt><strong>whiteSpace</strong></dt>
                <dd>Boolean value that indicates whether the character should be treated by programming languages as a whitespace character when parsing elements. This concept does not match the more restricted whitespace concept in many programming languages, but it is a generalization of that concept to the "Unicode world."</dd>
                <dt><strong>verticalOrientation</strong></dt>
                <dd>A property used to establish a default for the correct orientation of characters when used in vertical text layout, as described in <a href="https://www.unicode.org/reports/tr50/" rel="noopener noreferrer" target="_blank">Unicode Standard Annex #50, "Unicode Vertical Text Layout"</a></dd>
                <dt><strong>regionalIndicator</strong></dt>
                <dd>
                    <p>The regional indicator symbols are a set of 26 alphabetic Unicode characters (A–Z) intended to be used to encode <a href="https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2" rel="noopener noreferrer" target="_blank">ISO 3166-1 alpha-2 two-letter country codes</a> in a way that allows optional special treatment.</p>
                    <p>They are encoded in the range 🇦 (<code>U+1F1E6 <span>REGIONAL INDICATOR SYMBOL LETTER A</span></code>) to 🇿 (<code>U+1F1FF <span>REGIONAL INDICATOR SYMBOL LETTER Z</span></code>) Within the <strong>Enclosed Alphanumeric Supplement</strong> block in the <strong>Supplementary Multilingual Plane.</strong></p>
                    <p>These were defined as an alternative to encoding separate characters for each country flag. Although they can be displayed as Roman letters, it is intended that implementations may choose to display them in other ways, such as by using national flags.</p>
                    <p>For example, since the ISO 3166-1 alpha-2 country code for Ukraine is <code>UA</code>, when the characters 🇺 (<code>U+1F1FA</code>) and 🇦 (<code>U+1F1E6</code>) are placed next to eachother the Ukrainian flag should be rendered: 🇺🇦.</p>
                </dd>
            </dl>
"""

PROP_GROUP_EMOJI = """
            <div class="prop-group-ref">Reference: <a href="https://www.unicode.org/reports/tr51/" rel="noopener noreferrer" target="_blank">Unicode Technical Standard #51, "Unicode Emoji"</a></div>
            <dl>
                <dt><strong>emoji</strong></dt>
                <dd>Boolean value that indicates whether the character is recommended for use as emoji.</dd>
                <dt><strong>emojiPresentation</strong></dt>
                <dd>Boolean value that indicates whether the character has emoji presentation by default.</dd>
                <dt><strong>emojiModifier</strong></dt>
                <dd>Boolean value that indicates whether the character is used as an emoji modifier. Currently this includes only the skin tone modifier characters.</dd>
                <dt><strong>emojiModifierBase</strong></dt>
                <dd>Boolean value that indicates whether the character can serve as a base for emoji modifiers.</dd>
                <dt><strong>emojiComponent</strong></dt>
                <dd>Boolean value that indicates whether the character is used in emoji sequences but normally does not appear on emoji keyboards as a separate choice (e.g., keycap base characters or Regional_Indicator characters).</dd>
                <dt><strong>extendedPictographic</strong></dt>
                <dd>Boolean value that indicates whether the character is a pictographic symbol or otherwise similar in kind to characters with the Emoji property. This enables segmentation rules involving emoji to be specified stably, even in cases where an existing non-emoji pictographic symbol later comes to be treated as an emoji.</dd>
            </dl>
"""
