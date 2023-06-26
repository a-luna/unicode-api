import json
import os
from typing import Any, Dict, Optional

from fastapi.encoders import jsonable_encoder
from fastapi.openapi.docs import swagger_ui_default_parameters
from starlette.responses import HTMLResponse

from app.docs.api_docs.content.block import BLOCK_ENDPOINTS, UNICODE_BLOCK_OBJECT_INTRO, UNICODE_BLOCK_OBJECT_PROPERTIES
from app.docs.api_docs.content.character import (
    CHARACTER_ENDPOINTS,
    PROP_GROUP_BASIC,
    PROP_GROUP_BIDIRECTIONALITY,
    PROP_GROUP_CASE,
    PROP_GROUP_DECOMPOSITION,
    PROP_GROUP_EAW,
    PROP_GROUP_EMOJI,
    PROP_GROUP_F_AND_G,
    PROP_GROUP_HANGUL,
    PROP_GROUP_INDIC,
    PROP_GROUP_JOINING,
    PROP_GROUP_LINEBREAK,
    PROP_GROUP_MINIMUM,
    PROP_GROUP_NUMERIC,
    PROP_GROUP_QUICK_CHECK,
    PROP_GROUP_SCRIPT,
    PROP_GROUP_UTF8,
    PROP_GROUP_UTF16,
    PROP_GROUP_UTF32,
    UNICODE_CHARACTER_PROP_GROUPS_CONTINUED_1,
    UNICODE_CHARACTER_PROP_GROUPS_CONTINUED_2,
    UNICODE_CHARACTER_PROP_GROUPS_INTRO,
    UNICODE_CHATACTER_OBJECT_INTRO,
    VERBOSITY,
)
from app.docs.api_docs.content.intro import INTRODUCTION, LOOSE_MATCHING, PAGINATION, PROJECT_LINKS_SWAGGER_HTML, SEARCH
from app.docs.api_docs.content.plane import PLANE_ENDPOINTS, UNICODE_PLANE_OBJECT_INTRO, UNICODE_PLANE_OBJECT_PROPERTIES


def create_details_element_for_swagger_ui(
    title: str, content: str, open: bool | None = False, id: str | None = None
) -> str:
    open_tag = "<details open" if open else "<details"
    open_tag += f" id={id!r}>" if id else ">"
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


UNICODE_CHARACTERS_DOCS = f"""
    <div>
        {create_details_element_for_swagger_ui("API Endpoints", CHARACTER_ENDPOINTS, True)}<h4>The <code>UnicodeCharacter</code> Object</h4>
        {UNICODE_CHATACTER_OBJECT_INTRO}
        <h4 id="unicodecharacter-property-groups"><code>UnicodeCharacter</code> Property Groups</h4>
{UNICODE_CHARACTER_PROP_GROUPS_INTRO}
{create_details_element_for_swagger_ui('<h6 id="minimum">Property Group: Minimum</h6>', PROP_GROUP_MINIMUM, True)}
{UNICODE_CHARACTER_PROP_GROUPS_CONTINUED_1}
{UNICODE_CHARACTER_PROP_GROUPS_CONTINUED_2}
        <h4 id="verbosity">Verbosity</h4>
{VERBOSITY}
{create_details_element_for_swagger_ui('<h6 id="basic">Property Group: Basic</h6>', PROP_GROUP_BASIC)}
{create_details_element_for_swagger_ui('<h6 id="utf8">Property Group: UTF-8</h6>', PROP_GROUP_UTF8)}
{create_details_element_for_swagger_ui('<h6 id="utf16">Property Group: UTF-16</h6>', PROP_GROUP_UTF16)}
{create_details_element_for_swagger_ui('<h6 id="utf32">Property Group: UTF-32</h6>', PROP_GROUP_UTF32)}
{create_details_element_for_swagger_ui('<h6 id="bidirectionality">Property Group: Bidirectionality</h6>', PROP_GROUP_BIDIRECTIONALITY)}
{create_details_element_for_swagger_ui('<h6 id="decomposition">Property Group: Decomposition</h6>', PROP_GROUP_DECOMPOSITION)}
{create_details_element_for_swagger_ui('<h6 id="quick-check">Property Group: Quick Check</h6>', PROP_GROUP_QUICK_CHECK)}
{create_details_element_for_swagger_ui('<h6 id="numeric">Property Group: Numeric</h6>', PROP_GROUP_NUMERIC)}
{create_details_element_for_swagger_ui('<h6 id="joining">Property Group: Joining</h6>', PROP_GROUP_JOINING)}
{create_details_element_for_swagger_ui('<h6 id="linebreak">Property Group: Linebreak</h6>', PROP_GROUP_LINEBREAK)}
{create_details_element_for_swagger_ui('<h6 id="east-asian-width">Property Group: East Asian Width</h6>', PROP_GROUP_EAW)}
{create_details_element_for_swagger_ui('<h6 id="case">Property Group: Case</h6>', PROP_GROUP_CASE)}
{create_details_element_for_swagger_ui('<h6 id="script">Property Group: Script</h6>', PROP_GROUP_SCRIPT)}
{create_details_element_for_swagger_ui('<h6 id="hangul">Property Group: Hangul</h6>', PROP_GROUP_HANGUL)}
{create_details_element_for_swagger_ui('<h6 id="indic">Property Group: Indic</h6>', PROP_GROUP_INDIC)}
{create_details_element_for_swagger_ui('<h6 id="function-and-graphic">Property Group: Function and Graphic</h6>', PROP_GROUP_F_AND_G)}
{create_details_element_for_swagger_ui('<h6 id="emoji">Property Group: Emoji</h6>', PROP_GROUP_EMOJI)}</div>
"""

UNICODE_BLOCKS_DOCS = f"""
    <div>
        {create_details_element_for_swagger_ui("API Endpoints", BLOCK_ENDPOINTS, True)}<h4 id="the-unicodeblock-object">The <code>UnicodeBlock</code> Object</h4>
        {UNICODE_BLOCK_OBJECT_INTRO}
        {create_details_element_for_swagger_ui("<strong><code>UnicodeBlock</code> Properties</strong>", UNICODE_BLOCK_OBJECT_PROPERTIES, True)}</div>
"""

UNICODE_PLANES_DOCS = f"""
    <div>
        {create_details_element_for_swagger_ui("API Endpoints", PLANE_ENDPOINTS, True)}<h4 id="the-unicodeplane-object">The <code>UnicodePlane</code> Object</h4>
        {UNICODE_PLANE_OBJECT_INTRO}
        {create_details_element_for_swagger_ui("<strong><code>UnicodePlane</code> Properties</strong>", UNICODE_PLANE_OBJECT_PROPERTIES, True)}</div>
"""


def get_api_docs_for_swagger_ui():
    return (
        INTRODUCTION
        + create_details_element_for_swagger_ui(
            '<h3 id="project-resources">Project Resources/Contact Info</h3>', PROJECT_LINKS_SWAGGER_HTML
        )
        + create_details_element_for_swagger_ui('<h3 id="pagination">Pagination</h3>', PAGINATION)
        + create_details_element_for_swagger_ui('<h3 id="search">Search</h3>', SEARCH)
        + create_details_element_for_swagger_ui('<h3 id="loose-matching">Loose Matching</h3>', LOOSE_MATCHING)
        + "<h3>Core Resources</h3>\n"
        + create_details_element_for_swagger_ui(
            '<h4 id="unicode-characters">Unicode Characters</h4>', UNICODE_CHARACTERS_DOCS
        )
        + create_details_element_for_swagger_ui('<h4 id="unicode-blocks">Unicode Blocks</h4>', UNICODE_BLOCKS_DOCS)
        + create_details_element_for_swagger_ui('<h4 id="unicode-planes">Unicode Planes</h4>', UNICODE_PLANES_DOCS)
    )


def get_swagger_ui_html(
    *,
    openapi_url: str,
    title: str,
    swagger_js_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js",
    swagger_css_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css",
    swagger_favicon_url: str = "https://fastapi.tiangolo.com/img/favicon.png",
    oauth2_redirect_url: Optional[str] = None,
    init_oauth: Optional[Dict[str, Any]] = None,
    swagger_ui_parameters: Optional[Dict[str, Any]] = None,
    custom_js_url: Optional[str] = None,
) -> HTMLResponse:
    current_swagger_ui_parameters = swagger_ui_default_parameters.copy()
    if swagger_ui_parameters:
        current_swagger_ui_parameters.update(swagger_ui_parameters)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href={swagger_css_url!r}>
    <link rel="shortcut icon" href={swagger_favicon_url!r}>
    """

    if os.environ.get("ENV", "DEV") == "PROD":
        html += """
        <script async src="https://aluna-umami.netlify.app/script.js" data-website-id="13067599-d69c-4a00-a745-207308bd4d18"></script>
        """

    html += f"""
    <title>{title}</title>
    </head>
    <body>
    <svg xmlns='http://www.w3.org/2000/svg' width='56' height='100'>
      <rect width='56' height='100' fill='#808080cc'/>
      <path d='M28 66L0 50L0 16L28 0L56 16L56 50L28 66L28 100' fill='none' stroke='#2875bd' stroke-width='1'/>
      <path d='M28 0L28 34L0 50L0 84L28 100L56 84L56 50L28 34' fill='none' stroke='#256db1' stroke-width='1'/>
    </svg>
    <div id="swagger-ui"></div>
    <script src={swagger_js_url!r}></script>
    <script defer src={custom_js_url!r}></script>
    <script>
    const ui = SwaggerUIBundle({{
        url: {openapi_url!r},
    """

    for key, value in current_swagger_ui_parameters.items():
        html += f"{json.dumps(key)}: {json.dumps(jsonable_encoder(value))},\n"

    if oauth2_redirect_url:
        html += f"oauth2RedirectUrl: window.location.origin + {oauth2_redirect_url!r},"

    html += """
    presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
    })"""

    if init_oauth:
        html += f"""
        ui.initOAuth({json.dumps(jsonable_encoder(init_oauth))})
        """

    html += """
    </script>
    </body>
    </html>
    """
    return HTMLResponse(html)
