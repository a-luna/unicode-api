# flake8: noqa
from app.core.config import get_settings
from app.core.util import get_unicode_version_release_date


INTRODUCTION = f"""
<p>This API provides access to detailed information for all characters, blocks and planes in <a href="https://www.unicode.org/versions/Unicode{get_settings().UNICODE_VERSION}/" rel="noopener noreferrer" target="_blank">version {get_settings().UNICODE_VERSION} of the Unicode Standard</a> (released {get_unicode_version_release_date(get_settings().UNICODE_VERSION)}). In an attempt to adhere to the tenants of <a href="http://en.wikipedia.org/wiki/Representational_State_Transfer" rel="noopener noreferrer" target="_blank">REST</a>, the API is organized around the following principles:</p>
<ul class="api-principles">
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
            <li><a href="mailto:contact@aaronluna.dev">Send Email</a></li>
        </ul>
    </ul>
"""

PROJECT_LINKS_README = """
    <ul>
        <li><a href="https://unicode-api.aaronluna.dev/" rel="noopener noreferrer" target="_blank">Interactive API Documents (Swagger UI)</a></li>
        <li>Created by Aaron Luna</li>
        <ul>
            <li><a href="https://aaronluna.dev" rel="noopener noreferrer" target="_blank">Personal Website</a></li>
            <li><a href="mailto:contact@aaronluna.dev">Send Email</a></li>
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
        <p><span class="alert">⚠️</span> <strong><i>IMPORTANT: Only one of <code>starting_after</code> or <code>ending_before</code> may be used in a request, sending a value for both parameters will produce a response with status <code>400 Bad Request</code></i></strong>.</p>
    </div>
"""

SEARCH = """
    <div>
        <p>The top-level API resources for <strong>Unicode Characters</strong> and <strong>Unicode Blocks</strong> also have support for retrieval via "search" API methods. These API methods (<code>/v1/characters/search</code> and <code>/v1/blocks/search</code>) share an identical structure, taking the same four parameters: <code>name</code>, <code>min_score</code>, <code>per_page</code>, and <code>page</code>.</p>
        <p>The <code>name</code> parameter is the search term and is used to retrieve a character/block using the official name defined in the UCD. Since a <a href="https://en.wikipedia.org/wiki/Approximate_string_matching" rel="noopener noreferrer" target="_blank">fuzzy search algorithm</a> is used for this process, the value of <code>name</code> does not need to be an exact match with a character/block name.</p>
        <p>The response will contain a <code>results</code> parameter that represents the characters/blocks that matched your query. Each object in this list has a <code>score</code> property which is a number ranging from <strong>0-100</strong> that describes how similar the character/block name is to the <code>name</code> value provided by the user (A value of 100 means that the <code>name</code> provided by the user is an exact match with a character/block name). The list contains all results where <code>score</code> &gt;= <code>min_score</code>, sorted by <code>score</code> (the first element in the list being the <i><strong>most similar</strong></i>).</p>
        <p>The default value for <code>min_score</code> is <strong>80</strong>, however if your request is returning zero results, you can lower this value to potentially surface lower-quality results. Keep in mind, the lowest value for <code>min_score</code> that is permitted is <strong>70</strong>, since the relevence of results quickly drops off around a score of <strong>72</strong>, often producing hundreds of results with no relevance to the search term.</p>
        <p>The <code>per_page</code> parameter controls how many results are included in a single response. The response will include a <code>hasMore</code> parameter that indicates whether there are more search results beyond the current page, as well as <code>currentPage</code> and <code>totalResults</code> parameters. If <code>hasMore=true</code>, the response will also contain a <code>nextPage</code> parameter.</p>
        <p>For example, if you receive a response to a search request with <code>hasMore=true</code> and <code>nextPage=2</code>, you can update your request to include <code>page=2</code> to fetch the next page of results. If the next response includes <code>hasMore=true</code> and <code>nextPage=3</code>, update your request to include <code>page=3</code>, etc. Rinse and repeat until you receive a response with <code>hasMore=false</code>, indicating that you have received the final set of search results.</p>
    </div>
"""

LOOSE_MATCHING = """
    <div>
        <p>Unicode specifies a set of rules to be used when comparing symbolic values, such as block names, known as <strong>loose matching rule</strong> <a href="https://www.unicode.org/reports/tr44/#UAX44-LM3" rel="noopener noreferrer" target="_blank">UAX44-LM3</a>. The algotithm for UAX44-LM3 is simple: <strong><i>Ignore case, whitespace, underscore ('_'), hyphens, and any initial prefix string "is".</i></strong></p>
        <p>This rule applies to many of the parameters that are included with API requests, which avoids returning a 400 response when a parameter name, for example, is sent as 'script', but the expected value is 'Script'. Under UAX44-LM3, both values are equivalent.</p>
        <p>For another example, under this rule the block name "Supplemental Arrows-A" is equivalent to "supplemental_arrows__a" and "SUPPLEMENTALARROWSA" since all three of these strings would be reduced to "supplementalarrowsa" after applying UAX44-LM3. For any query or path parameter that expects the name of a Unicode block, any of these three values could be provided and would be understood to refer to block <code>U+27F0..U+27FF <span>SUPPLEMENTAL ARROWS-A</span></code>.</p>
        <p>Whenever the loose-matching rule applies to a parameter, it will be called out in the docuentation for each individual API endpoint below.</p>
    </div>
"""
