<h2>Unicode API</h2>
<p>This API provides access to detailed information for all characters, blocks and planes in <a href="https://www.unicode.org/versions/Unicode15.0.0/" rel="noopener noreferrer" target="_blank">version 15.0 of the Unicode Standard</a> (released September 13, 2022). In an attempt to adhere to the tenants of <a href="http://en.wikipedia.org/wiki/Representational_State_Transfer" rel="noopener noreferrer" target="_blank">REST</a>, the API is organized around the following principles:</p>
<ul>
    <li>URLs are predictable and resource-oriented.</li>
    <li>Uses standard HTTP verbs and response codes.</li>
    <li>Returns JSON-encoded responses.</li>
</ul>
<details>
  <summary>
    <strong>Project Resources/Contact Info</strong>
  </summary>
    <ul>
        <li><a href="https://unicode-api.aaronluna.dev/" rel="noopener noreferrer" target="_blank">Interactive API Documents (Swagger UI)</a></li>
        <li>Created by Aaron Luna</li>
        <ul>
            <li><a href="https://aaronluna.dev" rel="noopener noreferrer" target="_blank">Personal Website</a></li>
            <li><a href="mailto:contact@aaronluna.dev" rel="noopener noreferrer" class="link">Send Email</a></li>
        </ul>
    </ul>
</details>
<details>
  <summary>
    <strong>Pagination</strong>
  </summary>
    <div>
        <p>All top-level API resources have support for bulk fetches via "list" API methods (i.e., you can list characters/blocks/planes). These API methods share a common structure, taking at least these three parameters: <code>limit</code>, <code>starting_after</code>, and <code>ending_before</code>.</p>
        <p>For your initial request, you should only provide a value for <code>limit</code> (if the default value of <code>limit=10</code> is ok, you do not need to provide values for any parameter in your initial request). The response of a list API method contains a <code>data</code> parameter that represents a single page of results, and a <code>hasMore</code> parameter that indicates whether the list contains more results after this set.</p>
        <p>The <code>starting_after</code> parameter acts as a cursor to navigate between paginated responses, however, the value used for this parameter is different for each endpoint. For <strong>Unicode Characters</strong>, the value of this parameter is the <strong>codepoint</strong> property, while for <strong>Unicode Blocks</strong> the <strong>id</strong> property is used.</p>
        <p>For example, if you request 10 items and the response contains <code>hasMore=true</code>, there are more search results beyond the first 10. If the 10th search result has <code>codepoint=U+0346</code>, you can retrieve the next set of results by sending <code>starting_after=U+0346</code> in a subsequent request.</p>
        <p>The <code>ending_before</code> parameter also acts as a cursor to navigate between pages, but instead of requesting the next set of results it allows you to access previous pages in the list.</p>
        <p>For example, if you previously requested 10 items beyond the first page of results, and the first search result of the current page has <code>codepoint=U+0357</code>, you can retrieve the previous set of results by sending <code>ending_before=U+0357</code> in a subsequent request.</p>
        <p><strong><i>IMPORTANT: Only one of <code>starting_after</code> or <code>ending_before</code> may be used in a request.</i></strong></p>
    </div>
</details>
<details>
  <summary>
    <strong>Search</strong>
  </summary>
    <div>
        <p></p>
    </div>
</details>
<h3>Core Resources</h3>
<details>
  <summary>
    <strong>Unicode Characters</strong>
  </summary>
    <div>
        <p>The <code>UnicodeCharacter</code> object represents a single character/codepoint in the <a href="https://unicode.org/reports/tr44/" rel="noopener noreferrer" target="_blank">Unicode Character Database (UCD)</a>. It contains a rich set of properties that document the purpose and intended representation of the character.</p>
        <details>
  <summary>
    <strong>Endpoints</strong>
  </summary>
    <dl>
        <dt><strong>GET</strong> <code>/v1/characters/{string}</code></dt>
        <dd>Retrieve one or more Character(s)</dd>
        <dt><strong>GET</strong> <code>/v1/characters</code></dt>
        <dd>List Characters</dd>
        <dt><strong>GET</strong> <code>/v1/characters/search</code></dt>
        <dd>Search Characters</dd>
    </dl>
</details>
<h4>The Unicode Character Object</h4>
<p>Each property is assigned to a <strong>property group</strong>. Responses from any <code>character</code> endpoint will only include properties from the <strong>MINIMUM</strong> property group by default. The <code>/v1/characters</code> endpoint accepts one or more <code>show_props</code> parameters that allow you to specify additional property groups to include in the response.</p>
<details>
  <summary>
    <strong>Properties of the <code>UnicodeCharacter</code> object</strong>
  </summary>
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
</details>
</div>
</details>
<details>
  <summary>
    <strong>Unicode Blocks</strong>
  </summary>
<div>
    <p></p>
</div>
</details>
<details>
  <summary>
    <strong>Unicode Planes</strong>
  </summary>
<div>
    <p></p>
</div>
</details>
