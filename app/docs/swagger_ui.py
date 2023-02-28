import json
import os
from typing import Any, Dict, Optional

from fastapi.encoders import jsonable_encoder
from fastapi.openapi.docs import swagger_ui_default_parameters
from starlette.responses import HTMLResponse

from app.docs.content import *


def create_details_element_for_swagger_ui(title: str, content: str, open: bool | None = False) -> str:
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


UNICODE_CHARACTERS_DOCS = f"""
    <div>
        {create_details_element_for_swagger_ui("Endpoints", CHARACTER_ENDPOINTS, True)}<h4>The <code>UnicodeCharacter</code> Object</h4>
        {UNICODE_CHATACTER_OBJECT_INTRO}
        <h4><code>UnicodeCharacter</code> Property Groups</h4>
{UNICODE_CHARACTER_PROP_GROUPS_INTRO}
{create_details_element_for_swagger_ui("<strong>Property Group: Minimum</strong>", PROP_GROUP_MINIMUM, True)}
{UNICODE_CHARACTER_PROP_GROUPS_CONTINUED_1}
{UNICODE_CHARACTER_PROP_GROUPS_CONTINUED_2}
{create_details_element_for_swagger_ui("<strong>Property Group: Basic</strong> (<code>show_props=Basic</code>)", PROP_GROUP_BASIC)}
{create_details_element_for_swagger_ui("<strong>Property Group: UTF-8</strong> (<code>show_props=UTF8</code>)", PROP_GROUP_UTF8)}
{create_details_element_for_swagger_ui("<strong>Property Group: UTF-16</strong> (<code>show_props=UTF16</code>)", PROP_GROUP_UTF16)}
{create_details_element_for_swagger_ui("<strong>Property Group: UTF-32</strong> (<code>show_props=UTF32</code>)", PROP_GROUP_UTF32)}
{create_details_element_for_swagger_ui("<strong>Property Group: Bidirectionality</strong> (<code>show_props=Bidirectionality</code>)", PROP_GROUP_BIDIRECTIONALITY)}
{create_details_element_for_swagger_ui("<strong>Property Group: Decomposition</strong> (<code>show_props=Decomposition</code>)", PROP_GROUP_DECOMPOSITION)}
{create_details_element_for_swagger_ui("<strong>Property Group: Quick Check</strong> (<code>show_props=Quick_Check</code>)", PROP_GROUP_QUICK_CHECK)}
{create_details_element_for_swagger_ui("<strong>Property Group: Numeric</strong> (<code>show_props=Numeric</code>)", PROP_GROUP_NUMERIC)}
{create_details_element_for_swagger_ui("<strong>Property Group: Joining</strong> (<code>show_props=Joining</code>)", PROP_GROUP_JOINING)}
{create_details_element_for_swagger_ui("<strong>Property Group: Linebreak</strong> (<code>show_props=Linebreak</code>)", PROP_GROUP_LINEBREAK)}
{create_details_element_for_swagger_ui("<strong>Property Group: East Asian Width</strong> (<code>show_props=East_Asian_Width</code>)", PROP_GROUP_EAW)}
{create_details_element_for_swagger_ui("<strong>Property Group: Case</strong> (<code>show_props=Case</code>)", PROP_GROUP_CASE)}
{create_details_element_for_swagger_ui("<strong>Property Group: Script</strong> (<code>show_props=Script</code>)", PROP_GROUP_SCRIPT)}
{create_details_element_for_swagger_ui("<strong>Property Group: Hangul</strong> (<code>show_props=Hangul</code>)", PROP_GROUP_HANGUL)}
{create_details_element_for_swagger_ui("<strong>Property Group: Indic</strong> (<code>show_props=Indic</code>)", PROP_GROUP_INDIC)}
{create_details_element_for_swagger_ui("<strong>Property Group: Function and Graphic</strong> (<code>show_props=Function_and_Graphic</code>)", PROP_GROUP_F_AND_G)}
{create_details_element_for_swagger_ui("<strong>Property Group: Emoji</strong> (<code>show_props=Emoji</code>)", PROP_GROUP_EMOJI)}</div>
"""

UNICODE_BLOCKS_DOCS = f"""
    <div>
        {create_details_element_for_swagger_ui("Endpoints", BLOCK_ENDPOINTS, True)}<h4>The <code>UnicodeBlock</code> Object</h4>
        {UNICODE_BLOCK_OBJECT_INTRO}
        {create_details_element_for_swagger_ui("<strong><code>UnicodeBlock</code> Properties</strong>", UNICODE_BLOCK_OBJECT_PROPERTIES, True)}</div>
"""

UNICODE_PLANES_DOCS = f"""
    <div>
        {create_details_element_for_swagger_ui("Endpoints", PLANE_ENDPOINTS, True)}<h4>The <code>UnicodePlane</code> Object</h4>
        {UNICODE_PLANE_OBJECT_INTRO}
        {create_details_element_for_swagger_ui("<strong><code>UnicodePlane</code> Properties</strong>", UNICODE_PLANE_OBJECT_PROPERTIES, True)}</div>
"""


def get_api_docs_for_swagger_ui():
    return (
        INTRODUCTION
        + create_details_element_for_swagger_ui("Project Resources/Contact Info", PROJECT_LINKS_SWAGGER_HTML)
        + create_details_element_for_swagger_ui("Pagination", PAGINATION)
        + create_details_element_for_swagger_ui("Search", SEARCH)
        + "<h3>Core Resources</h3>\n"
        + create_details_element_for_swagger_ui("Unicode Characters", UNICODE_CHARACTERS_DOCS)
        + create_details_element_for_swagger_ui("Unicode Blocks", UNICODE_BLOCKS_DOCS)
        + create_details_element_for_swagger_ui("Unicode Planes", UNICODE_PLANES_DOCS)
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
    <link type="text/css" rel="stylesheet" href="{swagger_css_url}">
    <link rel="shortcut icon" href="{swagger_favicon_url}">
    """

    if os.environ.get("ENV", "DEV") == "PROD":
        html += """
        <script async defer data-website-id="be7afe60-557b-4d2b-a504-ee2dc4583cb4" src="https://aluna-umami.netlify.app/umami.js"></script>
        """

    html += f"""
    <title>{title}</title>
    </head>
    <body>
    <svg xmlns='http://www.w3.org/2000/svg' width='56' height='100'>
      <rect width='56' height='100' fill='#a0b0c07f'/>
      <path d='M28 66L0 50L0 16L28 0L56 16L56 50L28 66L28 100' fill='none' stroke='#bcc7d2' stroke-width='2'/>
      <path d='M28 0L28 34L0 50L0 84L28 100L56 84L56 50L28 34' fill='none' stroke='#a6b5c4' stroke-width='2'/>
    </svg>
    <div id="swagger-ui"></div>
    <script src="{custom_js_url}"></script>
    <script src="{swagger_js_url}"></script>
    <script>
    const ui = SwaggerUIBundle({{
        url: '{openapi_url}',
    """

    for key, value in current_swagger_ui_parameters.items():
        html += f"{json.dumps(key)}: {json.dumps(jsonable_encoder(value))},\n"

    if oauth2_redirect_url:
        html += f"oauth2RedirectUrl: window.location.origin + '{oauth2_redirect_url}',"

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
