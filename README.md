<h1>Unicode API</h1>
<ul class="toc">
	<li>
		<a href="#introduction">Introduction</a>
	</li>
	<li>
		<a href="#project-resources-contact-info">Project Resources/Contact Info</a>
	</li>
	<li>
		<a href="#pagination">Pagination</a>
	</li>
	<li>
		<a href="#search">Search</a>
	</li>
	<li>
		<a href="#loose-matching">Loose Matching</a>
	</li>
	<li>
		<a href="#core-resources">Core Resources</a>
		<ul>
			<li>
				<a href="#unicode-characters">Unicode Characters</a>
				<ul>
					<li>
						<a href="#character-api-endpoints">API Endpoints</a>
					</li>
					<li>
						<a href="#the-unicodecharacter-object">The <code>UnicodeCharacter</code> Object</a>
					</li>
					<li>
						<a href="#unicodecharacter-property-groups"><code>UnicodeCharacter</code> Property Groups</a>
					</li>
					<li>
						<a href="#verbosity">Verbosity</a>
					</li>
				</ul>
			</li>
			<li>
				<a href="#unicode-codepoints">Unicode Codepoints</a>
				<ul>
					<li>
						<a href="#codepoint-api-endpoints">API Endpoints</a>
					</li>
				</ul>
			</li>
			<li>
				<a href="#unicode-blocks">Unicode Blocks</a>
				<ul>
					<li>
						<a href="#block-api-endpoints">API Endpoints</a>
					</li>
					<li>
						<a href="#the-unicodeblock-object">The <code>UnicodeBlock</code> Object</a>
					</li>
				</ul>
			</li>
			<li>
				<a href="#unicode-planes">Unicode Planes</a>
				<ul>
					<li>
						<a href="#plane-api-endpoints">API Endpoints</a>
					</li>
					<li>
						<a href="#the-unicodeplane-object">The <code>UnicodePlane</code> Object</a>
					</li>
				</ul>
			</li>
		</ul>
	</li>
</ul>
<h2 id="introduction">Introduction</h2>
<p>This API provides access to detailed information for all characters, blocks and planes in <a href="https://www.unicode.org/versions/Unicode15.0.0/" rel="noopener noreferrer" target="_blank">version 15.0.0 of the Unicode Standard</a> (released Sep 13, 2022). In an attempt to adhere to the tenants of <a href="http://en.wikipedia.org/wiki/Representational_State_Transfer" rel="noopener noreferrer" target="_blank">REST</a>, the API is organized around the following principles:</p>
<ul class="api-principles">
    <li>URLs are predictable and resource-oriented.</li>
    <li>Uses standard HTTP verbs and response codes.</li>
    <li>Returns JSON-encoded responses.</li>
</ul>
<h2 id="project-resources-contact-info">Project Resources/Contact Info</h2>
<ul>
    <li><a href="https://unicode-api.aaronluna.dev/" rel="noopener noreferrer" target="_blank">Interactive API Documents (Swagger UI)</a></li>
    <li>Created by Aaron Luna</li>
    <ul>
        <li><a href="https://aaronluna.dev" rel="noopener noreferrer" target="_blank">Personal Website</a></li>
        <li><a href="mailto:contact@aaronluna.dev">Send Email</a></li>
    </ul>
</ul>
<h2 id="pagination">Pagination</h2>
<div>
    <p>The top-level API resources for <strong>Unicode Characters</strong> and <strong>Unicode Blocks</strong> have support for retrieving all character/block objects via "list" API methods. These API methods (<code>/v1/characters</code> and <code>/v1/blocks</code>) share a common structure, taking at least these three parameters: <code>limit</code>, <code>starting_after</code>, and <code>ending_before</code>.</p>
    <p>For your initial request, you should only provide a value for <code>limit</code> (if the default value of <code>limit=10</code> is ok, you do not need to provide values for any parameter in your initial request). The response of a list API method contains a <code>data</code> parameter that represents a single page of results, and a <code>hasMore</code> parameter that indicates whether the list contains more results after this set.</p>
    <p>The <code>starting_after</code> parameter acts as a cursor to navigate between paginated responses, however, the value used for this parameter is different for each endpoint. For <strong>Unicode Characters</strong>, the value of this parameter is the <code>codepoint</code> property, while for <strong>Unicode Blocks</strong> the <code>id</code> property is used.</p>
    <p>For example, if you request 10 items and the response contains <code>hasMore=true</code>, there are more search results beyond the first 10. If the 10th search result has <code>codepoint=U+0346</code>, you can retrieve the next set of results by sending <code>starting_after=U+0346</code> in a subsequent request.</p>
    <p>The <code>ending_before</code> parameter also acts as a cursor to navigate between pages, but instead of requesting the next set of results it allows you to access previous pages in the list.</p>
    <p>For example, if you previously requested 10 items beyond the first page of results, and the first search result of the current page has <code>codepoint=U+0357</code>, you can retrieve the previous set of results by sending <code>ending_before=U+0357</code> in a subsequent request.</p>
    <p><span class="alert">⚠️</span> <strong><i>IMPORTANT: Only one of <code>starting_after</code> or <code>ending_before</code> may be used in a request, sending a value for both parameters will produce a response with status <code>400 Bad Request</code></i></strong>.</p>
</div>
<h2 id="search">Search</h2>
<div>
    <p>The top-level API resources for <strong>Unicode Characters</strong> and <strong>Unicode Blocks</strong> also have support for retrieval via "search" API methods. These API methods (<code>/v1/characters/search</code> and <code>/v1/blocks/search</code>) share an identical structure, taking the same four parameters: <code>name</code>, <code>min_score</code>, <code>per_page</code>, and <code>page</code>.</p>
    <p>The <code>name</code> parameter is the search term and is used to retrieve a character/block using the official name defined in the UCD. Since a <a href="https://en.wikipedia.org/wiki/Approximate_string_matching" rel="noopener noreferrer" target="_blank">fuzzy search algorithm</a> is used for this process, the value of <code>name</code> does not need to be an exact match with a character/block name.</p>
    <p>The response will contain a <code>results</code> parameter that represents the characters/blocks that matched your query. Each object in this list has a <code>score</code> property which is a number ranging from <strong>0-100</strong> that describes how similar the character/block name is to the <code>name</code> value provided by the user (A value of 100 means that the <code>name</code> provided by the user is an exact match with a character/block name). The list contains all results where <code>score</code> &gt;= <code>min_score</code>, sorted by <code>score</code> (the first element in the list being the <i><strong>most similar</strong></i>).</p>
    <p>The default value for <code>min_score</code> is <strong>80</strong>, however if your request is returning zero results, you can lower this value to potentially surface lower-quality results. Keep in mind, the lowest value for <code>min_score</code> that is permitted is <strong>70</strong>, since the relevence of results quickly drops off around a score of <strong>72</strong>, often producing hundreds of results with no relevance to the search term.</p>
    <p>The <code>per_page</code> parameter controls how many results are included in a single response. The response will include a <code>hasMore</code> parameter that indicates whether there are more search results beyond the current page, as well as <code>currentPage</code> and <code>totalResults</code> parameters. If <code>hasMore=true</code>, the response will also contain a <code>nextPage</code> parameter.</p>
    <p>For example, if you receive a response to a search request with <code>hasMore=true</code> and <code>nextPage=2</code>, you can update your request to include <code>page=2</code> to fetch the next page of results. If the next response includes <code>hasMore=true</code> and <code>nextPage=3</code>, update your request to include <code>page=3</code>, etc. Rinse and repeat until you receive a response with <code>hasMore=false</code>, indicating that you have received the final set of search results.</p>
</div>
<h2 id="loose-matching">Loose Matching</h2>
<div>
    <p>Unicode specifies a set of rules to be used when comparing symbolic values, such as block names, known as <strong>loose matching rule</strong> <a href="https://www.unicode.org/reports/tr44/#UAX44-LM3" rel="noopener noreferrer" target="_blank">UAX44-LM3</a>. The algotithm for UAX44-LM3 is simple: <strong><i>Ignore case, whitespace, underscore ('_'), hyphens, and any initial prefix string "is".</i></strong></p>
    <p>This rule applies to many of the parameters that are included with API requests, which avoids returning a 400 response when a parameter name, for example, is sent as 'script', but the expected value is 'Script'. Under UAX44-LM3, both values are equivalent.</p>
    <p>For another example, under this rule the block name "Supplemental Arrows-A" is equivalent to "supplemental_arrows__a" and "SUPPLEMENTALARROWSA" since all three of these strings would be reduced to "supplementalarrowsa" after applying UAX44-LM3. For any query or path parameter that expects the name of a Unicode block, any of these three values could be provided and would be understood to refer to block <code>U+27F0..U+27FF <span>SUPPLEMENTAL ARROWS-A</span></code>.</p>
    <p>Whenever the loose-matching rule applies to a parameter, it will be called out in the docuentation for each individual API endpoint below.</p>
</div>
<h2 id="core-resources">Core Resources</h2>
<h3 id="unicode-characters">Unicode Characters</h3>
<div>
	<details open class='api-endpoints'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><h4 id="character-api-endpoints">API Endpoints</h4></strong>
        </summary>
        <dl>
            <dt><strong>GET</strong> <code>/v1/characters/-/{string}</code></dt>
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
	</details>
	<h4 id="the-unicodecharacter-object">The <code>UnicodeCharacter</code> Object</h4>
    <p>The <code>UnicodeCharacter</code> object represents a single character/codepoint in the <a href="https://unicode.org/reports/tr44/" rel="noopener noreferrer" target="_blank">Unicode Character Database (UCD)</a>. It contains a rich set of properties that document the purpose and intended representation of the character.</p>
    <h4 id="unicodecharacter-property-groups"><code>UnicodeCharacter</code> Property Groups</h4>
    <p>If each response contained every character property, it would be massively inneficient. To ensure that the API remains responsive and performant while also allowing clients to access the full set of character properties, each property is assigned to a <strong>property group</strong>.</p><p>Since they are designed to return lists of characters, responses from the <code>/v1/characters</code> or <code>/v1/characters/search</code> endpoints will only include properties from the <strong>Minimum</strong> property group:</p>
	<details open class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>Minimum</strong></strong>
        </summary>
        <dl>
            <dt><strong>character</strong></dt>
            <dd>A unit of information used for the organization, control, or representation of textual data.</dd>
            <dt><strong>name</strong></dt>
            <dd>A unique string used to identify each character encoded in the Unicode standard.</dd>
            <dt><strong>description</strong><br /><span class="cjk-only">(CJK Characters ONLY)</span></dt>
            <dd>
                <p>An English definition for this character. Definitions are for modern written Chinese and are usually (but not always) the same as the definition in other Chinese dialects or non-Chinese languages.</p>
                <p class="prop-group-ref">More info: <a href="http://www.unicode.org/reports/tr38/#kDefinition" rel="noopener noreferrer" target="_blank">http://www.unicode.org/reports/tr38/#kDefinition</a></p>
            </dd>
            <dt><strong>codepoint</strong></dt>
            <dd>
                <p>In character encoding terminology, a codepoint is a numerical value that maps to a specific character. Code points usually represent a single grapheme—usually a letter, digit, punctuation mark, or whitespace—but sometimes represent symbols, control characters, or formatting. The set of all possible code points within a given encoding/character set make up that encoding's codespace.</p>
                <p>For example, the character encoding scheme ASCII comprises 128 code points in the range <code>00-7F</code>, Extended ASCII comprises 256 code points in the range <code>00-FF</code>, and Unicode comprises 1,114,112 code points in the range <code>0000-10FFFF</code>. The Unicode code space is divided into seventeen planes (the basic multilingual plane, and 16 supplementary planes), each with 65,536 (= 2<sup>16</sup>) code points. Thus the total size of the Unicode code space is 17 × 65,536 = 1,114,112.</p>
            </dd>
            <dt><strong>uriEncoded</strong></dt>
            <dd>
                <p>The character as a URI encoded string. A URI is a string that identifies an abstract or physical resource on the internet (The specification for the URI format is defined in <a href="https://www.rfc-editor.org/rfc/rfc3986" rel="noopener noreferrer" target="_blank">RFC 3986</a>).</p>
                <p>A URI string must contain only a defined subset of characters from the standard 128 ASCII character set, any other characters must be replaced by an escape sequence representing the UTF-8 encoding of the character.</p>
                <p>For example, ∑ (<code>U+2211 <span>N-ARY SUMMATION</span></code>) in UTF-8 encoding is <code>0xE2 0x88 0x91</code>. To include this character in a URI, each UTF-8 byte is prefixed with the <code>%</code> character to produce the URI-encoded string: <code>%E2%88%91</code>.</p>
            </dd>
        </dl>
	</details>
	<br />
	<p><span class="alert">⚠️</span> <strong><i>NOTE: Specifying <code>show_props=Minimum</code> in any request is redundent since the <strong>Minimum</strong> property group is included in all responses.</i></strong></p>
	<p>If you wish to explore the properties of one or more specifc characters, the <code>/v1/characters/-/{string}</code> and <code>/v1/characters/filter</code> endpoints accept one or more <code>show_props</code> parameters that allow you to specify additional property groups to include in the response.</p><p>For example, you could view the properties from groups <strong>UTF-8</strong>, <strong>Numeric</strong>, and <strong>Script</strong> for the character Ⱒ (<code>U+2C22 <span>GLAGOLITIC CAPITAL LETTER SPIDERY HA</span></code>), which is equal to <code>0xE2 0xB0 0xA2</code> in UTF-8 encoding by submitting the following request: <a href="http://localhost:3507/v1/characters/-/%E2%B0%A2?show_props=UTF8&show_props=Numeric&show_props=Script" rel="noopener noreferrer" target="_blank">/v1/characters/-/%E2%B0%A2?show_props=UTF8&show_props=Numeric&show_props=Script</a>.</p>
	<h4 id="verbosity">Verbosity</h4>
	<p>The value of many of the properties that are defined for each character are only meaningful for specific blocks or a small subset of codepoints (e.g., the <code>hangul_syllable_type</code> property will have a <code>(Not Applicable) NA</code> value for all codepoints except those in the four blocks that contain characters from the Hangul writing system).</p><p>By default, the <code>hangul_syllable_type</code> property will <strong>NOT</strong> be included with the response for any character that has this default value even if the user has submitted a request containing <code>show_props=hangul</code> or <code>show_props=all</code>. For actual Hangul characters, the property will be included in the response.</p><p>These properties are removed to make the size of each response as small as possible. Knowing that the 🇺 (<code>U+1F1FA <span>REGIONAL INDICATOR SYMBOL LETTER U</span></code>) character has the value <code>hangul_syllable_type=NA</code> provides no real information about this character.</p><p>However, if you wish to see every property value, include <code>verbose=true</code> with your request to the <code>/v1/characters/-/{string}</code> or <code>/v1/characters/filter</code> endpoints.</p>
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>Basic</strong></strong>
        </summary>
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
            <dt><strong>ideoFrequency</strong><br /><span class="cjk-only">(CJK Characters ONLY)</span></dt>
            <dd>A rough frequency measurement for the character based on analysis of traditional Chinese USENET postings; characters with a kFrequency of 1 are the most common, those with a kFrequency of 2 are less common, and so on, through a kFrequency of 5.</dd>
            <dt><strong>ideoGradeLevel</strong><br /><span class="cjk-only">(CJK Characters ONLY)</span></dt>
            <dd>The primary grade in the Hong Kong school system by which a student is expected to know the character; this data is derived from <cite>朗文初級中文詞典, Hong Kong: Longman, 2001</cite>.</dd>
            <dt><strong>rsCountUnicode</strong><br /><span class="cjk-only">(CJK Characters ONLY)</span></dt>
            <dd>
                <p>The standard radical-stroke count for this character in the form “radical.additional strokes”. The radical is indicated by a number in the range (1..214) inclusive. An apostrophe (') after the radical indicates a simplified version of the given radical. The “additional strokes” value is the residual stroke-count, the count of all strokes remaining after eliminating all strokes associated with the radical.</p>
                <p>This field is also used for additional radical-stroke indices where either a character may be reasonably classified under more than one radical, or alternate stroke count algorithms may provide different stroke counts.</p>
                <p>The residual stroke count may be negative. This is because some characters (for example, U+225A9, U+29C0A) are constructed by removing strokes from a standard radical.</p>
            </dd>
            <dt><strong>rsCountKangxi</strong><br /><span class="cjk-only">(CJK Characters ONLY)</span></dt>
            <dd>The Kangxi radical-stroke count for this character consistent with the value of the character in the<cite>《康熙字典》Kangxi Dictionary</cite> in the form “radical.additional strokes”.</dd>
            <dt><strong>totalStrokes</strong><br /><span class="cjk-only">(CJK Characters ONLY)</span></dt>
            <dd>The total number of strokes in the character (including the radical). When there are two values, then the first is preferred for zh-Hans (CN) and the second is preferred for zh-Hant (TW). When there is only one value, it is appropriate for both</dd>
        </dl>
	</details>
	<br />
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>UTF-8</strong></strong>
        </summary>
        <div>UTF-8 is a method of encoding the Unicode character set where each code unit is equal to 8-bits. UTF-8 is backwards-compatible with ASCII and all codepoints in range 0-127 are represented as a single byte. Codepoints greater than 127 are represented as a sequence of 2-4 bytes.</div>
        <dl>
            <dt><strong>utf8</strong></dt>
            <dd>The UTF-8 encoded value for the character as a hex string.</dd>
            <dt><strong>utf8HexBytes</strong></dt>
            <dd>The byte sequence for the UTF-8 encoded value for the character. This property returns a list of strings, hex values (base-16) in range <code>00-FF</code>.</dd>
            <dt><strong>utf8DecBytes</strong></dt>
            <dd>The byte sequence for the UTF-8 encoded value for the character. This property returns a list of integers, decimal values (base-10) in range 0-127</dd>
        </dl>
	</details>
	<br />
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>UTF-16</strong></strong>
        </summary>
        <div>UTF-16 is a method of encoding the Unicode character set where each code unit is equal to 16-bits. All codepoints in the BMP (Plane 0) can be represented as a single 16-bit code unit (2 bytes). Code points in the supplementary planes (Planes 1-16) are represented as pairs of 16-bit code units (4 bytes).</div>
        <dl>
            <dt><strong>utf16</strong></dt>
            <dd>The UTF-16 encoded value for the character as a hex string.</dd>
            <dt><strong>utf16HexBytes</strong></dt>
            <dd>The byte sequence for the UTF-16 encoded value for the character. This property returns a list of strings, hex values (base-16) in range <code>0000-FFFF</code>.</dd>
            <dt><strong>utf16DecBytes</strong></dt>
            <dd>The byte sequence for the UTF-16 encoded value for the character. This property returns a list of integers, decimal values (base-10) in range 0-65,535</dd>
        </dl>
	</details>
	<br />
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>UTF-32</strong></strong>
        </summary>
        <div>UTF-32 is a method of encoding the Unicode character set where each code unit is equal to 32-bits. UTF-32 is the simplest Unicode encoding form. Each Unicode code point is represented directly by a single 32-bit code unit. Because of this, UTF-32 has a one-to-one relationship between encoded character and code unit; it is a fixed-width character encoding form.</div>
        <dl>
            <dt><strong>utf32</strong></dt>
            <dd>The UTF-32 encoded value for the character as a hex string.</dd>
            <dt><strong>utf32HexBytes</strong></dt>
            <dd>The byte sequence for the UTF-32 encoded value for the character. This property returns a list of strings, hex values (base-16) in range <code>00000000-0010FFFF</code>.</dd>
            <dt><strong>utf32DecBytes</strong></dt>
            <dd>The byte sequence for the UTF-32 encoded value for the character. This property returns a list of integers, decimal values (base-10) in range 0-1,114,111</dd>
        </dl>
	</details>
	<br />
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>Bidirectionality</strong></strong>
        </summary>
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
                    <li><code>U+200E	LEFT-TO-RIGHT MARK</code></li>
                    <li><code>U+200F	RIGHT-TO-LEFT MARK</code></li>
                    <li><code>U+202A	LEFT-TO-RIGHT EMBEDDING</code></li>
                    <li><code>U+202B	RIGHT-TO-LEFT EMBEDDING</code></li>
                    <li><code>U+202C	POP DIRECTIONAL FORMATTING</code></li>
                    <li><code>U+202D	LEFT-TO-RIGHT OVERRIDE</code></li>
                    <li><code>U+202E	RIGHT-TO-LEFT OVERRIDE</code></li>
                    <li><code>U+2066	LEFT-TO-RIGHT ISOLATE</code></li>
                    <li><code>U+2067	RIGHT-TO-LEFT ISOLATE</code></li>
                    <li><code>U+2068	FIRST STRONG ISOLATE</code></li>
                    <li><code>U+2069	POP DIRECTIONAL ISOLATE</code></li>
                    <li><code>U+061C	ARABIC LETTER MARK</code></li>
                </ul>
            </dd>
            <dt><strong>pairedBracketType</strong></dt>
            <dd>Type of a paired bracket, either opening, closing or none (the default value). This property is used in the implementation of parenthesis matching.</dd>
            <dt><strong>pairedBracketProperty</strong></dt>
            <dd>For an opening bracket, the code point of the matching closing bracket. For a closing bracket, the code point of the matching opening bracket.</dd>
        </dl>
	</details>
	<br />
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>Decomposition</strong></strong>
        </summary>
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
	</details>
	<br />
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>Quick Check</strong></strong>
        </summary>
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
	</details>
	<br />
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>Numeric</strong></strong>
        </summary>
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
                <p>If the character has the property value <code><strong>numericType=Decimal</code></strong>, then the <code>numericValue</code> of that digit is represented with an integer value (limited to the range 0..9).</p>
                <p>If the character has the property value <code><strong>numericType=Digit</code></strong>, then the <code>numericValue</code> of that digit is represented with an integer value (limited to the range 0..9). This covers digits that need special handling, such as the compatibility superscript digits. Starting with Unicode 6.3.0, no newly encoded numeric characters will be given <code><strong>numericValue=Digit</code></strong>, nor will existing characters with <code><strong>numericValue=Decimal</code></strong> be changed to <code><strong>numericValue=Digit</code></strong>. The distinction between those two types is not considered useful.</p>
                <p>If the character has the property value <code><strong>numericType=Numeric</code></strong>, then the <code>numericValue</code> of that character is represented with a positive or negative integer or rational number. This includes fractions such as, for example, "1/5" for ⅕ (<code>U+2155 <span>VULGAR FRACTION ONE FIFTH</span></code>).</p>
            </dd>
            <dt><strong>numericValueParsed</strong></dt>
            <dd><strong><i>This is NOT a property from the Unicode Standard.</i></strong> This is a floating point version of the <strong>numericValue</strong> property (which is a string value). For example, <code>0.2</code> for ⅕ (<code>U+2155 <span>VULGAR FRACTION ONE FIFTH</span></code>)
            </dd>
        </dl>
	</details>
	<br />
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>Joining</strong></strong>
        </summary>
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
	</details>
	<br />
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>Linebreak</strong></strong>
        </summary>
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
	</details>
	<br />
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>East Asian Width</strong></strong>
        </summary>
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
	</details>
	<br />
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>Case</strong></strong>
        </summary>
        <dl>
            <dt><strong>uppercase</strong></dt>
            <dd>Boolean value that indicates whether the character is an uppercase letter.</dd>
            <dt><strong>lowercase</strong></dt>
            <dd>Boolean value that indicates whether the character is a lowercase letter.</dd>
            <dt><strong>simpleUppercaseMapping</strong></dt>
            <dd>The uppercase form of the character, if expressible as a single character.</dd>
            <dt><strong>simpleLowercaseMapping</strong></dt>
            <dd>The lowercase form of the character, if expressible as a single character.</dd>
            <dt><strong>simpleTitlecaseMapping</strong></dt>
            <dd>The titlecase form of the character, if expressible as a single character.</dd>
            <dt><strong>simpleCaseFolding</strong></dt>
            <dd>The case-folded (lowercase) form of the character when applying simple folding, which does not change the length of a string (and may thus fail to fold some characters correctly).</dd>
        </dl>
	</details>
	<br />
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>Script</strong></strong>
        </summary>
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
	</details>
	<br />
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>Hangul</strong></strong>
        </summary>
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
	</details>
	<br />
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>Indic</strong></strong>
        </summary>
        <dl>
            <dt><strong>indicSyllabicCategory</strong></dt>
            <dd>Used to identify the type of syllable that a character belongs to, such as a vowel, consonant, or a combination of both.</dd>
            <dt><strong>indicMatraCategory</strong></dt>
            <dd>Used to identify the type of matra (vowel sign) associated with a character, such as a short or long vowel sign.</dd>
            <dt><strong>indicPositionalCategory</strong></dt>
            <dd>Used to identify the position of a character in a syllable, such as the initial, medial, or final position.</dd>
        </dl>
	</details>
	<br />
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>CJK Variants</strong></strong>
        </summary>
        <div class="prop-group-ref cjk-prop-group">Reference: <a href="https://www.unicode.org/reports/tr38/#N10211" rel="noopener noreferrer" target="_blank">Unicode Standard Annex #38, "Unicode Han Database (Unihan), Section 3.7 Variants"</a></div>
        <div>
            <p>Although Unicode encodes characters and not glyphs, the line between the two can sometimes be hard to draw, particularly in East Asia. There, thousands of years worth of writing have produced thousands of pairs which can be used more-or-less interchangeably.</p>
            <p>To deal with this situation, the Unicode Standard has adopted a three-dimensional model for determining the relationship between ideographs, and has formal rules for when two forms may be unified. Both are described in some detail in the Unicode Standard. Briefly, however, the three-dimensional model uses the x-axis to represent meaning, and the y-axis to represent abstract shape. The z-axis is used for stylistic variations.</p>
            <p>The <code>traditionalVariant</code> and <code>simplifiedVariant</code> fields are used in character-by-character conversions between simplified and traditional Chinese (SC and TC, respectively).</p>
            <p>Two variation fields, <code>semanticVariant</code> and <code>specializedSemanticVariant</code>, are used to mark cases where two characters have identical and overlapping meanings, respectively.</p>
            <p>The <code>spoofingVariant</code> field is used to denote a special class of variant, a spoofing variant. Spoofing variants are potentially used in bad faith to direct users to unexpected URLs, evade email filters, or otherwise deceive end-users.</p>
            <p>For more information on CJK variants, please see <a href="https://www.unicode.org/reports/tr38/#N10211" rel="noopener noreferrer" target="_blank">UAX #38, Section 3.7</a>.</p>
        </div>
        <dl>
            <dt><strong>traditionalVariant</strong></dt>
            <dd>The Unicode value(s) for the traditional Chinese variant(s) for this character.</dd>
            <dt><strong>simplifiedVariant</strong></dt>
            <dd>The Unicode value(s) for the simplified Chinese variant(s) for this character.</dd>
            <dt><strong>zVariant</strong></dt>
            <dd>The z-variants for the character, if any. Z-variants are instances where the same abstract shape has been encoded multiple times, either in error or because of source separation. Z-variant pairs also have identical semantics.</dd>
            <dt><strong>compatibilityVariant</strong></dt>
            <dd>The canonical Decomposition_Mapping value for the ideograph</dd>
            <dt><strong>semanticVariant</strong></dt>
            <dd>The Unicode value for a semantic variant for this character. A semantic variant is an x- or y-variant with similar or identical meaning which can generally be used in place of the indicated character.</dd>
            <dt><strong>specializedSemanticVariant</strong></dt>
            <dd>The Unicode value for a specialized semantic variant for this character. The syntax is the same as for the kSemanticVariant field. A specialized semantic variant is an x- or y-variant with similar or identical meaning only in certain contexts.</dd>
            <dt><strong>spoofingVariant</strong></dt>
            <dd>The spoofing variants for the character, if any. Spoofing variants include character pairs which look similar, particularly at small point sizes, which are not already z-variants or compatibility variants.</dd>
        </dl>
	</details>
	<br />
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>CJK Numeric</strong></strong>
        </summary>
        <div class="prop-group-ref cjk-prop-group">Reference: <a href="https://www.unicode.org/reports/tr38/#N1024D" rel="noopener noreferrer" target="_blank">Unicode Standard Annex #38, "Unicode Han Database (Unihan), Section 3.8 Numeric Values"</a></div>
        <div>
            <p>There are three fields, <code>accountingNumeric</code>, <code>otherNumeric</code>, and <code>primaryNumeric</code> to indicate the numerical values an ideograph may have. Traditionally, ideographs were used both for numbers and words, and so many ideographs have (or can have) numeric values. The various kinds of numeric values are specified by these three fields.</p>
            <p>The three numeric-value fields should have no overlap; that is, characters with a <code>accountingNumeric</code> value should not have a <code>otherNumeric</code> or </code>primaryNumeric</code> value as well.</p>
        </div>
        <dl>
            <dt><strong>accountingNumeric</strong></dt>
            <dd>
                <p>The value of the character when used as an accounting numeral to prevent fraud. A numeral such as 十 (ten) is easily transformed into 千 (thousand) by adding a single stroke, so monetary documents often use an accounting form of the numeral, such as 拾 (ten), instead of the more common—and simpler—form.</p>
                <p>Characters with this property will have a single, well-defined value, which a native reader can reasonably be expected to understand.</p>
            </dd>
            <dt><strong>primaryNumeric</strong></dt>
            <dd>
                <p>The value of the character when used as a numeral. Characters which have this property have numeric values that are common, and always convey the same numeric value.</p>
                <p>For example, 千 always means “thousand.” A native reader is expected to understand the numeric value for these characters.</p>
            </dd>
            <dt><strong>otherNumeric</strong></dt>
            <dd>
                <p>One or more values of the character when used as a numeral. Characters with this property are rarely used for writing numbers, or have non-standard or multiple values depending on the region.</p>
                <p>For example, 㠪 is a rare character whose meaning, “five,” would not be recognized by most native readers. An English-language equivalent is “gross,” whose numeric value, “one hundred forty-four,” is not universally understood by native readers.</p>
            </dd>
        </dl>
	</details>
	<br />
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>CJK Readings</strong></strong>
        </summary>
        <div class="prop-group-ref cjk-prop-group">Reference: <a href="https://www.unicode.org/reports/tr38/#N1019C" rel="noopener noreferrer" target="_blank">Unicode Standard Annex #38, "Unicode Han Database (Unihan), Section 3.4 Readings"</a></div>
        <div>
            <p>The properties in this group include the pronunciations for a given character in Mandarin, Cantonese, Japanese, Sino-Japanese, Korean, and Vietnamese.</p>
            <p>Any attempt at providing a reading or set of readings for a character is bound to be fraught with difficulty, because the readings will vary over time and from place to place, even within a language. Mandarin is the official language of both the PRC and Taiwan (with some differences between the two) and is the primary language over much of northern and central China, with vast differences from place to place. Even Cantonese, the modern language covered by the Unihan database with the least geographical range, is spoken throughout Guangdong Province and in much of neighboring Guangxi Zhuang Autonomous Region, and covers four large urban centers (Guangzhou, Shenzhen, Macao, and Hong Kong). There are therefore distinct regional variations in pronunciation and vocabulary.</p>
            <p>Indeed, even the same speaker will pronounce the same word differently depending on the speaker or even the social context. This is particularly true for languages such as Cantonese, where there has been comparatively little government effort to standardize the language.</p>
            <p>Add to this the fact that in none of these languages—the various forms of Chinese, Japanese, Korean, Vietnamese—is the syllable the fundamental unit of the language. As in the West, it’s the word, and the pronunciation of a character is tied to the word of which it is a part. In Chinese (followed by Vietnamese and Korean), the rule is one ideograph/one syllable, with most words written using multiple ideographs. In most cases, an ideograph has only one reading (or only one important reading), but there are numerous exceptions.</p>
            <p>In Japanese, the situation is enormously more complex. Japanese has two pronunciation systems, one derived from Chinese (the on pronunciation, or Sino-Japanese), and the other from Japanese (the kun pronunciation).</p>
            <p>The on readings derive from Chinese loan-words. They depend on factors such as when (and from which part of China) the loan-word was borrowed, and changes to Japanese since then. On readings can therefore have little obvious relationship to modern Chinese readings, and the same Chinese reading for a given kanji can be reflected in multiple on readings in Japanese. Contrary to Chinese practice, on readings may be polysyllabic.</p>
            <p>Kun readings, on the other hand, derive from native Japanese words for which either existing kanji were adopted or new kanji coined.</p>
            <p>The net result is that multiple readings are the rule for Japanese kanji. These multiple readings may bear no relationship to one another and are highly context-sensitive. Even a native Japanese reader may not know the correct pronunciation of a proper noun if it is written only in kanji.</p>
        </div>
        <dl>
            <dt><strong>mandarin</strong></dt>
            <dd>The most customary pīnyīn reading for this character. When there are two values, then the first is preferred for zh-Hans (CN) and the second is preferred for zh-Hant (TW). When there is only one value, it is appropriate for both.</dd>
            <dt><strong>cantonese</strong></dt>
            <dd>The most customary jyutping (Cantonese) reading for this character.</dd>
            <dt><strong>japaneseKun</strong></dt>
            <dd>The Japanese pronunciation(s) of this character in the Hepburn romanization.</dd>
            <dt><strong>japaneseOn</strong></dt>
            <dd>The Sino-Japanese pronunciation(s) of this character.</dd>
            <dt><strong>hangul</strong></dt>
            <dd>The modern Korean pronunciation(s) for this character in Hangul</dd>
            <dt><strong>vietnamese</strong></dt>
            <dd>The character's pronunciation(s) in Quốc ngữ.</dd>
        </dl>
	</details>
	<br />
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>Function and Graphic</strong></strong>
        </summary>
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
	</details>
	<br />
	<details class='property-group'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong>Emoji</strong></strong>
        </summary>
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
	</details>
</div>
<h3 id="unicode-codepoints">Unicode Codepoints</h3>
<div>
	<details open class='api-endpoints'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><h4 id="codepoint-api-endpoints">API Endpoints</h4></strong>
        </summary>
            <dl>
                <dt><strong>GET</strong> <code>/v1/codepoints/{hex}</code></dt>
                <dd>Retrieve details of a single character</dd>
            </dl>
	</details>
	<p>The <code>UnicodeCodepoint</code> resource is not an object like the other resources, it is simply a hexadecimal value that refers to a single character in the Unicode codespace. </p><p>This endpoint performs nearly the same function as the <code>/v1/characters/-/{string}</code> endpoint. However, sending a request for a character to the <code>/v1/characters/-/{string}</code> endpoint requires you to provide either the character itself or the URI encoded string representation of the character.</p><p>Since there are plenty of scenarios where it may be easier to supply the assigned codepoint for a character rather than the rendered glyph or URI-encoded value, the <code>/v1/codepoints/{hex}</code> endpoint allows you to request the same sets of character property groups as the <code>/v1/characters/-/{string}</code> endpoint.</p><p>The only difference between the two endpoints is requests to the <code>/v1/characters/-/{string}</code> endpoint can retrieve data for one or more characters, while requests to the <code>/v1/codepoints/{hex}</code> endpoint can only be used to retrieve details of a single character.</p>
</div>
<h3 id="unicode-blocks">Unicode Blocks</h3>
<div>
	<details open class='api-endpoints'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><h4 id="block-api-endpoints">API Endpoints</h4></strong>
        </summary>
        <dl>
            <dt><strong>GET</strong> <code>/v1/blocks/{name}</code></dt>
            <dd>Retrieve one or more Block(s)</dd>
            <dt><strong>GET</strong> <code>/v1/blocks</code></dt>
            <dd>List Blocks</dd>
            <dt><strong>GET</strong> <code>/v1/blocks/search</code></dt>
            <dd>Search Blocks</dd>
        </dl>
	</details>
	<h4 id="the-unicodeblock-object">The <code>UnicodeBlock</code> Object</h4>
    <p>The <code>UnicodeBlock</code> object represents a grouping of characters within the Unicode encoding space. Each block is generally, but not always, meant to supply glyphs used by one or more specific languages, or in some general application area such as mathematics, surveying, decorative typesetting, social forums, etc.</p><p>Each block is a uniquely named, continuous, non-overlapping range of code points, containing a multiple of 16 code points (additionally, the starting codepoint for each block is a multiple of 16). A block may contain unassigned code points, which are reserved.</p><p>The <code>UnicodeBlock</code> object exposes a small set of properties such as the official name of the block, the range of code points assigned to the block and the total number of defined characters within the block:</p>
	<details>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong><code>UnicodeBlock</code> Properties</strong></strong>
        </summary>
        <dl>
            <dt><strong>id</strong></dt>
            <dd><strong><i>This is NOT a property from the Unicode Standard.</i></strong> This is an integer value used to navigate within a paginated list of <code>UnicodeBlock</code> objects. The first block (<code>U+0000..U+007F <span>BASIC LATIN</span></code>) has <code>id=1</code> and each block is numbered sequentially in order of starting codepoint.</dd>
            <dt><strong>name</strong></dt>
            <dd>Unicode blocks are identified by unique names, which use only ASCII characters and are usually descriptive of the nature of the symbols (in English), such as "Tibetan" or "Supplemental Arrows-A".</dd>
            <dt><strong>plane</strong></dt>
            <dd>A string value equal to the abbreviated name of the Unicode Plane containing the block (e.g., "BMP" for Basic Multilingual Plane).</dd>
            <dt><strong>start</strong></dt>
            <dd>A string value equal to the first codepoint allocated to the block, expressed in <code>U+hhhhhh</code> format.</dd>
            <dt><strong>finish</strong></dt>
            <dd>A string value equal to the last codepoint allocated to the block, expressed in <code>U+hhhhhh</code> format.</dd>
            <dt><strong>total_allocated</strong></dt>
            <dd>An integer value equal to the total number of characters (defined or reserved) contained in the block.</dd>
            <dt><strong>total_defined</strong></dt>
            <dd>An integer value equal to the total number of characters with defined names, glyphs, etc in the block.</dd>
        </dl>
	</details>
</div>
<h3 id="unicode-planes">Unicode Planes</h3>
<div>
	<details open class='api-endpoints'>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><h4 id="plane-api-endpoints">API Endpoints</h4></strong>
        </summary>
        <dl>
            <dt><strong>GET</strong> <code>/v1/planes/{number}</code></dt>
            <dd>Retrieve one or more Plane(s)</dd>
            <dt><strong>GET</strong> <code>/v1/planes</code></dt>
            <dd>List Planes</dd>
        </dl>
	</details>
	<h4 id="the-unicodeplane-object">The <code>UnicodePlane</code> Object</h4>
    <p>The <code>UnicodePlane</code> object represents a continuous group of <strong>65,536</strong> (2<sup>16</sup>) code points. There are 17 planes, identified by the numbers 0 to 16. The first two positions of a character's codepoint value (U+<strong>hh</strong>hhhh) correspond to the plane number in hex format (possible values <code>0x00</code>–<code>0x10</code>).</p><p>Plane 0 is the <strong>Basic Multilingual Plane (BMP)</strong>, which contains most commonly used characters. The higher planes 1 through 16 are called "supplementary planes". The last code point in plane 16 is the last code point in Unicode, U+10FFFF.</p>
	<details>
        <summary style="list-style: none; align-items: center">
            <div style="display: flex; gap: 0.75rem; align-items: center; justify-content: space-between; flex: 0; margin: 0 0 0 0.25rem; padding: 0.25rem 1rem 0.25rem 0">
                <div style="height: 16px; transition: transform 0.3s ease-in">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                        <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                    </svg>
                </div>
            </div>
            <strong style="flex: 1"><strong><code>UnicodePlane</code> Properties</strong></strong>
        </summary>
        <dl>
            <dt><strong>number</strong></dt>
            <dd>The official number that identifies the range of codepoints within a plane. The first two positions of a character's codepoint value (U+<strong>hh</strong>hhhh) correspond to the plane number in hex format (possible values <code>0x00</code>...<code>0x10</code>). This is a decimal value, however, with possible values <strong>0...16</strong>.</dd>
            <dt><strong>name</strong></dt>
            <dd>
                <p>The official name of a plane, according to the Unicode Standard. As of version 15.0.0, seven of the total 17 planes have official names (the official abbreviation for each plane if also given in parentheses):</p>
				<ol>
					<li style="list-style-type: '0.'"><span>Basic Multilingual Plane (BMP)</span></li>
					<li style="list-style-type: '1.'"><span>Supplementary Multilingual Plane (SMP)</span></li>
					<li style="list-style-type: '2.'"><span>Supplementary Ideographic Plane (SIP)</span></li>
					<li style="list-style-type: '3.'"><span>Tertiary Ideographic Plane (TIP)</span></li>
					<li style="list-style-type: '14.'"><span>Supplementary Special-purpose Plane (SSP)</span></li>
					<li style="list-style-type: '15.'"><span>Supplementary Private Use Area-A (SPUA-A)</span></li>
					<li style="list-style-type: '16.'"><span>Supplementary Private Use Area-B (SPUA-B)</span></li>
				</ol>
                <p>The codepoints within Planes 4-13 (<code>U+40000</code>...<code>U+​DFFFF</code>) are unassigned, and these planes currently have no official name/abbreviation.</p>
            </dd>
            <dt><strong>abbreviation</strong></dt>
            <dd>An acronym that identifies the plane, the list in the previous definition contains the abbreviation for each plane along with the official name.</dd>
            <dt><strong>start</strong></dt>
            <dd>A string value equal to the first codepoint allocated to the plane, expressed in <code>U+hhhhhh</code> format.</dd>
            <dt><strong>finish</strong></dt>
            <dd>A string value equal to the last codepoint allocated to the plane, expressed in <code>U+hhhhhh</code> format.</dd>
            <dt><strong>total_allocated</strong></dt>
            <dd>An integer value equal to the total number of characters (defined or reserved) contained in the plane (always 2<sup>16</sup>).</dd>
            <dt><strong>total_defined</strong></dt>
            <dd>An integer value equal to the total number of characters with defined names, glyphs, etc in the plane.</dd>
        </dl>
	</details>
</div>
