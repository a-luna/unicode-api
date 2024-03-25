import json
from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.openapi.docs import swagger_ui_default_parameters
from starlette.responses import HTMLResponse

from app.config.api_settings import get_settings
from app.docs.api_docs.content.block import BLOCK_ENDPOINTS, UNICODE_BLOCK_OBJECT_INTRO, UNICODE_BLOCK_OBJECT_PROPERTIES
from app.docs.api_docs.content.character import (
    CHARACTER_ENDPOINTS,
    CHARACTER_OBJECT_INTRO,
    CHARACTER_PROP_GROUPS_CONTINUED_1,
    CHARACTER_PROP_GROUPS_CONTINUED_2,
    CHARACTER_PROP_GROUPS_INTRO,
    PROP_GROUP_BASIC,
    PROP_GROUP_BIDIRECTIONALITY,
    PROP_GROUP_CASE,
    PROP_GROUP_CJK_NUMERIC,
    PROP_GROUP_CJK_READINGS,
    PROP_GROUP_CJK_VARIANTS,
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
    VERBOSITY,
)
from app.docs.api_docs.content.codepoint import CODEPOINT_CONTENT, CODEPOINTS_ENDPOINTS
from app.docs.api_docs.content.intro import (
    INTRODUCTION,
    LOOSE_MATCHING_HTML,
    PAGINATION_HTML,
    PROJECT_LINKS_SWAGGER,
    SEARCH_HTML,
)
from app.docs.api_docs.content.plane import PLANE_ENDPOINTS, UNICODE_PLANE_OBJECT_INTRO, UNICODE_PLANE_OBJECT_PROPERTIES
from app.docs.util import slugify


# fmt: off
def create_details_element_for_swagger_ui(title: str, content: str, class_name: str | None = None, open: bool | None = False) -> str:
    open_tag = "<details open" if open else "<details"
    open_tag += f" class={class_name!r}>" if class_name else ">"
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


def create_swagger_details_element_with_heading(section: str, heading_level: int, content: str, open: bool | None = False) -> str:
    id = section.replace("-", "").replace(" ", "-").lower()
    title = f'<h{heading_level} id="{id}">{section}</h{heading_level}>'
    return create_details_element_for_swagger_ui(title=title, content=content, class_name="intro", open=open)


def create_swagger_details_element_for_property_group(prop_group: str, heading_level: int, content: str, open: bool | None = False) -> str:
    title = f'<h{heading_level} id="{slugify(prop_group)}">Property Group: {prop_group}</h{heading_level}>'
    return create_details_element_for_swagger_ui(title=title, content=content, class_name="property-group", open=open)


def create_swagger_details_element_for_api_endpoints(content: str, open: bool | None = False) -> str:
    return create_details_element_for_swagger_ui(title="API Endpoints", content=content, class_name="api-endpoints", open=open)


# API DOCS INTRO SECTIONS
LINKS = create_swagger_details_element_with_heading(section="Project Resources/Contact Info", heading_level=3, content=PROJECT_LINKS_SWAGGER)
PAGINATION = create_swagger_details_element_with_heading(section="Pagination", heading_level=3, content=PAGINATION_HTML)
SEARCH = create_swagger_details_element_with_heading(section="Search", heading_level=3, content=SEARCH_HTML)
LOOSE_MATCHING = create_swagger_details_element_with_heading(section="Loose Matching", heading_level=3, content=LOOSE_MATCHING_HTML)

# API ENDPOINT DETAILS ELEMENTS
CHARACTER_API_ENDPOINTS = create_swagger_details_element_for_api_endpoints(content=CHARACTER_ENDPOINTS, open=True)
CODEPOINT_API_ENDPOINTS = create_swagger_details_element_for_api_endpoints(content=CODEPOINTS_ENDPOINTS, open=True)
BLOCK_ENDPOINTS = create_swagger_details_element_for_api_endpoints(content=BLOCK_ENDPOINTS, open=True)
PLANE_ENDPOINTS = create_swagger_details_element_for_api_endpoints(content=PLANE_ENDPOINTS, open=True)

# CHARACTER PROPERTY GROUP DETAILS ELEMENTS
CHARACTER_PROP_GROUP_MINIMUM = create_swagger_details_element_for_property_group(prop_group="Minimum", heading_level=6, content=PROP_GROUP_MINIMUM, open=True)
CHARACTER_PROP_GROUP_BASIC = create_swagger_details_element_for_property_group(prop_group="Basic", heading_level=6, content=PROP_GROUP_BASIC, open=False)
CHARACTER_PROP_GROUP_UTF8 = create_swagger_details_element_for_property_group(prop_group="UTF-8", heading_level=6, content=PROP_GROUP_UTF8, open=False)
CHARACTER_PROP_GROUP_UTF16 = create_swagger_details_element_for_property_group(prop_group="UTF-16", heading_level=6, content=PROP_GROUP_UTF16, open=False)
CHARACTER_PROP_GROUP_UTF32 = create_swagger_details_element_for_property_group(prop_group="UTF-32", heading_level=6, content=PROP_GROUP_UTF32, open=False)
CHARACTER_PROP_GROUP_BIDIRECTIONALITY = create_swagger_details_element_for_property_group(prop_group="Bidirectionality", heading_level=6, content=PROP_GROUP_BIDIRECTIONALITY, open=False)
CHARACTER_PROP_GROUP_DECOMPOSITION = create_swagger_details_element_for_property_group(prop_group="Decomposition", heading_level=6, content=PROP_GROUP_DECOMPOSITION, open=False)
CHARACTER_PROP_GROUP_QUICK_CHECK = create_swagger_details_element_for_property_group(prop_group="Quick Check", heading_level=6, content=PROP_GROUP_QUICK_CHECK, open=False)
CHARACTER_PROP_GROUP_NUMERIC = create_swagger_details_element_for_property_group(prop_group="Numeric", heading_level=6, content=PROP_GROUP_NUMERIC, open=False)
CHARACTER_PROP_GROUP_JOINING = create_swagger_details_element_for_property_group(prop_group="Joining", heading_level=6, content=PROP_GROUP_JOINING, open=False)
CHARACTER_PROP_GROUP_LINEBREAK = create_swagger_details_element_for_property_group(prop_group="Linebreak", heading_level=6, content=PROP_GROUP_LINEBREAK, open=False)
CHARACTER_PROP_GROUP_EAW = create_swagger_details_element_for_property_group(prop_group="East Asian Width", heading_level=6, content=PROP_GROUP_EAW, open=False)
CHARACTER_PROP_GROUP_CASE = create_swagger_details_element_for_property_group(prop_group="Case", heading_level=6, content=PROP_GROUP_CASE, open=False)
CHARACTER_PROP_GROUP_SCRIPT = create_swagger_details_element_for_property_group(prop_group="Script", heading_level=6, content=PROP_GROUP_SCRIPT, open=False)
CHARACTER_PROP_GROUP_HANGUL = create_swagger_details_element_for_property_group(prop_group="Hangul", heading_level=6, content=PROP_GROUP_HANGUL, open=False)
CHARACTER_PROP_GROUP_INDIC = create_swagger_details_element_for_property_group(prop_group="Indic", heading_level=6, content=PROP_GROUP_INDIC, open=False)
CHARACTER_PROP_GROUP_CJK_VARIANTS = create_swagger_details_element_for_property_group(prop_group="CJK Variants", heading_level=6, content=PROP_GROUP_CJK_VARIANTS, open=False)
CHARACTER_PROP_GROUP_CJK_NUMERIC = create_swagger_details_element_for_property_group(prop_group="CJK Numeric", heading_level=6, content=PROP_GROUP_CJK_NUMERIC, open=False)
CHARACTER_PROP_GROUP_CJK_READINGS = create_swagger_details_element_for_property_group(prop_group="CJK Readings", heading_level=6, content=PROP_GROUP_CJK_READINGS, open=False)
CHARACTER_PROP_GROUP_F_AND_G = create_swagger_details_element_for_property_group(prop_group="Function and Graphic", heading_level=6, content=PROP_GROUP_F_AND_G, open=False)
CHARACTER_PROP_GROUP_EMOJI = create_swagger_details_element_for_property_group(prop_group="Emoji", heading_level=6, content=PROP_GROUP_EMOJI, open=False)

# UNICODE CHARACTERS DOCS
UNICODE_CHARACTERS_DOCS = f"""
    <div>
        {CHARACTER_API_ENDPOINTS}<h4>The <code>UnicodeCharacter</code> Object</h4>
        {CHARACTER_OBJECT_INTRO}
        <h4 id="unicodecharacter-property-groups"><code>UnicodeCharacter</code> Property Groups</h4>
{CHARACTER_PROP_GROUPS_INTRO}
{CHARACTER_PROP_GROUP_MINIMUM}
{CHARACTER_PROP_GROUPS_CONTINUED_1}
{CHARACTER_PROP_GROUPS_CONTINUED_2}
        <h4 id="verbosity">Verbosity</h4>
{VERBOSITY}
{CHARACTER_PROP_GROUP_BASIC}
{CHARACTER_PROP_GROUP_UTF8}
{CHARACTER_PROP_GROUP_UTF16}
{CHARACTER_PROP_GROUP_UTF32}
{CHARACTER_PROP_GROUP_BIDIRECTIONALITY}
{CHARACTER_PROP_GROUP_DECOMPOSITION}
{CHARACTER_PROP_GROUP_QUICK_CHECK}
{CHARACTER_PROP_GROUP_NUMERIC}
{CHARACTER_PROP_GROUP_JOINING}
{CHARACTER_PROP_GROUP_LINEBREAK}
{CHARACTER_PROP_GROUP_EAW}
{CHARACTER_PROP_GROUP_CASE}
{CHARACTER_PROP_GROUP_SCRIPT}
{CHARACTER_PROP_GROUP_HANGUL}
{CHARACTER_PROP_GROUP_INDIC}
{CHARACTER_PROP_GROUP_CJK_VARIANTS}
{CHARACTER_PROP_GROUP_CJK_NUMERIC}
{CHARACTER_PROP_GROUP_CJK_READINGS}
{CHARACTER_PROP_GROUP_F_AND_G}
{CHARACTER_PROP_GROUP_EMOJI}
</div>
"""

UNICODE_CHARACTERS = create_swagger_details_element_with_heading(section="Unicode Characters", heading_level=4, content=UNICODE_CHARACTERS_DOCS)

# UNICODE CODEPOINTS DOCS
UNICODE_CODEPOINTS_DOCS = f"""
    <div>
        {CODEPOINT_API_ENDPOINTS}{CODEPOINT_CONTENT}</div>
"""

UNICODE_CODEPOINTS = create_swagger_details_element_with_heading(section="Unicode Codepoints", heading_level=4, content=UNICODE_CODEPOINTS_DOCS)

# UNICODE BLOCKS DOCS
UNICODE_BLOCKS_DOCS = f"""
    <div>
        {BLOCK_ENDPOINTS}<h4 id="the-unicodeblock-object">The <code>UnicodeBlock</code> Object</h4>
        {UNICODE_BLOCK_OBJECT_INTRO}
        {create_details_element_for_swagger_ui(title="<strong><code>UnicodeBlock</code> Properties</strong>", content=UNICODE_BLOCK_OBJECT_PROPERTIES, open=True)}</div>
"""

UNICODE_BLOCKS = create_swagger_details_element_with_heading(section="Unicode Blocks", heading_level=4, content=UNICODE_BLOCKS_DOCS)

# UNICODE PLANES DOCS
UNICODE_PLANES_DOCS = f"""
    <div>
        {PLANE_ENDPOINTS}<h4 id="the-unicodeplane-object">The <code>UnicodePlane</code> Object</h4>
        {UNICODE_PLANE_OBJECT_INTRO}
        {create_details_element_for_swagger_ui(title="<strong><code>UnicodePlane</code> Properties</strong>", content=UNICODE_PLANE_OBJECT_PROPERTIES, open=True)}</div>
"""

UNICODE_PLANES = create_swagger_details_element_with_heading(section="Unicode Planes", heading_level=4, content=UNICODE_PLANES_DOCS)


def get_api_docs_for_swagger_ui():
    return (
        INTRODUCTION
        + LINKS
        + PAGINATION
        + SEARCH
        + LOOSE_MATCHING
        + "<h3>Core Resources</h3>\n"
        + UNICODE_CHARACTERS
        + UNICODE_CODEPOINTS
        + UNICODE_BLOCKS
        + UNICODE_PLANES
    )


def get_swagger_ui_html(
    *,
    openapi_url: str,
    title: str,
    swagger_js_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
    swagger_css_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    swagger_favicon_url: str = "https://fastapi.tiangolo.com/img/favicon.png",
    oauth2_redirect_url: str | None = None,
    init_oauth: dict[str, Any] | None = None,
    swagger_ui_parameters: dict[str, Any] | None = None,
    custom_js_url: str | None = None,
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

    if get_settings().is_prod:
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
    <div id="swagger-ui">
    </div>
    <script src="{swagger_js_url}"></script>
    <script defer src={custom_js_url!r}></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
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
# fmt: on
