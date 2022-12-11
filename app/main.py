import os
from http import HTTPStatus
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi_redis_cache import FastApiRedisCache
from starlette.responses import RedirectResponse

from app.api.api_v1.api import router
from app.api.api_v1.dependencies import get_unicode
from app.core.config import settings


APP_FOLDER = Path(__file__).parent
STATIC_FOLDER = APP_FOLDER.joinpath("static")

API_DESCRIPTION = """
<p><a href="https://github.com/a-luna/unicode-api" target="_blank" rel="noreferrer">Source Code (github.com)</a></p>
<details>
    <summary>
        <div>
            <span>Properties of the <strong>UnicodeCharacter</strong> Object</span>
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512" stroke="currentColor" fill="currentColor" style="stroke-width: 0; padding: 0; ">
                    <path d="M285.476 272.971L91.132 467.314c-9.373 9.373-24.569 9.373-33.941 0l-22.667-22.667c-9.357-9.357-9.375-24.522-.04-33.901L188.505 256 34.484 101.255c-9.335-9.379-9.317-24.544.04-33.901l22.667-22.667c9.373-9.373 24.569-9.373 33.941 0L285.475 239.03c9.373 9.372 9.373 24.568.001 33.941z"></path>
                </svg>
            </div>
        </div>
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
        <dd>The <a href="https://www.unicode.org/versions/latest/ch04.pdf#G124142">General Category</a> that this character belongs to (e.g., letters, numbers, punctuation, symbols, etc.). The full list of values which are valid for this property is defined in <a href="http://www.unicode.org/reports/tr44/#General_Category_Values">Unicode Standard Annex #44</a></dd>
        <dt><strong>bidirectional_class</strong></dt>
        <dd>A value assigned to each Unicode character based on the appropriate directional formatting style. Each character has an implicit <i>bidirectional type</i>. The bidirectional types left-to-right and right-to-left are called <i>strong types</i>, and characters of those types are called strong directional characters. The bidirectional types associated with numbers are called <i>weak types</i>.</dd>
        <dt><strong>combining_class</strong></dt>
        <dd>Similar to <strong>bidirectional_class</strong>, this value helps to determine how the canonical ordering of sequences of combining characters takes place. For more info, please see <a href="https://www.unicode.org/versions/Unicode15.0.0/ch04.pdf#page=11">Unicode Standard Section 4.3</a>.</dd>
        <dt><strong>bidirectional_is_mirrored</strong></dt>
        <dd>A normative property of characters such as parentheses, whose images are mirrored horizontally in text that is laid out from right to left. For example, <code>U+0028 <span>LEFT PARENTHESIS</span></code> is interpreted as opening parenthesis; in a left-to-right context it will appear as “(”, while in a right-to-left context it will appear as the mirrored glyph “)”. This requirement is necessary to render the character properly in a bidirectional context.</dd>
        <dt><strong>html_entities</strong></dt>
        <dd>A string begining with an ampersand (&) character and ending with a semicolon (;). Entities are used to display reserved characters (e.g., '<' in an HTML document) or invisible characters (e.g., non-breaking spaces). For more info, please see the <a href="https://developer.mozilla.org/en-US/docs/Glossary/Entity">MDN entry for HTML Entities</a>.</dd>
        <dt><strong>uri_encoded</strong></dt>
        <dd>The character as a URI encoded string. A URI is a string that identifies an abstract or physical resource on the internet (The specification for the URI format is defined in <a href="https://www.rfc-editor.org/rfc/rfc3986">RFC 3986</a>). The string must contain only a defined subset of characters from the standard 128 ASCII character set, any other characters must be replaced by an escape sequence representing the UTF-8 encoding of the character. For example, ∑ (<code>U+2211 <span>N-ARY SUMMATION</span></code>) is equal to <code>0xE2 0x88 0x91</code> in UTF-8 encoding. When used as part of a URI, this character must be escaped using the string <code>%E2%88%91</code>.</dd>
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

This API provides access to every character in the Unicode database. It can be used in various ways:
- You can list all characters ordered by codepoint using the **`/api/v1/characters`** endpoint.
  - Rather than listing every character, you can list only characters from a Unicode Block using the **block** query parameter.
  - By default, the response contains only the rendered character, name and codepoint for each character. A **link** is provided with each character that can be used to request the full set of character properties.
- You can search the Unicode database by name using the **`/api/v1/characters/search`** endpoint.
- If you would like to see detailed information about a Unicode character, use the **`/api/v1/characters/{string}`** endpoint.
"""  # noqa: B950

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=API_DESCRIPTION,
    version=settings.API_VERSION,
    contact={
        "name": "Aaron Luna",
        "url": "https://aaronluna.dev",
        "email": "contact@aaronluna.dev",
    },
    license_info={
        "name": "MIT",
        "url": "https://github.com/a-luna/unicode-api/blob/main/LICENSE",
    },
    openapi_url=f"{settings.API_VERSION}/openapi.json",
    docs_url=None,
    redoc_url=None,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3500",
        "http://10.0.1.74:3500",
        "https://base64-demo.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=str(STATIC_FOLDER)), name="static")


@app.on_event("startup")
def init_redis():
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url=settings.REDIS_URL,
        response_header=settings.CACHE_HEADER,
    )


# @app.on_event("startup")
# def init_unicode_obj():
#     if os.environ.get("ENV") != "PROD":
#         return
#     unicode = get_unicode()
#     unicode.characters
#     unicode.blocks
#     unicode.planes


@app.get(f"{settings.API_VERSION}/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        title=f"{settings.PROJECT_NAME} - Swagger UI",
        openapi_url=app.openapi_url,
        swagger_ui_parameters={
            "docExpansion": "list",
            "defaultModelsExpandDepth": 0,
            "syntaxHighlight.theme": "arta",
            "tryItOutEnabled": "true",
            "displayRequestDuration": "true",
        },
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="/static/favicon.png",
    )


@app.get("/", include_in_schema=False)
def get_api_root():
    return RedirectResponse(
        url=app.url_path_for("swagger_ui_html"),
        status_code=int(HTTPStatus.PERMANENT_REDIRECT),
    )


app.include_router(router, prefix=settings.API_VERSION)
