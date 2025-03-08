import logging.config
import time
from contextlib import asynccontextmanager
from pathlib import Path

import requests
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, RedirectResponse

from app.api.api_v1.api import router
from app.config.api_settings import UnicodeApiSettings, get_settings
from app.constants import LOCALE_REGEX
from app.core.cache import cached_data
from app.core.logging import LOGGING_CONFIG
from app.core.rate_limit import RateLimitDecision, rate_limit
from app.core.redis_client import redis
from app.docs.api_docs.swagger_ui import get_api_docs_for_swagger_ui, get_swagger_ui_html
from app.enums.request_type import RequestType


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    init_logging(settings)
    init_redis()
    init_unicode_data(settings)
    yield


def init_logging(settings: UnicodeApiSettings) -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("app.api")
    logger.info(f"ENV: {settings.ENV}, UNICODE_VERSION: {settings.UNICODE_VERSION}")
    logger.info(settings.rate_limit_settings_report)


def init_redis():
    _ = redis.client


def init_unicode_data(settings: UnicodeApiSettings) -> None:
    start = time.process_time_ns()
    _ = cached_data.property_value_id_map
    _ = cached_data.non_unihan_character_name_map
    _ = cached_data.blocks
    _ = cached_data.planes
    _ = cached_data.all_non_unihan_codepoints
    _ = cached_data.all_cjk_codepoints
    _ = cached_data.all_tangut_ideograph_codepoints
    _ = cached_data.all_tangut_component_codepoints
    end = time.process_time_ns()
    td = (end - start) / 1_000_000
    logger = logging.getLogger("app.api")
    logger.info(f"Initialized Unicode v{settings.UNICODE_VERSION} data in {td:.0f} milliseconds.")


def simplify_operation_ids(app: FastAPI) -> None:
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


app = FastAPI(
    title=get_settings().PROJECT_NAME,
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
async def apply_rate_limiting(request: Request, call_next):
    logger = logging.getLogger("app.api")
    logger.info(f"URL: {request.path_params}, {request.query_params.items()}")
    decision, error = rate_limit.validate_request(request)
    if decision.request_type == RequestType.RATE_LIMITED_DENIED:
        decision.log()
        return JSONResponse(content=error, status_code=status.HTTP_429_TOO_MANY_REQUESTS)
    if decision.request_type == RequestType.ERROR:
        return JSONResponse(content=error, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if decision.request_type in [RequestType.RATE_LIMITED_ALLOWED]:
        send_umami_event(request, decision)
        decision.log()
    return await call_next(request)


def send_umami_event(request: Request, decision: RateLimitDecision):
    settings = get_settings()
    if settings.is_dev or settings.is_test:
        return
    umami_url = "https://aluna-umami.netlify.app/api/send"
    response = requests.post(
        umami_url,
        headers={
            "Content-Type": "application/json",
            "User-Agent": request.headers.get("User-Agent", requests.utils.default_user_agent()),
        },
        json={"payload": create_umami_event_payload(settings, request, decision), "type": "event"},
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger = logging.getLogger("app.api")
        logger.error(f"HTTP error occurred: {e}")


def create_umami_event_payload(settings: UnicodeApiSettings, request: Request, decision: RateLimitDecision) -> dict:
    return {
        "hostname": settings.HOSTNAME,
        "language": request.headers.get("Accept-Language", "en-US"),
        "referrer": request.headers.get("Referer", ""),
        "screen": f"{request.headers.get('Screen-Width', '')}x{request.headers.get('Screen-Height', '')}",
        "title": f"{settings.PROJECT_NAME} API",
        "url": request.url.path,
        "website": settings.UMAMI_WEBSITE_ID,
        "name": request.url.path,
        "data": get_umami_event_data(request, decision),
    }


def get_umami_event_data(request: Request, decision: RateLimitDecision) -> dict:
    language, variant = get_user_locale(request)
    data = {"client_ip": decision.ip, "language": language, "variant": variant}
    for n, (param, val) in enumerate(request.query_params.items()):
        data[f"param-{n}-name"] = param
        data[f"param-{n}-value"] = val
    return data


def get_user_locale(request: Request) -> tuple[str, str]:
    header_accept_lang = request.headers.get("Accept-Language", "")
    if match := LOCALE_REGEX.match(header_accept_lang):
        return (match.group(1), match.group(2))
    return ("", "")


@app.get(f"{get_settings().API_VERSION}/docs", include_in_schema=False, response_class=FileResponse)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title=f"{get_settings().PROJECT_NAME} Docs - Swagger UI",
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
    return RedirectResponse(
        url=app.url_path_for("swagger_ui_html"),
        status_code=status.HTTP_308_PERMANENT_REDIRECT,
    )
