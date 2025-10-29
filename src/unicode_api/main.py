import logging.config
import time
from collections.abc import Awaitable, Callable
from contextlib import asynccontextmanager
from datetime import timedelta
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, RedirectResponse

from unicode_api.api.api_v1.api import router
from unicode_api.config.api_settings import UnicodeApiSettings, get_settings
from unicode_api.core.cache import cached_data
from unicode_api.core.logging import LOGGING_CONFIG
from unicode_api.core.rate_limit import rate_limit
from unicode_api.core.redis_client import redis
from unicode_api.core.umami import send_api_request_event_to_umami, send_rate_limit_exceeded_event_to_umami
from unicode_api.core.util import format_timedelta_str
from unicode_api.docs.api_docs.swagger_ui import get_api_docs_for_swagger_ui, get_swagger_ui_html
from unicode_api.enums.request_type import RequestType


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for the FastAPI application.

    This asynchronous function is used to manage the application's lifespan events.
    It initializes necessary components such as logging, Redis, and Unicode data
    before the application starts serving requests.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: This function yields control back to the FastAPI framework after
        performing the initialization tasks.
    """
    settings = get_settings()
    init_logging(settings)
    init_redis()
    init_unicode_data(settings)
    yield


def init_logging(settings: UnicodeApiSettings) -> None:
    """
    Initialize logging configuration for the application.

    This function sets up the logging configuration using a predefined
    dictionary-based configuration and logs initial information about
    the application's environment and Unicode version. It also logs
    a report of the rate limit settings.

    Args:
        settings (UnicodeApiSettings): The application settings containing
        environment details, Unicode version, and rate limit configuration.

    Returns:
        None
    """
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("unicode_api.api")
    logger.info(f"ENV: {settings.ENV}, UNICODE_VERSION: {settings.UNICODE_VERSION}")
    logger.info(settings.rate_limit_settings_report)


def init_redis():
    """
    Initializes the Redis client.

    This function sets up the Redis client for use within the application.
    It ensures that the Redis client is properly instantiated and ready
    for performing operations such as storing and retrieving data.
    """
    _ = redis.client


def init_unicode_data(settings: UnicodeApiSettings) -> None:
    """
    Initializes and loads Unicode data into memory by accessing various cached data properties.
    This function measures the time taken to load the data and logs the duration.

    Args:
        settings (UnicodeApiSettings): The settings object containing the Unicode version information.

    Side Effects:
        - Accesses cached Unicode data properties to ensure they are loaded into memory.
        - Logs the time taken to load the Unicode data.

    Example Log Message:
        "Unicode v13.0 data loaded in 123.45 milliseconds."
    """
    start_ns = time.process_time_ns()
    _ = cached_data.property_value_id_map
    _ = cached_data.non_unihan_character_name_map
    _ = cached_data.blocks
    _ = cached_data.planes
    _ = cached_data.all_non_unihan_codepoints
    _ = cached_data.all_cjk_codepoints
    _ = cached_data.all_tangut_ideograph_codepoints
    _ = cached_data.all_tangut_component_codepoints
    end_ns = time.process_time_ns()
    td_ms = (end_ns - start_ns) / 1_000_000
    td = timedelta(milliseconds=td_ms)
    logger = logging.getLogger("unicode_api.api")
    logger.info(
        f"Unicode v{settings.UNICODE_VERSION} data loaded in {format_timedelta_str(td, precise=True)} milliseconds."
    )


def simplify_operation_ids(app: FastAPI) -> None:
    """
    Simplifies the operation IDs of all API routes in a FastAPI application.

    This function iterates through all the routes in the provided FastAPI application.
    For each route that is an instance of `APIRoute`, it sets the `operation_id` to the
    route's name. Additionally, it appends the route's name, path, and path regex to
    a cached data structure for further use.

    Args:
        app (FastAPI): The FastAPI application instance whose routes will be processed.

    Returns:
        None
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name
            cached_data.api_routes.append({"name": route.name, "path": route.path, "path_regex": route.path_regex})


app = FastAPI(
    title=get_settings().project_name,
    description=get_api_docs_for_swagger_ui(),
    version=get_settings().API_VERSION,
    openapi_url=f"{get_settings().API_VERSION}/openapi.json",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3500",
        "http://10.0.1.74:3500",
        "https://base64.aaronluna.dev",
        "http://172.17.0.1",
    ],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["X-UnicodeAPI-Test"],
)
STATIC_FOLDER = Path(__file__).parent.joinpath("static")
app.mount("/static", StaticFiles(directory=str(STATIC_FOLDER)), name="static")
app.include_router(router, prefix=get_settings().API_VERSION)
simplify_operation_ids(app)


@app.middleware("http")
async def apply_rate_limiting(request: Request, call_next: Callable[[Request], Awaitable[Response]]):
    """
    Middleware function to apply rate limiting to incoming requests.

    This function evaluates whether a request should be allowed, denied, or results
    in an error based on rate limiting rules. It logs the decision and sends
    appropriate events to an analytics service.

    Args:
        request (Request): The incoming HTTP request object.
        call_next (Callable): The next middleware or endpoint to call if the request
            is allowed.

    Returns:
        JSONResponse: A JSON response with an appropriate status code and error
            message if the request is denied or an error occurs.
        Awaitable: The result of calling the next middleware or endpoint if the
            request is allowed.
    """
    decision = rate_limit.validate_request(request)
    match decision.request_type:
        case RequestType.RATE_LIMITED_ALLOWED:
            send_api_request_event_to_umami(request, decision.ip)
            decision.log()
        case RequestType.RATE_LIMITED_DENIED:
            send_rate_limit_exceeded_event_to_umami(request, decision.ip)
            decision.log()
            return JSONResponse(content=decision.error, status_code=status.HTTP_429_TOO_MANY_REQUESTS)
        case RequestType.ERROR:
            return JSONResponse(content=decision.error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        case _:
            pass
    return await call_next(request)


@app.get(f"{get_settings().API_VERSION}/docs", include_in_schema=False, response_class=FileResponse)
async def swagger_ui_html():
    """
    Generate the Swagger UI HTML for the API documentation.

    This function returns a customized Swagger UI HTML page for the API documentation.
    It uses the `get_swagger_ui_html` function to generate the HTML with various parameters
    to configure the appearance and behavior of the Swagger UI.

    Returns:
        HTMLResponse: The generated Swagger UI HTML page.

    Swagger UI Parameters:
        - docExpansion: Controls how the API documentation is expanded. Default is "list".
        - defaultModelsExpandDepth: Sets the default expansion depth for models. Default is -1 (collapsed).
        - useUnsafeMarkdown: Enables the use of unsafe Markdown. Default is True.
        - syntaxHighlight.theme: Sets the syntax highlighting theme. Default is "arta".
        - tryItOutEnabled: Enables the "Try it out" feature. Default is True.
        - displayRequestDuration: Displays the duration of API requests. Default is True.
        - requestSnippetsEnabled: Enables request snippets. Default is True.
        - requestSnippets: Configures request snippet generators and their behavior.
            - generators: Defines available snippet generators (e.g., cURL with bash syntax).
            - defaultExpanded: Determines if snippets are expanded by default. Default is False.
            - languages: Specifies supported languages for snippets. Default is None.

    Custom URLs:
        - swagger_js_url: URL for the Swagger UI JavaScript file.
        - swagger_css_url: URL for the Swagger UI CSS file.
        - swagger_favicon_url: URL for the Swagger UI favicon.
        - custom_js_url: URL for a custom JavaScript file to extend Swagger UI functionality.
    """
    return get_swagger_ui_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title=f"{get_settings().project_name} Docs - Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="/static/favicon.png",
        swagger_ui_parameters={
            "docExpansion": "list",
            "defaultModelsExpandDepth": -1,
            "useUnsafeMarkdown": True,
            "syntaxHighlight.theme": "arta",
            "tryItOutEnabled": "true",
            "displayRequestDuration": "true",
            "requestSnippetsEnabled": "true",
            "requestSnippets": {
                "generators": {
                    "curl_bash": {"title": "cURL (bash)", "syntax": "bash"},
                },
                "defaultExpanded": False,
                "languages": None,
            },
        },
        custom_js_url="/static/custom.js",
    )


@app.get("/", include_in_schema=False)
def get_api_root():
    """
    Redirects the root endpoint of the API to the Swagger UI documentation.

    Returns:
        RedirectResponse: A response object that redirects to the Swagger UI
        with a 308 Permanent Redirect status code.
    """
    return RedirectResponse(
        url=app.url_path_for("swagger_ui_html"),
        status_code=status.HTTP_308_PERMANENT_REDIRECT,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
