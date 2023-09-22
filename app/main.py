import logging.config
import os
import re
from http import HTTPStatus
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi_utils.openapi import simplify_operation_ids
from starlette.responses import FileResponse, RedirectResponse

from app.api.api_v1.api import router
from app.core.config import get_settings
from app.core.redis_client import redis
from app.data.cache import cached_data
from app.docs.api_docs.swagger_ui import get_api_docs_for_swagger_ui, get_swagger_ui_html

APP_FOLDER = Path(__file__).parent
STATIC_FOLDER = APP_FOLDER.joinpath("static")
RATE_LIMIT_ROUTE_REGEX = re.compile(r"^\/v1\/blocks|characters|planes")


app = FastAPI(
    title=get_settings().PROJECT_NAME,
    description=get_api_docs_for_swagger_ui(),
    version=get_settings().API_VERSION,
    openapi_url=f"{get_settings().API_VERSION}/openapi.json",
    docs_url=None,
    redoc_url=None,
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
app.mount("/static", StaticFiles(directory=str(STATIC_FOLDER)), name="static")


@app.on_event("startup")
def init_unicode_obj():
    _ = cached_data.non_unihan_character_name_map
    _ = cached_data.blocks
    _ = cached_data.planes
    _ = cached_data.all_unicode_versions


@app.on_event("startup")
def init_redis_client():
    settings = get_settings()
    logging.config.dictConfig(settings.LOGGING_CONFIG)
    _ = redis.get_redis_client()


@app.middleware("http")
async def apply_rate_limiting(request: Request, call_next):
    if testing(request) or not RATE_LIMIT_ROUTE_REGEX.search(request.url.path) or not request.client:
        return await call_next(request)
    result = redis.is_request_allowed_by_rate_limit(request.client.host)
    if result.success:
        return await call_next(request)
    return JSONResponse(content=result.error, status_code=int(HTTPStatus.TOO_MANY_REQUESTS))


def testing(request: Request) -> bool:
    test_header = os.environ.get("TEST_HEADER", "").lower()
    return (
        test_header in request.headers or test_header in request.headers.get("access-control-request-headers", [])
        if test_header
        else False
    )


@app.get(f"{get_settings().API_VERSION}/docs", include_in_schema=False, response_class=FileResponse)
async def swagger_ui_html():
    settings = get_settings()
    return get_swagger_ui_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title=f"{settings.PROJECT_NAME} Docs - Swagger UI",
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
        status_code=int(HTTPStatus.PERMANENT_REDIRECT),
    )


app.include_router(router, prefix=get_settings().API_VERSION)
simplify_operation_ids(app)
